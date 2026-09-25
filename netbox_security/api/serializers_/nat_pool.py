from netbox_security.mixins import GenericAssignmentValidationMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    IntegerField,
)

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer

from netbox_security.models import NatPool, NatPoolAssignment

from netbox_security.constants import (
    POOL_ASSIGNMENT_MODELS,
)


class NatPoolSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:natpool-detail"
    )
    member_count = IntegerField(read_only=True)

    class Meta:
        model = NatPool
        fields = (
            "id",
            "url",
            "display",
            "name",
            "pool_type",
            "status",
            "description",
            "member_count",
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
            "status",
            "pool_type",
            "description",
            "member_count",
        )


class NatPoolAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = POOL_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
    pool = NatPoolSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(POOL_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = NatPoolAssignment
        fields = [
            "id",
            "url",
            "display",
            "pool",
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
            "pool",
            "assigned_object_type",
            "assigned_object_id",
        )
