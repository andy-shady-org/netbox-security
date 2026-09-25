from rest_framework.serializers import HyperlinkedIdentityField

from netbox.api.serializers import PrimaryModelSerializer
from ipam.api.serializers import (
    IPAddressSerializer,
    PrefixSerializer,
    IPRangeSerializer,
)
from netbox_security.models import (
    NatPoolMember,
)

from .nat_pool import NatPoolSerializer


class NatPoolMemberSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:natpoolmember-detail"
    )
    pool = NatPoolSerializer(nested=True, required=True, allow_null=False)
    address = IPAddressSerializer(nested=True, required=False, allow_null=True)
    prefix = PrefixSerializer(nested=True, required=False, allow_null=True)
    address_range = IPRangeSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = NatPoolMember
        fields = (
            "id",
            "url",
            "display",
            "name",
            "description",
            "pool",
            "status",
            "address",
            "prefix",
            "address_range",
            "source_ports",
            "destination_ports",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "pool", "status")

    def _sync_related_object_status(self, instance):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user is not None:
            instance.sync_related_object_status(user)

        return instance

    def create(self, validated_data):
        instance = super().create(validated_data)
        return self._sync_related_object_status(instance)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return self._sync_related_object_status(instance)

