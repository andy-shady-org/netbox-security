from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ChoiceField,
    SerializerMethodField,
    JSONField,
    IntegerField,
    ValidationError,
)
from drf_spectacular.utils import extend_schema_field

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model

from netbox_security.models import NatRuleSet, NatRuleSetAssignment
from netbox_security.constants import (
    RULESET_ASSIGNMENT_MODELS,
)
from netbox_security.choices import (
    NatTypeChoices,
    RuleDirectionChoices,
)

from netbox_security.api.serializers import SecurityZoneSerializer


class NatRuleSetSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:natruleset-detail"
    )
    nat_type = ChoiceField(choices=NatTypeChoices, required=True)
    direction = ChoiceField(choices=RuleDirectionChoices, required=True)
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
        error_message = {}
        if isinstance(data, dict):
            if (source_zones := data.get("source_zones")) is not None and (
                destination_zones := data.get("destination_zones")
            ) is not None:
                if set(source_zones) & set(destination_zones):
                    error_message_mismatch_zones = "Cannot have the same source and destination zones within a rule"
                    error_message["source_zones"] = [error_message_mismatch_zones]
                    error_message["destination_zones"] = [error_message_mismatch_zones]
        if error_message:
            raise ValidationError(error_message)
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


class NatRuleSetAssignmentSerializer(NetBoxModelSerializer):
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

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data
