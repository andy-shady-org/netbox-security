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

from tenancy.models import Tenant

from netbox_security.models import (
    AddressSet,
    AddressSetAssignment,
    Address,
)

__all__ = (
    "AddressSetForm",
    "AddressSetFilterForm",
    "AddressSetImportForm",
    "AddressSetBulkEditForm",
    "AddressSetAssignmentForm",
)


class AddressSetForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    addresses = DynamicModelMultipleChoiceField(
        required=True, label=_("Addresses"), queryset=Address.objects.all()
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet("name", "addresses", "description", name=_("AddressSet List")),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = AddressSet
        fields = [
            "name",
            "addresses",
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
        FieldSet("name", "addresses", name=_("AddressSet List")),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    addresses = DynamicModelMultipleChoiceField(
        required=False, label=_("Addresses"), queryset=Address.objects.all()
    )
    tags = TagFilterField(model)


class AddressSetImportForm(NetBoxModelImportForm):
    addresses = CSVModelMultipleChoiceField(
        queryset=Address.objects.all(),
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
            "addresses",
            "description",
            "tenant",
            "tags",
        )


class AddressSetBulkEditForm(NetBoxModelBulkEditForm):
    model = AddressSet
    description = forms.CharField(max_length=200, required=False)
    tags = TagFilterField(model)
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label=_("Tenant"),
    )
    nullable_fields = []
    fieldsets = (
        FieldSet("name", "description"),
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
