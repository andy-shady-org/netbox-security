from rest_framework.serializers import HyperlinkedIdentityField
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers import TenantSerializer
from netbox_security.api.serializers import (
    SecurityZoneSerializer, 
    AddressSerializer,
)
from netbox_security.models import (
    SecurityZonePolicy,
)


class SecurityZonePolicySerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(view_name='plugins-api:netbox_security-api:securityzonepolicy-detail')
    source_zone = SecurityZoneSerializer(nested=True, required=True, allow_null=True)
    destination_zone = SecurityZoneSerializer(nested=True, required=True, allow_null=True)
    source_address = AddressSerializer(nested=True, required=True, allow_null=True)
    destination_address = AddressSerializer(nested=True, required=True, allow_null=True)
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = SecurityZonePolicy
        fields = ('id', 'url', 'display', 'name', 'description', 
                  'source_zone', 'source_address', 'destination_zone', 'destination_address', 
                  'application', 'tenant', 'comments', 'tags', 'custom_fields', 
                  'created', 'last_updated')
        brief_fields = ('id', 'url', 'display', 'name', 'description',
                        'source_zone', 'source_address', 'destination_zone', 'destination_address', 
                        'application')
