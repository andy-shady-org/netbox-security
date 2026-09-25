from netbox_security.mixins import GenericAssignmentValidationMixin
from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer

from netbox_security.models import AddressList, AddressListAssignment
from netbox_security.constants import (
    ADDRESS_ASSIGNMENT_MODELS,
    ADDRESS_LIST_ASSIGNMENT_MODELS,
)


class AddressListSerializer(GenericAssignmentValidationMixin, NetBoxModelSerializer):
    assignment_models = ADDRESS_LIST_ASSIGNMENT_MODELS
    assignment_permission = "view"
    allow_empty_assignment = True
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:addresslist-detail"
    )
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ADDRESS_LIST_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = AddressList
        fields = (
            "id",
            "url",
            "display",
            "name",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "assigned_object_type",
            "assigned_object_id",
        )


class AddressListAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = ADDRESS_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
    address_list = AddressListSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ADDRESS_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = AddressListAssignment
        fields = [
            "id",
            "url",
            "display",
            "address_list",
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
            "address_list",
            "assigned_object_type",
            "assigned_object_id",
        )
