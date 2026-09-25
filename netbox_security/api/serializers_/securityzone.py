from netbox_security.mixins import GenericAssignmentValidationMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    IntegerField,
    BooleanField,
)
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer
from tenancy.api.serializers import TenantSerializer

from netbox_security.models import SecurityZone, SecurityZoneAssignment
from netbox_security.constants import ZONE_ASSIGNMENT_MODELS


class SecurityZoneSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:securityzone-detail"
    )
    allow_intra_zone = BooleanField(required=False, default=False)
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
            "allow_intra_zone",
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
            "allow_intra_zone",
            "source_policy_count",
            "destination_policy_count",
            "description",
        )


class SecurityZoneAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = ZONE_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
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
