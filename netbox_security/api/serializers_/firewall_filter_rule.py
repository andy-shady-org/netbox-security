from netbox_security.constants import FILTER_SETTING_ASSIGNMENT_MODELS
from netbox_security.mixins import GenericAssignmentValidationMixin
from rest_framework import serializers

from netbox.api.serializers import PrimaryModelSerializer

from .firewall_filter import FirewallFilterSerializer

from netbox_security.models import (
    FirewallFilterRule,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
)

__all__ = (
    "FirewallFilterRuleSerializer",
    "FirewallRuleFromSettingSerializer",
    "FirewallRuleThenSettingSerializer",
)


class FirewallRuleFromSettingSerializer(
    GenericAssignmentValidationMixin, PrimaryModelSerializer
):
    assignment_models = FILTER_SETTING_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = True
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:firewallrulefromsetting-detail"
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FirewallRuleFromSetting
        fields = (
            "url",
            "id",
            "display",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "key",
            "value",
            "description",
            "comments",
        )
        brief_fields = (
            "url",
            "id",
            "display",
            "assigned_object",
            "key",
        )


class FirewallRuleThenSettingSerializer(
    GenericAssignmentValidationMixin, PrimaryModelSerializer
):
    assignment_models = FILTER_SETTING_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = True
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:firewallrulethensetting-detail"
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FirewallRuleThenSetting
        fields = (
            "url",
            "id",
            "display",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "key",
            "value",
            "description",
            "comments",
        )
        brief_fields = (
            "url",
            "id",
            "display",
            "assigned_object",
            "key",
        )


class FirewallFilterRuleSerializer(PrimaryModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:firewallfilterrule-detail"
    )
    firewall_filter = FirewallFilterSerializer(nested=True, required=True)
    from_settings = FirewallRuleFromSettingSerializer(required=False, many=True)
    then_settings = FirewallRuleThenSettingSerializer(required=False, many=True)

    class Meta:
        model = FirewallFilterRule
        fields = (
            "url",
            "id",
            "display",
            "name",
            "index",
            "firewall_filter",
            "from_settings",
            "then_settings",
            "description",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "url",
            "id",
            "display",
            "name",
            "description",
            "index",
            "firewall_filter",
        )
