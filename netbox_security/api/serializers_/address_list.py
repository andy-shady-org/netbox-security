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

from netbox_security.models import AddressList, AddressListAssignment
from netbox_security.constants import (
    ADDRESS_ASSIGNMENT_MODELS,
    ADDRESS_LIST_ASSIGNMENT_MODELS,
)


class AddressListSerializer(NetBoxModelSerializer):
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

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data


class AddressListAssignmentSerializer(NetBoxModelSerializer):
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

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data
