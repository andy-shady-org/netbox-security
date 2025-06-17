from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    JSONField,
    IntegerField,
)
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model
from tenancy.api.serializers import TenantSerializer

from netbox_security.models import FirewallFilter, FirewallFilterAssignment
from netbox_security.constants import FILTER_ASSIGNMENT_MODELS


class FirewallFilterSerializer(NetBoxModelSerializer):
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


class FirewallFilterAssignmentSerializer(NetBoxModelSerializer):
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

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data
