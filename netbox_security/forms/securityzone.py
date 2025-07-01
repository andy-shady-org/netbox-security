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
    CSVModelChoiceField,
)

from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    SecurityZone,
    SecurityZoneAssignment,
)

__all__ = (
    "SecurityZoneForm",
    "SecurityZoneFilterForm",
    "SecurityZoneImportForm",
    "SecurityZoneBulkEditForm",
    "SecurityZoneAssignmentForm",
)


class SecurityZoneForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet("name", "identifier", "description", name=_("Security Zone")),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = SecurityZone
        fields = [
            "name",
            "identifier",
            "tenant_group",
            "tenant",
            "description",
            "comments",
            "tags",
        ]


class SecurityZoneFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = SecurityZone
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "name",
            "identifier",
        ),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    tags = TagFilterField(model)


class SecurityZoneImportForm(NetBoxModelImportForm):
    identifier = forms.CharField(max_length=100, required=False)
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )

    class Meta:
        model = SecurityZone
        fields = (
            "name",
            "identifier",
            "description",
            "tenant",
            "tags",
        )


class SecurityZoneBulkEditForm(NetBoxModelBulkEditForm):
    model = SecurityZone
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


class SecurityZoneAssignmentForm(forms.ModelForm):
    zone = DynamicModelChoiceField(
        label=_("Security Zone"), queryset=SecurityZone.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "zone"),)

    class Meta:
        model = SecurityZoneAssignment
        fields = ("zone",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_zone(self):
        zone = self.cleaned_data["zone"]

        conflicting_assignments = SecurityZoneAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            zone=zone,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return zone
