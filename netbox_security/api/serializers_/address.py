from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    IntegerField,
    HyperlinkedIdentityField,
    SerializerMethodField,
    CharField,
)
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer
from tenancy.api.serializers import TenantSerializer
from netbox_security.mixins import GenericAssignmentValidationMixin
from netbox_security.models import Address, AddressAssignment
from netbox_security.constants import (
    ADDRESS_ASSIGNMENT_MODELS,
    ADDRESS_FIELD_ASSIGNMENT_MODELS,
)


class AddressSerializer(GenericAssignmentValidationMixin, PrimaryModelSerializer):
    assignment_models = ADDRESS_FIELD_ASSIGNMENT_MODELS
    assignment_permission = "view"
    allow_empty_assignment = True
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:address-detail"
    )
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ADDRESS_FIELD_ASSIGNMENT_MODELS),
        allow_null=True,
        required=False,
        default=None,
    )
    assigned_object = SerializerMethodField(read_only=True)
    assigned_object_id = IntegerField(allow_null=True, required=False, default=None)
    dns_name = CharField(required=False, allow_null=True)

    class Meta:
        model = Address
        fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "dns_name",
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
            "assigned_object_type",
            "assigned_object_id",
            "dns_name",
            "description",
        )

    def to_internal_value(self, data):
        if isinstance(data, dict) and self.instance is None and not self.nested:
            # Keep dns_name-only creates valid in bulk operations where omitted fields
            # can otherwise be treated as required by per-item validation.
            data = data.copy()
            data.setdefault("assigned_object_type", None)
            data.setdefault("assigned_object_id", None)

        return super().to_internal_value(data)


class AddressAssignmentSerializer(
    GenericAssignmentValidationMixin, NetBoxModelSerializer
):
    assignment_models = ADDRESS_ASSIGNMENT_MODELS
    assignment_permission = "change"
    allow_empty_assignment = False
    address = AddressSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ADDRESS_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = AddressAssignment
        fields = [
            "id",
            "url",
            "display",
            "address",
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
            "address",
            "assigned_object_type",
            "assigned_object_id",
        )
