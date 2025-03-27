from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model

from netbox_security.api.serializers import FirewallFilterSerializer

from netbox_security.models import (
    FirewallFilterRule,
    FirewallRuleSetting
)

__all__ = (
    'FirewallFilterRuleSerializer',
    'FirewallRuleSettingSerializer',
)


class FirewallRuleSettingSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:firewallrulesetting-detail')

    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FirewallRuleSetting
        fields = (
            'url', 'id', 'display', 'assigned_object_type', 'assigned_object_id', 'assigned_object', 'key', 'value',
            'description', 'comments',
        )
        brief_fields = ('url', 'id', 'display', 'assigned_object', 'key', )

    @extend_schema_field(serializers.JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {'request': self.context['request']}
        return serializer(obj.assigned_object, context=context, nested=True).data


class FirewallFilterRuleSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_routing-api:firewallfilterrule-detail')
    filter = FirewallFilterSerializer(nested=True)
    from_settings = FirewallRuleSettingSerializer(many=True)
    then_settings = FirewallRuleSettingSerializer(many=True)

    class Meta:
        model = FirewallFilterRule
        fields = ('url', 'id', 'display', 'name', 'index', 'filter', 'from_settings', 'then_settings', 'description', 'comments', 'tags')
        brief_fields = ('url', 'id', 'display', 'name', 'index', 'filter', )
