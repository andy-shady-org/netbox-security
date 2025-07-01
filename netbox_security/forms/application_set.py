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
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
)

from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    ApplicationSet,
    ApplicationSetAssignment,
    Application,
)

__all__ = (
    "ApplicationSetForm",
    "ApplicationSetFilterForm",
    "ApplicationSetImportForm",
    "ApplicationSetBulkEditForm",
    "ApplicationSetAssignmentForm",
)


class ApplicationSetForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    applications = DynamicModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=True,
        quick_add=True,
        help_text=_("A list of applications to include in this set."),
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet(
            "name",
            "identifier",
            "applications",
            "description",
            name=_("Application Set Parameters"),
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = ApplicationSet
        fields = [
            "name",
            "identifier",
            "applications",
            "tenant_group",
            "tenant",
            "description",
            "comments",
            "tags",
        ]


class ApplicationSetFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = ApplicationSet
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("name", "identifier", "applications_id", name=_("Application Set")),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    applications_id = DynamicModelMultipleChoiceField(
        queryset=Application.objects.all(),
        label=_("Applications"),
        required=False,
    )
    tags = TagFilterField(model)


class ApplicationSetImportForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=200, required=False)
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )
    applications = CSVModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=True,
        to_field_name="name",
        help_text=_("An list of applications to include in this set."),
    )

    class Meta:
        model = ApplicationSet
        fields = (
            "name",
            "identifier",
            "applications",
            "description",
            "tenant",
            "tags",
        )


class ApplicationSetBulkEditForm(NetBoxModelBulkEditForm):
    model = ApplicationSet
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
    applications = DynamicModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=False,
        help_text=_("A list of applications to include in this set."),
    )
    nullable_fields = ["description", "tenant"]
    fieldsets = (
        FieldSet("applications", "description"),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class ApplicationSetAssignmentForm(forms.ModelForm):
    application_set = DynamicModelChoiceField(
        label=_("Application Set"), queryset=ApplicationSet.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "application_set"),)

    class Meta:
        model = ApplicationSetAssignment
        fields = ("application_set",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_application_set(self):
        application_set = self.cleaned_data["application_set"]

        conflicting_assignments = ApplicationSetAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            application_set=application_set,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return application_set
