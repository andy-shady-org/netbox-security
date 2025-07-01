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
    CSVModelMultipleChoiceField,
    DynamicModelMultipleChoiceField,
    CSVMultipleChoiceField,
)

from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    Application,
    ApplicationAssignment,
    ApplicationItem,
)
from netbox_security.choices import ProtocolChoices
from netbox_security.mixins import PortsForm


__all__ = (
    "ApplicationForm",
    "ApplicationFilterForm",
    "ApplicationImportForm",
    "ApplicationBulkEditForm",
    "ApplicationAssignmentForm",
)


class ApplicationForm(PortsForm, TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    application_items = DynamicModelMultipleChoiceField(
        queryset=ApplicationItem.objects.all(),
        required=False,
        quick_add=True,
        help_text=_("A list of Application Items to include in this set."),
    )
    protocol = forms.MultipleChoiceField(
        choices=ProtocolChoices,
        required=False,
    )
    fieldsets = (
        FieldSet(
            "name",
            "identifier",
            "application_items",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
            name=_("Application Parameters"),
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = Application
        fields = [
            "name",
            "identifier",
            "application_items",
            "protocol",
            "destination_ports",
            "source_ports",
            "tenant_group",
            "tenant",
            "description",
            "comments",
            "tags",
        ]


class ApplicationFilterForm(PortsForm, TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Application
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "name",
            "identifier",
            "application_items_id",
            "protocol",
            "destination_ports",
            "source_ports",
            name=_("Application"),
        ),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    application_items_id = DynamicModelMultipleChoiceField(
        queryset=ApplicationItem.objects.all(),
        label=_("Application Items"),
        required=False,
    )
    protocol = forms.MultipleChoiceField(
        choices=ProtocolChoices,
        required=False,
    )
    tags = TagFilterField(model)


class ApplicationImportForm(PortsForm, NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=200, required=False)
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )
    application_items = CSVModelMultipleChoiceField(
        queryset=ApplicationItem.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("An list of Applications Items to include in this set."),
        label=_("Application Items"),
    )
    protocol = CSVMultipleChoiceField(
        choices=ProtocolChoices,
        required=False,
    )

    class Meta:
        model = Application
        fields = (
            "name",
            "identifier",
            "application_items",
            "destination_ports",
            "source_ports",
            "protocol",
            "description",
            "tenant",
            "tags",
        )


class ApplicationBulkEditForm(PortsForm, NetBoxModelBulkEditForm):
    model = Application
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
    application_items = DynamicModelMultipleChoiceField(
        queryset=ApplicationItem.objects.all(),
        required=False,
    )
    protocol = forms.MultipleChoiceField(
        choices=ProtocolChoices,
        required=False,
    )
    nullable_fields = ["description", "tenant"]
    fieldsets = (
        FieldSet(
            "application_items",
            "protocol",
            "source_ports",
            "destination_ports",
            "description",
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class ApplicationAssignmentForm(forms.ModelForm):
    application = DynamicModelChoiceField(
        label=_("Application"), queryset=Application.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "application"),)

    class Meta:
        model = ApplicationAssignment
        fields = ("application",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_application(self):
        application = self.cleaned_data["application"]

        conflicting_assignments = ApplicationAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            application=application,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return application
