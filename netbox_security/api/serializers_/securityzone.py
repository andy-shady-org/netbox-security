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

from netbox_security.models import SecurityZone, SecurityZoneAssignment
from netbox_security.constants import ZONE_ASSIGNMENT_MODELS


class SecurityZoneSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:securityzone-detail"
    )
    source_policy_count = IntegerField(read_only=True)
    destination_policy_count = IntegerField(read_only=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = SecurityZone
        fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "description",
            "tenant",
            "source_policy_count",
            "destination_policy_count",
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
            "source_policy_count",
            "destination_policy_count",
            "description",
        )


class SecurityZoneAssignmentSerializer(NetBoxModelSerializer):
    zone = SecurityZoneSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ZONE_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = SecurityZoneAssignment
        fields = [
            "id",
            "url",
            "display",
            "zone",
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
            "zone",
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
