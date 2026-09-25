from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import JSONField
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError


def restrict_generic_assignments(
    queryset, user, *, assignment_models=None, allow_empty_assignment=None, seen=()
):
    """Filter generic targets before pagination, including plugin reference chains."""
    model = queryset.model
    if model._meta.app_label != "netbox_security":
        return queryset
    try:
        type_field = model._meta.get_field("assigned_object_type")
        id_field = model._meta.get_field("assigned_object_id")
    except FieldDoesNotExist:
        return queryset
    if model in seen:
        return queryset.none()
    if assignment_models is None:
        assignment_models = type_field.get_limit_choices_to()
    if allow_empty_assignment is None:
        allow_empty_assignment = type_field.null and id_field.null

    visible = Q(pk__in=[])
    if allow_empty_assignment:
        empty = Q(assigned_object_type__isnull=True, assigned_object_id__isnull=True)
        if model._meta.model_name == "address":
            empty &= Q(dns_name__isnull=False) & ~Q(dns_name="")
        visible |= empty

    for content_type in ContentType.objects.filter(assignment_models):
        target_model = content_type.model_class()
        manager = getattr(target_model, "objects", None)
        if manager is None or not hasattr(manager, "restrict"):
            continue
        targets = restrict_generic_assignments(
            manager.restrict(user, "view"), user, seen=(*seen, model)
        )
        visible |= Q(
            assigned_object_type_id=content_type.pk,
            assigned_object_id__in=targets.order_by().values("pk"),
        )
    return queryset.filter(visible)


def get_visible_assignment_target(obj, user):
    content_type = obj.assigned_object_type
    object_id = obj.assigned_object_id
    if content_type is None or object_id is None:
        return None
    allowed = obj._meta.get_field("assigned_object_type").get_limit_choices_to()
    if not ContentType.objects.filter(allowed, pk=content_type.pk).exists():
        return None
    manager = getattr(content_type.model_class(), "objects", None)
    if manager is None or not hasattr(manager, "restrict"):
        return None
    targets = restrict_generic_assignments(manager.restrict(user, "view"), user)
    return targets.filter(pk=object_id).first()


class GenericAssignmentViewSetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        request = getattr(self, "request", None)
        if request is None:
            return queryset.none()
        return restrict_generic_assignments(
            queryset,
            request.user,
            assignment_models=self.serializer_class.assignment_models,
            allow_empty_assignment=self.serializer_class.allow_empty_assignment,
        )


class GenericAssignmentValidationMixin:
    assignment_models = None
    allow_empty_assignment = False

    assignment_permission = "view"

    def validate(self, data):
        if not isinstance(data, dict):
            # Nested input resolves to an existing object, not a write payload.
            request = self.context.get("request")
            if request is None:
                raise PermissionDenied("A request context is required.")
            visible = restrict_generic_assignments(
                self.Meta.model.objects.restrict(request.user, "view"), request.user
            )
            if not visible.filter(pk=data.pk).exists():
                raise ValidationError(
                    "The reference does not exist or is not permitted."
                )
            return super().validate(data)

        content_type = data.get(
            "assigned_object_type",
            getattr(self.instance, "assigned_object_type", None),
        )
        object_id = data.get(
            "assigned_object_id",
            getattr(self.instance, "assigned_object_id", None),
        )

        if content_type is None and object_id is None:
            if self.allow_empty_assignment:
                return super().validate(data)
            raise ValidationError(
                {
                    "assigned_object_id": "An assignment target is required.",
                }
            )

        if content_type is None or object_id is None:
            raise ValidationError(
                {
                    "assigned_object_type": (
                        "Specify both the object type and object ID."
                    ),
                    "assigned_object_id": (
                        "Specify both the object type and object ID."
                    ),
                }
            )

        if (
            self.assignment_models is None
            or not ContentType.objects.filter(
                self.assignment_models,
                pk=content_type.pk,
            ).exists()
        ):
            raise ValidationError(
                {
                    "assigned_object_type": "Unsupported assignment type.",
                }
            )

        request = self.context.get("request")
        if request is None:
            raise PermissionDenied(
                "A request context is required to validate the target."
            )

        model = content_type.model_class()
        manager = getattr(model, "objects", None)
        if manager is None or not hasattr(manager, "restrict"):
            raise ValidationError(
                {
                    "assigned_object_type": "Unsupported assignment type.",
                }
            )

        targets = restrict_generic_assignments(
            manager.restrict(request.user, "view"), request.user
        )
        if self.assignment_permission != "view":
            targets = targets.restrict(request.user, self.assignment_permission)

        if not targets.filter(pk=object_id).exists():
            raise ValidationError(
                {
                    "assigned_object_id": (
                        "The target does not exist or is not permitted."
                    ),
                }
            )

        return super().validate(data)

    def _is_event_serialization(self):
        # NetBox's serialize_for_event() explicitly supplies request=None.
        # A missing context must still fail closed; writes never use this bypass.
        return "request" in self.context and self.context["request"] is None

    def to_representation(self, instance):
        if self._is_event_serialization():
            return super().to_representation(instance)
        # Nested serializers bypass the target-filtered viewset. Check before
        # rendering display/URLs, which may dereference the generic target.
        if (
            instance.assigned_object_type_id is not None
            or instance.assigned_object_id is not None
        ):
            request = self.context.get("request")
            if (
                request is None
                or get_visible_assignment_target(instance, request.user) is None
            ):
                raise PermissionDenied("The assignment target is not accessible.")
        return super().to_representation(instance)

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        from utilities.api import get_serializer_for_model

        if self._is_event_serialization():
            # Event payloads are internal snapshots, independent of user access.
            target = obj.assigned_object
        else:
            request = self.context.get("request")
            if request is None:
                return None
            target = get_visible_assignment_target(obj, request.user)
        if target is None:
            return None
        serializer = get_serializer_for_model(target)
        return serializer(target, nested=True, context=self.context).data
