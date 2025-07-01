from django import forms
from django.utils.translation import gettext_lazy as _

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
    CSVMultipleChoiceField,
)

from netbox_security.models import (
    SecurityZonePolicy,
    SecurityZone,
    AddressList,
    Application,
    ApplicationSet,
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
    identifier = forms.CharField(max_length=100, required=False)
    index = forms.IntegerField(required=True)
    description = forms.CharField(max_length=200, required=False)
    source_zone = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
        quick_add=True,
        required=True,
    )
    destination_zone = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
        quick_add=True,
        required=True,
    )
    source_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        quick_add=True,
        required=False,
    )
    destination_address = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        quick_add=True,
        required=False,
    )
    applications = DynamicModelMultipleChoiceField(
        queryset=Application.objects.all(),
        quick_add=True,
        required=False,
    )
    application_sets = DynamicModelMultipleChoiceField(
        queryset=ApplicationSet.objects.all(),
        quick_add=True,
        required=False,
    )
    policy_actions = forms.MultipleChoiceField(
        choices=ActionChoices,
        required=True,
    )
    fieldsets = (
        FieldSet(
            "name", "identifier", "index", "description", name=_("Security Zone Policy")
        ),
        FieldSet("source_zone", "source_address", name=_("Source Assignment")),
        FieldSet(
            "destination_zone", "destination_address", name=_("Destination Assignment")
        ),
        FieldSet("applications", "application_sets", name=_("Applications")),
        FieldSet("policy_actions", name=_("Policy Actions")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = SecurityZonePolicy
        fields = [
            "name",
            "identifier",
            "index",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "applications",
            "application_sets",
            "policy_actions",
            "description",
            "comments",
            "tags",
        ]

    def clean(self):
        super().clean()
        error_message = {}
        if (source_zone := self.cleaned_data.get("source_zone")) is not None and (
            destination_zone := self.cleaned_data.get("destination_zone")
        ) is not None:
            if source_zone == destination_zone:
                error_message_mismatch_zones = (
                    "Cannot have the same source and destination zone within a policy"
                )
                error_message["source_zone"] = [error_message_mismatch_zones]
                error_message["destination_zone"] = [error_message_mismatch_zones]
        if (source_address := self.cleaned_data.get("source_address")) is not None and (
            destination_address := self.cleaned_data.get("destination_address")
        ) is not None:
            if set(source_address) & set(destination_address):
                error_message_mismatch_zones = "Cannot have the same source and destination addresses within a policy"
                error_message["source_address"] = [error_message_mismatch_zones]
                error_message["destination_address"] = [error_message_mismatch_zones]
        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class SecurityZonePolicyFilterForm(NetBoxModelFilterSetForm):
    model = SecurityZonePolicy
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("name", "identifier", "index"),
        FieldSet(
            "source_zone_id",
            "source_address_id",
            "destination_zone_id",
            "destination_address_id",
            "applications_id",
            "application_sets_id",
            name=_("Source/Destination Assignment"),
        ),
        FieldSet("policy_actions", name=_("Policy Actions")),
    )
    index = forms.IntegerField(required=False)
    source_zone_id = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        label=_("Source Zone"),
        required=False,
    )
    destination_zone_id = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        label=_("Destination Zone"),
        required=False,
    )
    source_address_id = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        label=_("Source Address"),
        required=False,
    )
    destination_address_id = DynamicModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        label=_("Destination Address"),
        required=False,
    )
    applications_id = DynamicModelMultipleChoiceField(
        queryset=Application.objects.all(),
        label=_("Applications"),
        required=False,
    )
    application_sets_id = DynamicModelMultipleChoiceField(
        queryset=ApplicationSet.objects.all(),
        label=_("Application Sets"),
        required=False,
    )
    policy_actions = forms.MultipleChoiceField(
        choices=ActionChoices,
        required=True,
    )
    tags = TagFilterField(model)


class SecurityZonePolicyImportForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=100, required=True)
    identifier = forms.CharField(max_length=100, required=False)
    index = forms.IntegerField(
        required=True,
        label=_("Index"),
    )
    source_zone = CSVModelChoiceField(
        queryset=SecurityZone.objects.all(),
        to_field_name="name",
        required=True,
    )
    destination_zone = CSVModelChoiceField(
        queryset=SecurityZone.objects.all(),
        to_field_name="name",
        required=True,
    )
    source_address = CSVModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        to_field_name="name",
        required=False,
    )
    destination_address = CSVModelMultipleChoiceField(
        queryset=AddressList.objects.all(),
        to_field_name="name",
        required=False,
    )
    applications = CSVModelMultipleChoiceField(
        queryset=Application.objects.all(),
        to_field_name="name",
        required=False,
    )
    application_sets = CSVModelMultipleChoiceField(
        queryset=ApplicationSet.objects.all(),
        to_field_name="name",
        required=False,
    )
    policy_actions = CSVMultipleChoiceField(
        choices=ActionChoices,
        required=True,
    )

    class Meta:
        model = SecurityZonePolicy
        fields = (
            "name",
            "identifier",
            "index",
            "description",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "applications",
            "application_sets",
            "policy_actions",
            "tags",
        )

    def clean(self):
        super().clean()
        error_message = {}
        if (source_zone := self.cleaned_data.get("source_zone")) is not None and (
            destination_zone := self.cleaned_data.get("destination_zone")
        ) is not None:
            if source_zone == destination_zone:
                error_message_mismatch_zones = (
                    "Cannot have the same source and destination zone within a policy"
                )
                error_message["source_zone"] = [error_message_mismatch_zones]
                error_message["destination_zone"] = [error_message_mismatch_zones]
        if (source_address := self.cleaned_data.get("source_address")) is not None and (
            destination_address := self.cleaned_data.get("destination_address")
        ) is not None:
            if set(source_address) & set(destination_address):
                error_message_mismatch_zones = "Cannot have the same source and destination addresses within a policy"
                error_message["source_address"] = [error_message_mismatch_zones]
                error_message["destination_address"] = [error_message_mismatch_zones]
        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


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
    applications = DynamicModelMultipleChoiceField(
        queryset=Application.objects.all(),
        required=False,
    )
    application_sets = DynamicModelMultipleChoiceField(
        queryset=ApplicationSet.objects.all(),
        required=False,
    )
    description = forms.CharField(max_length=200, required=False)
    tags = TagFilterField(model)
    nullable_fields = ["description"]
    fieldsets = (
        FieldSet("description"),
        FieldSet("source_zone", "destination_zone", name="Security Zones"),
        FieldSet("source_address", "destination_address", name="Address Lists"),
        FieldSet("applications", "application_sets", name="Applications"),
        FieldSet("tags", name=_("Tags")),
    )
