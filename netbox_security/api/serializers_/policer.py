from netbox_security.mixins import GenericAssignmentValidationMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    BooleanField,
    SerializerMethodField,
    IntegerField,
)

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers import TenantSerializer

from netbox_security.models import Policer, PolicerAssignment
from netbox_security.constants import (
    POLICER_ASSIGNMENT_MODELS,
)


class PolicerSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:policer-detail"
    )
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    logical_interface_policer = BooleanField(required=False, allow_null=True)
    physical_interface_policer = BooleanField(required=False, allow_null=True)
    discard = BooleanField(required=False, allow_null=True)
    out_of_profile = BooleanField(required=False, allow_null=True)
    bandwidth_limit = IntegerField(required=False, allow_null=True)
    bandwidth_percent = IntegerField(required=False, allow_null=True)
    burst_size_limit = IntegerField(required=False, allow_null=True)

    class Meta:
        model = Policer
        fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "tenant",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
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
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "description",
        )


class PolicerAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = POLICER_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
    policer = PolicerSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(POLICER_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = PolicerAssignment
        fields = [
            "id",
            "url",
            "display",
            "policer",
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
            "policer",
            "assigned_object_type",
            "assigned_object_id",
        )
