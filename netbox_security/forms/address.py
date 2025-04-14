from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)

from tenancy.forms import TenancyForm, TenancyFilterForm
from ipam.formfields import IPNetworkFormField
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
)

from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    Address,
    AddressAssignment,
)

__all__ = (
    "AddressForm",
    "AddressFilterForm",
    "AddressImportForm",
    "AddressBulkEditForm",
    "AddressAssignmentForm",
)


class AddressForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    value = IPNetworkFormField(
        required=True,
        label=_("Value"),
        help_text=_("The IP address or prefix value in x.x.x.x/yy format"),
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet("name", "value", "description", name=_("Address List")),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = Address
        fields = [
            "name",
            "value",
            "tenant_group",
            "tenant",
            "description",
            "comments",
            "tags",
        ]


class AddressFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Address
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("name", "value", name=_("Address List")),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    tags = TagFilterField(model)


class AddressImportForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(max_length=200, required=False)
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )
    value = forms.CharField(
        max_length=64,
        required=True,
        help_text=_("The IP address or prefix value in x.x.x.x/yy format"),
    )

    class Meta:
        model = Address
        fields = (
            "name",
            "value",
            "description",
            "tenant",
            "tags",
        )


class AddressBulkEditForm(NetBoxModelBulkEditForm):
    model = Address
    description = forms.CharField(max_length=200, required=False)
    tags = TagFilterField(model)
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
    value = forms.CharField(
        max_length=64,
        required=False,
        help_text=_("The IP address or prefix value in x.x.x.x/yy format"),
    )
    nullable_fields = ["description", "tenant"]
    fieldsets = (
        FieldSet("value", "description"),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class AddressAssignmentForm(forms.ModelForm):
    address = DynamicModelChoiceField(
        label=_("Address"), queryset=Address.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "address"),)

    class Meta:
        model = AddressAssignment
        fields = ("address",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_address(self):
        address = self.cleaned_data["address"]

        conflicting_assignments = AddressAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            address=address,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return address
