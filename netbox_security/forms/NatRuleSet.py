from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm
)
from utilities.forms.rendering import FieldSet,  ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    CSVModelMultipleChoiceField,
    CommentField,
)

from netbox_security.choices import (
    NatTypeChoices, RuleDirectionChoices
)

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
    name = forms.CharField(
        max_length=64,
        required=True
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    nat_type = forms.ChoiceField(
        required=True,
        choices=NatTypeChoices,
        widget=forms.Select()
    )
    direction = forms.ChoiceField(
        required=True,
        choices=RuleDirectionChoices,
        widget=forms.Select()
    )
    source_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    fieldsets = (
        FieldSet('name', 'nat_type', 'description', 'direction'),
        FieldSet('source_zones', 'destination_zones', name=_('Security Zones)')),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = NatRuleSet
        fields = ['name', 'description', 'nat_type', 'direction',
                  'source_zones', 'destination_zones', 'comments', 'tags']

    def clean(self):
        super().clean()
        error_message = {}
        source_zones = self.cleaned_data.get("source_zones")
        destination_zones = self.cleaned_data.get("destination_zones")
        if set(source_zones) & set(destination_zones):
            error_message_mismatch_zones = f'Cannot have the same source and destination zones within a rule'
            error_message["source_zones"] = [error_message_mismatch_zones]
            error_message["destination_zones"] = [error_message_mismatch_zones]
        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class NatRuleSetFilterForm(NetBoxModelFilterSetForm):
    model = NatRuleSet
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("nat_type", "direction", "source_zones", "destination_zones", name="Rule Set Details"),
    )
    nat_type = forms.MultipleChoiceField(
        choices=NatTypeChoices,
        required=False,
    )
    direction = forms.ChoiceField(
        required=False,
        choices=RuleDirectionChoices,
        widget=forms.Select()
    )
    source_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    tags = TagFilterField(model)


class NatRuleSetImportForm(NetBoxModelImportForm):
    nat_type = CSVChoiceField(
        choices=NatTypeChoices,
        help_text=_('NAT Type')
    )
    direction = CSVChoiceField(
        choices=RuleDirectionChoices,
        help_text=_('Direction')
    )
    source_zones = CSVModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zones = CSVModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )

    class Meta:
        model = NatRuleSet
        fields = ("name", "nat_type", "direction", "source_zones", "destination_zones", "tags")


class NatRuleSetBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(
        max_length=200,
        required=False
    )
    nat_type = forms.ChoiceField(
        required=False,
        choices=NatTypeChoices,
        widget=forms.Select()
    )
    direction = forms.ChoiceField(
        required=False,
        choices=RuleDirectionChoices,
        widget=forms.Select()
    )
    source_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    destination_zones = DynamicModelMultipleChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
    )
    tag = TagFilterField(NatRuleSet)

    model = NatRuleSet
    nullable_fields = [
       'description',
    ]
    fieldsets = (
        FieldSet('nat_type', 'description', 'direction'),
        FieldSet('source_zones', 'destination_zones', name=_('Security Zones)')),
        FieldSet("tags", name=_("Tags")),
    )


class NatRuleSetAssignmentForm(forms.ModelForm):
    ruleset = DynamicModelChoiceField(
        label=_('NAT Ruleset'),
        queryset=NatRuleSet.objects.all()
    )

    fieldsets = (
        FieldSet(ObjectAttribute('assigned_object'), 'ruleset'),
    )

    class Meta:
        model = NatRuleSetAssignment
        fields = ('ruleset',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_ruleset(self):
        ruleset = self.cleaned_data['ruleset']

        conflicting_assignments = NatRuleSetAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            ruleset=ruleset
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(id=self.instance.id)

        if conflicting_assignments.exists():
            raise forms.ValidationError(
                _('Assignment already exists')
            )

        return ruleset
