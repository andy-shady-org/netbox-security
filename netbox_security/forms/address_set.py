from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)

from tenancy.forms import TenancyForm, TenancyFilterForm
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CommentField,
    CSVModelMultipleChoiceField,
    CSVModelChoiceField,
)
from dcim.models import Device, VirtualDeviceContext
from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    AddressSet,
    AddressSetAssignment,
    Address,
    SecurityZone,
)

__all__ = (
    "AddressSetForm",
    "AddressSetFilterForm",
    "AddressSetImportForm",
    "AddressSetBulkEditForm",
    "AddressSetAssignmentForm",
    "AddressSetAssignmentFilterForm",
)


class AddressSetForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    addresses = DynamicModelMultipleChoiceField(
        required=False,
        label=_("Addresses"),
        quick_add=True,
        queryset=Address.objects.all(),
    )
    address_sets = DynamicModelMultipleChoiceField(
        required=False,
        label=_("Address Sets"),
        quick_add=True,
        queryset=AddressSet.objects.all(),
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet(
            "name",
            "identifier",
            "addresses",
            "address_sets",
            "description",
            name=_("Address Set Parameters"),
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = AddressSet
        fields = [
            "name",
            "identifier",
            "addresses",
            "address_sets",
            "tenant_group",
            "tenant",
            "description",
            "comments",
            "tags",
        ]


class AddressSetFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = AddressSet
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "name",
            "identifier",
            "addresses_id",
            "address_sets_id",
            name=_("AddressSet List"),
        ),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    addresses_id = DynamicModelMultipleChoiceField(
        required=False,
        label=_("Addresses"),
        queryset=Address.objects.all(),
    )
    address_sets_id = DynamicModelMultipleChoiceField(
        required=False,
        label=_("Address Sets"),
        queryset=AddressSet.objects.all(),
    )
    tags = TagFilterField(model)


class AddressSetImportForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=200, required=False)
    addresses = CSVModelMultipleChoiceField(
        queryset=Address.objects.all(),
        to_field_name="name",
        required=False,
    )
    address_sets = CSVModelMultipleChoiceField(
        queryset=AddressSet.objects.all(),
        to_field_name="name",
        required=False,
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )

    class Meta:
        model = AddressSet
        fields = (
            "name",
            "identifier",
            "addresses",
            "address_sets",
            "description",
            "tenant",
            "tags",
        )


class AddressSetBulkEditForm(NetBoxModelBulkEditForm):
    model = AddressSet
    description = forms.CharField(max_length=200, required=False)
    tenant_group = DynamicModelChoiceField(
        queryset=TenantGroup.objects.all(),
        required=False,
        label=_("Tenant Group"),
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_("Tenant"),
    )
    tags = TagFilterField(model)
    nullable_fields = ["description", "tenant"]
    fieldsets = (
        FieldSet("description"),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class AddressSetAssignmentForm(forms.ModelForm):
    address_set = DynamicModelChoiceField(
        label=_("AddressSet"), queryset=AddressSet.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "address_set"),)

    class Meta:
        model = AddressSetAssignment
        fields = ("address_set",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_address_set(self):
        address_set = self.cleaned_data["address_set"]

        conflicting_assignments = AddressSetAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            address_set=address_set,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return address_set


class AddressSetAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = AddressSetAssignment
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "address_set_id",
            name=_("Address Set"),
        ),
        FieldSet(
            "device_id",
            "virtualdevicecontext_id",
            "security_zone_id",
            name="Assignments",
        ),
    )
    address_set_id = DynamicModelMultipleChoiceField(
        queryset=AddressSet.objects.all(),
        required=False,
        label=_("Address Set"),
    )
    device_id = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_("Device"),
    )
    virtualdevicecontext_id = DynamicModelChoiceField(
        queryset=VirtualDeviceContext.objects.all(),
        required=False,
        query_params={"device_id": "$device_id"},
        label=_("Virtual Device Context"),
    )
    security_zone_id = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
        label=_("Security Zone"),
    )
