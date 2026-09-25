from netbox_security.mixins import GenericAssignmentValidationMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    IntegerField,
)
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer
from tenancy.api.serializers import TenantSerializer

from netbox_security.models import FirewallFilter, FirewallFilterAssignment
from netbox_security.constants import FILTER_ASSIGNMENT_MODELS


class FirewallFilterSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:firewallfilter-detail"
    )
    rule_count = IntegerField(read_only=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = FirewallFilter
        fields = (
            "id",
            "url",
            "display",
            "name",
            "family",
            "rule_count",
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
            "family",
            "rule_count",
            "description",
        )


class FirewallFilterAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = FILTER_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
    firewall_filter = FirewallFilterSerializer(
        nested=True, required=True, allow_null=False
    )
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(FILTER_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = FirewallFilterAssignment
        fields = [
            "id",
            "url",
            "display",
            "firewall_filter",
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
            "firewall_filter",
            "assigned_object_type",
            "assigned_object_id",
        )
