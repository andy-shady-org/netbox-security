from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model

from netbox_security.api.serializers import FirewallFilterSerializer

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


class FirewallRuleFromSettingSerializer(NetBoxModelSerializer):
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

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, context=context, nested=True).data


class FirewallRuleThenSettingSerializer(NetBoxModelSerializer):
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

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, context=context, nested=True).data


class FirewallFilterRuleSerializer(NetBoxModelSerializer):
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
