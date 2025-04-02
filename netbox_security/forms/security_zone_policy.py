from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.forms import SimpleArrayField

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)

from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    CSVModelMultipleChoiceField,
    CSVModelChoiceField,
    TagFilterField,
    CommentField,
)

from tenancy.models import Tenant

from netbox_security.models import (
    SecurityZonePolicy,
    SecurityZone,
    AddressList,
)

from netbox_security.choices import ActionChoices


__all__ = (
    "SecurityZonePolicyForm",
    "SecurityZonePolicyFilterForm",
    "SecurityZonePolicyImportForm",
    "SecurityZonePolicyBulkEditForm",
)


class SecurityZonePolicyForm(NetBoxModelForm):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=200, required=False)
    source_zone = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
    )
    destination_zone = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
    )
    source_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
    )
    destination_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
    )
    application = SimpleArrayField(
        forms.CharField(max_length=50),
        help_text=_("Comma-separated list of applications."),
        required=True,
    )
    actions = forms.MultipleChoiceField(
        choices=ActionChoices,
        required=True,
    )
    fieldsets = (
        FieldSet("name", "index", "description", name=_("Security Zone Policy")),
        FieldSet("source_zone", "source_address", name=_("Source Assignment")),
        FieldSet(
            "destination_zone", "destination_address", name=_("Destination Assignment")
        ),
        FieldSet("application", name=_("Application")),
        FieldSet("actions", name=_("Actions")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = SecurityZonePolicy
        fields = [
            "name",
            "index",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "application",
            "actions",
            "description",
            "comments",
            "tags",
        ]

    def clean(self):
        super().clean()
        error_message = {}
        source_zone = self.cleaned_data.get("source_zone")
        destination_zone = self.cleaned_data.get("destination_zone")
        source_address = self.cleaned_data.get("source_address")
        destination_address = self.cleaned_data.get("destination_address")
        if source_zone == destination_zone:
            error_message_mismatch_zones = (
                "Cannot have the same source and destination zone within a policy"
            )
            error_message["source_zone"] = [error_message_mismatch_zones]
            error_message["destination_zone"] = [error_message_mismatch_zones]
        if set(source_address) & set(destination_address):
            error_message_mismatch_zones = (
                "Cannot have the same source and destination addresses within a policy"
            )
            error_message["source_address"] = [error_message_mismatch_zones]
            error_message["destination_address"] = [error_message_mismatch_zones]
        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class SecurityZonePolicyFilterForm(NetBoxModelFilterSetForm):
    model = SecurityZonePolicy
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("name", "index"),
        FieldSet(
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            name=_("Source/Destination Assignment"),
        ),
        FieldSet("actions", name=_("Actions")),
    )
    index = forms.IntegerField(required=False)
    source_zone = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zone = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    source_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        required=False,
    )
    destination_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        required=False,
    )
    actions = forms.MultipleChoiceField(
        choices=ActionChoices,
        required=True,
    )
    tags = TagFilterField(model)


class SecurityZonePolicyImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
    )
    source_zone = CSVModelChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zone = CSVModelChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    source_address = CSVModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        required=False,
    )
    destination_address = CSVModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        required=False,
    )

    class Meta:
        model = SecurityZonePolicy
        fields = (
            "name",
            "index",
            "description",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "application",
            "tenant",
            "tags",
        )


class SecurityZonePolicyBulkEditForm(NetBoxModelBulkEditForm):
    model = SecurityZonePolicy
    source_zone = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zone = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    source_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        required=False,
    )
    destination_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        required=False,
    )
    description = forms.CharField(max_length=200, required=False)
    tags = TagFilterField(model)
    nullable_fields = ["description"]
    fieldsets = (
        FieldSet("description"),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
