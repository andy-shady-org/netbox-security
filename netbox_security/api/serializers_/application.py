from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    JSONField,
    ChoiceField,
    ListField,
    IntegerField,
)
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model
from tenancy.api.serializers import TenantSerializer
from netbox_security.models import Application, ApplicationAssignment
from netbox_security.api.serializers import ApplicationItemSerializer
from netbox_security.constants import APPLICATION_ASSIGNMENT_MODELS
from netbox_security.choices import ProtocolChoices


class ApplicationSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:application-detail"
    )
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    application_items = ApplicationItemSerializer(
        nested=True, required=False, allow_null=True, many=True
    )
    protocol = ListField(
        child=ChoiceField(choices=ProtocolChoices, required=False, allow_null=True),
        required=False,
        default=[],
    )
    source_ports = ListField(
        child=IntegerField(),
        required=False,
        allow_empty=True,
        default=[],
    )
    destination_ports = ListField(
        child=IntegerField(),
        required=False,
        allow_empty=True,
        default=[],
    )

    class Meta:
        model = Application
        fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "application_items",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
            "tenant",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "application_items",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
        )

    def create(self, validated_data):
        items = validated_data.pop("application_items", None)
        obj = super().create(validated_data)
        if items is not None:
            obj.application_items.set(items)
        return obj

    def update(self, instance, validated_data):
        items = validated_data.pop("application_items", None)
        obj = super().update(instance, validated_data)
        if items is not None:
            obj.application_items.set(items)
        return obj


class ApplicationAssignmentSerializer(NetBoxModelSerializer):
    application = ApplicationSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(APPLICATION_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = ApplicationAssignment
        fields = [
            "id",
            "url",
            "display",
            "application",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "created",
            "last_updated",
        ]
        brief_fields = (
            "id",
            "url",
            "display",
            "application",
            "assigned_object_type",
            "assigned_object_id",
        )

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data
