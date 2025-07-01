from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    JSONField,
)
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model
from tenancy.api.serializers import TenantSerializer

from netbox_security.models import AddressSet, AddressSetAssignment
from netbox_security.api.serializers import AddressSerializer
from netbox_security.constants import ADDRESS_ASSIGNMENT_MODELS


class AddressSetSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:addressset-detail"
    )
    addresses = AddressSerializer(
        nested=True, many=True, required=False, read_only=False
    )
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)

    class Meta:
        model = AddressSet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "addresses",
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
            "identifier",
            "addresses",
            "description",
        )

    def create(self, validated_data):
        addresses = validated_data.pop("addresses", None)
        obj = super().create(validated_data)
        if addresses is not None:
            obj.addresses.set(addresses)
        return obj

    def update(self, instance, validated_data):
        addresses = validated_data.pop("addresses", None)
        obj = super().update(instance, validated_data)
        if addresses is not None:
            obj.addresses.set(addresses)
        return obj


class AddressSetAssignmentSerializer(NetBoxModelSerializer):
    address_set = AddressSetSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ADDRESS_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = AddressSetAssignment
        fields = [
            "id",
            "url",
            "display",
            "address_set",
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
            "address_set",
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
