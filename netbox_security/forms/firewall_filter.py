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
    TagFilterField,
    CommentField,
    CSVChoiceField,
    CSVModelChoiceField,
)

from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    FirewallFilter,
    FirewallFilterAssignment,
)

from netbox_security.choices import FamilyChoices


__all__ = (
    "FirewallFilterForm",
    "FirewallFilterFilterForm",
    "FirewallFilterImportForm",
    "FirewallFilterBulkEditForm",
    "FirewallFilterAssignmentForm",
)


class FirewallFilterForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    family = forms.ChoiceField(
        required=False,
        choices=FamilyChoices,
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet("name", "family", "description", name=_("Firewall Filter Parameters")),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = FirewallFilter
        fields = [
            "name",
            "family",
            "tenant_group",
            "tenant",
            "description",
            "comments",
            "tags",
        ]


class FirewallFilterFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = FirewallFilter
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("name", "family", name=_("Firewall Filter")),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    family = forms.MultipleChoiceField(
        choices=FamilyChoices,
        required=False,
    )
    tags = TagFilterField(model)


class FirewallFilterImportForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(max_length=200, required=False)
    family = CSVChoiceField(
        choices=FamilyChoices,
        help_text=_("Family"),
        required=False,
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )

    class Meta:
        model = FirewallFilter
        fields = (
            "name",
            "family",
            "description",
            "tenant",
            "tags",
        )


class FirewallFilterBulkEditForm(NetBoxModelBulkEditForm):
    model = FirewallFilter
    description = forms.CharField(max_length=200, required=False)
    family = forms.ChoiceField(
        required=False,
        choices=FamilyChoices,
    )
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
        FieldSet("family", "description"),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class FirewallFilterAssignmentForm(forms.ModelForm):
    firewall_filter = DynamicModelChoiceField(
        label=_("Firewall Filter"), queryset=FirewallFilter.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "firewall_filter"),)

    class Meta:
        model = FirewallFilterAssignment
        fields = ("firewall_filter",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_firewall_filter(self):
        firewall_filter = self.cleaned_data["firewall_filter"]

        conflicting_assignments = FirewallFilterAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            firewall_filter=firewall_filter,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return firewall_filter
