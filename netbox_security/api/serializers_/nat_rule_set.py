from netbox_security.mixins import GenericAssignmentValidationMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    IntegerField,
    ValidationError,
)

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer

from netbox_security.models import NatRuleSet, NatRuleSetAssignment
from netbox_security.constants import (
    RULESET_ASSIGNMENT_MODELS,
)

from .securityzone import SecurityZoneSerializer


class NatRuleSetSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:natruleset-detail"
    )
    rule_count = IntegerField(read_only=True)
    source_zones = SecurityZoneSerializer(
        nested=True, required=False, allow_null=True, many=True
    )
    destination_zones = SecurityZoneSerializer(
        nested=True, required=False, allow_null=True, many=True
    )

    class Meta:
        model = NatRuleSet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "nat_type",
            "direction",
            "source_zones",
            "destination_zones",
            "rule_count",
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
            "description",
            "nat_type",
            "direction",
            "rule_count",
        )

    def validate(self, data):
        if not isinstance(data, dict):
            return super().validate(data)

        source_zones = data.get("source_zones")
        destination_zones = data.get("destination_zones")

        if source_zones and destination_zones:
            overlapping_zones = set(source_zones) & set(destination_zones)
            if overlapping_zones:
                message = (
                    "Cannot have the same source and destination zones within a rule."
                )
                raise ValidationError(
                    {
                        "source_zones": [message],
                        "destination_zones": [message],
                    }
                )

        return super().validate(data)

    def create(self, validated_data):
        source_zones = validated_data.pop("source_zones", None)
        destination_zones = validated_data.pop("destination_zones", None)
        rule = super().create(validated_data)

        if source_zones is not None:
            rule.source_zones.set(source_zones)
        if destination_zones is not None:
            rule.destination_zones.set(destination_zones)
        return rule

    def update(self, instance, validated_data):
        source_zones = validated_data.pop("source_zones", None)
        destination_zones = validated_data.pop("destination_zones", None)
        rule = super().update(instance, validated_data)

        if source_zones is not None:
            rule.source_zones.set(source_zones)
        if destination_zones is not None:
            rule.destination_zones.set(destination_zones)
        return rule


class NatRuleSetAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = RULESET_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
    ruleset = NatRuleSetSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(RULESET_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = NatRuleSetAssignment
        fields = [
            "id",
            "url",
            "display",
            "ruleset",
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
            "ruleset",
            "assigned_object_type",
            "assigned_object_id",
        )
