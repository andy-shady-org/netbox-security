from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    CSVModelMultipleChoiceField,
    CommentField,
)

from netbox_security.choices import NatTypeChoices, RuleDirectionChoices

from netbox_security.models import (
    NatRuleSet,
    NatRuleSetAssignment,
    SecurityZone,
)


__all__ = (
    "NatRuleSetForm",
    "NatRuleSetFilterForm",
    "NatRuleSetImportForm",
    "NatRuleSetBulkEditForm",
    "NatRuleSetAssignmentForm",
)


class NatRuleSetForm(NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(max_length=200, required=False)
    nat_type = forms.ChoiceField(required=False, choices=NatTypeChoices)
    direction = forms.ChoiceField(required=False, choices=RuleDirectionChoices)
    source_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        quick_add=True,
        required=False,
    )
    destination_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        quick_add=True,
        required=False,
    )
    fieldsets = (
        FieldSet(
            "name",
            "nat_type",
            "description",
            "direction",
            name=_("NAT Rule Set Parameters"),
        ),
        FieldSet("source_zones", "destination_zones", name=_("Security Zones")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = NatRuleSet
        fields = [
            "name",
            "description",
            "nat_type",
            "direction",
            "source_zones",
            "destination_zones",
            "comments",
            "tags",
        ]

    def clean(self):
        super().clean()
        error_message = {}
        if (source_zones := self.cleaned_data.get("source_zones")) is not None and (
            destination_zones := self.cleaned_data.get("destination_zones")
        ) is not None:
            if set(source_zones) & set(destination_zones):
                error_message_mismatch_zones = (
                    "Cannot have the same source and destination zones within a rule"
                )
                error_message["source_zones"] = [error_message_mismatch_zones]
                error_message["destination_zones"] = [error_message_mismatch_zones]
        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class NatRuleSetFilterForm(NetBoxModelFilterSetForm):
    model = NatRuleSet
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "nat_type",
            "direction",
            "source_zones_id",
            "destination_zones_id",
            name="Rule Set Details",
        ),
    )
    nat_type = forms.MultipleChoiceField(
        choices=NatTypeChoices,
        required=False,
    )
    direction = forms.ChoiceField(required=False, choices=RuleDirectionChoices)
    source_zones_id = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        label=_("Source Zones"),
        required=False,
    )
    destination_zones_id = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        label=_("Destination Zones"),
        required=False,
    )
    tags = TagFilterField(model)


class NatRuleSetImportForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(max_length=200, required=False)
    nat_type = CSVChoiceField(
        choices=NatTypeChoices,
        help_text=_("NAT Type"),
        required=False,
    )
    direction = CSVChoiceField(
        choices=RuleDirectionChoices,
        help_text=_("Direction"),
        required=False,
    )
    source_zones = CSVModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        to_field_name="name",
        required=False,
    )
    destination_zones = CSVModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        to_field_name="name",
        required=False,
    )

    class Meta:
        model = NatRuleSet
        fields = (
            "name",
            "description",
            "nat_type",
            "direction",
            "source_zones",
            "destination_zones",
            "tags",
        )

    def clean(self):
        super().clean()
        error_message = {}
        if (source_zones := self.cleaned_data.get("source_zones")) is not None and (
            destination_zones := self.cleaned_data.get("destination_zones")
        ) is not None:
            if set(source_zones) & set(destination_zones):
                error_message_mismatch_zones = (
                    "Cannot have the same source and destination zones within a rule"
                )
                error_message["source_zones"] = [error_message_mismatch_zones]
                error_message["destination_zones"] = [error_message_mismatch_zones]
        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class NatRuleSetBulkEditForm(NetBoxModelBulkEditForm):
    model = NatRuleSet
    description = forms.CharField(max_length=200, required=False)
    nat_type = forms.ChoiceField(required=False, choices=NatTypeChoices)
    direction = forms.ChoiceField(required=False, choices=RuleDirectionChoices)
    source_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    tag = TagFilterField(model)
    nullable_fields = [
        "description",
    ]
    fieldsets = (
        FieldSet("nat_type", "description", "direction"),
        FieldSet("source_zones", "destination_zones", name=_("Security Zones)")),
        FieldSet("tags", name=_("Tags")),
    )


class NatRuleSetAssignmentForm(forms.ModelForm):
    ruleset = DynamicModelChoiceField(
        label=_("NAT Ruleset"), queryset=NatRuleSet.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "ruleset"),)

    class Meta:
        model = NatRuleSetAssignment
        fields = ("ruleset",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_ruleset(self):
        ruleset = self.cleaned_data["ruleset"]

        conflicting_assignments = NatRuleSetAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            ruleset=ruleset,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return ruleset
