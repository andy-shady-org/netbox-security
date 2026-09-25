from netbox_security.mixins import GenericAssignmentValidationMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import (
    NetBoxModelSerializer,
    WritableNestedSerializer,
    PrimaryModelSerializer,
)
from tenancy.api.serializers import TenantSerializer

from netbox_security.models import AddressSet, AddressSetAssignment
from .address import AddressSerializer
from netbox_security.constants import ADDRESS_ASSIGNMENT_MODELS


class NestedAddressSetSerializer(WritableNestedSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:addressset-detail"
    )

    class Meta:
        model = AddressSet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "addresses",
            "address_sets",
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
            "address_sets",
            "description",
        )


class AddressSetSerializer(PrimaryModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:addressset-detail"
    )
    addresses = AddressSerializer(
        nested=True, many=True, required=False, read_only=False
    )
    address_sets = NestedAddressSetSerializer(
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
            "address_sets",
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
            "address_sets",
            "description",
        )

    def create(self, validated_data):
        addresses = validated_data.pop("addresses", None)
        address_sets = validated_data.pop("address_sets", None)
        obj = super().create(validated_data)
        if addresses is not None:
            obj.addresses.set(addresses)
        if address_sets is not None:
            obj.address_sets.set(address_sets)
        return obj

    def update(self, instance, validated_data):
        addresses = validated_data.pop("addresses", None)
        address_sets = validated_data.pop("address_sets", None)
        obj = super().update(instance, validated_data)
        if addresses is not None:
            obj.addresses.set(addresses)
        if address_sets is not None:
            obj.address_sets.set(address_sets)
        return obj


class AddressSetAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = ADDRESS_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
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
