from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)
from ipam.models import IPAddress, Prefix, IPRange

from utilities.forms.rendering import FieldSet, ObjectAttribute, TabbedGroups
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    CSVModelChoiceField,
    CSVModelMultipleChoiceField,
    CommentField,
)

from netbox_security.choices import (
    RuleStatusChoices,
    AddressTypeChoices,
    CustomInterfaceChoices,
)

from netbox_security.models import (
    NatPool,
    NatRuleSet,
    NatRule,
    NatRuleAssignment,
)
from netbox_security.mixins import PortsForm


__all__ = (
    "NatRuleForm",
    "NatRuleFilterForm",
    "NatRuleImportForm",
    "NatRuleBulkEditForm",
    "NatRuleAssignmentForm",
)


class NatRuleForm(PortsForm, NetBoxModelForm):
    rule_set = DynamicModelChoiceField(
        queryset=NatRuleSet.objects.all(),
        quick_add=True,
        required=True,
    )
    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(max_length=200, required=False)
    status = forms.ChoiceField(required=False, choices=RuleStatusChoices)
    source_type = forms.ChoiceField(required=False, choices=AddressTypeChoices)
    destination_type = forms.ChoiceField(required=False, choices=AddressTypeChoices)
    custom_interface = forms.ChoiceField(
        required=False,
        choices=CustomInterfaceChoices,
        widget=forms.Select(),
        help_text=_("Standard Interface assignment via Device -> Interface view"),
    )
    source_addresses = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        quick_add=True,
        required=False,
    )
    destination_addresses = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        quick_add=True,
        required=False,
    )
    source_prefixes = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        quick_add=True,
        required=False,
    )
    destination_prefixes = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        quick_add=True,
        required=False,
    )
    source_ranges = DynamicModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        quick_add=True,
        required=False,
    )
    destination_ranges = DynamicModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        quick_add=True,
        required=False,
    )
    source_pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        quick_add=True,
        required=False,
    )
    destination_pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        quick_add=True,
        required=False,
    )
    pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        quick_add=True,
        required=False,
    )
    fieldsets = (
        FieldSet("name", "rule_set", "status", "description", name=_("Rule")),
        FieldSet(
            "source_type", "destination_type", name=_("Source/Destination Address Type")
        ),
        FieldSet(
            TabbedGroups(
                FieldSet(
                    "source_addresses", "destination_addresses", name=_("IP Address")
                ),
                FieldSet("source_prefixes", "destination_prefixes", name=_("Prefix")),
                FieldSet("source_ranges", "destination_ranges", name=_("IP Range")),
                FieldSet("source_pool", "destination_pool", name=_("Pool")),
            ),
            name=_("Source/Destination Assignment"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("pool", name=_("NAT Pool")),
                FieldSet("custom_interface", name=_("Custom Interface")),
            ),
            name=_("Outbound Assignment"),
        ),
        FieldSet(
            "source_ports", "destination_ports", name=_("Source/Destination Ports")
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = NatRule
        fields = [
            "rule_set",
            "name",
            "description",
            "status",
            "source_type",
            "destination_type",
            "source_addresses",
            "destination_addresses",
            "source_prefixes",
            "destination_prefixes",
            "source_pool",
            "destination_pool",
            "source_ranges",
            "destination_ranges",
            "source_ports",
            "destination_ports",
            "pool",
            "comments",
            "tags",
        ]

    def clean(self):
        super().clean()
        error_message = {}
        if (
            source_addresses := self.cleaned_data.get("source_addresses")
        ) is not None and (
            destination_addresses := self.cleaned_data.get("destination_addresses")
        ):
            if set(destination_addresses) & set(source_addresses):
                error_address_entry = f"Source and Destination addresses cannot match: {source_addresses} - {destination_addresses}"
                error_message |= {
                    "destination_addresses": [error_address_entry],
                    "source_addresses": [error_address_entry],
                }

        if (
            source_prefixes := self.cleaned_data.get("source_prefixes")
        ) is not None and (
            destination_prefixes := self.cleaned_data.get("destination_prefixes")
        ):
            if set(destination_prefixes) & set(source_prefixes):
                error_prefix_entry = "Source and Destination prefixes cannot match."
                error_message |= {
                    "destination_prefixes": [error_prefix_entry],
                    "source_prefixes": [error_prefix_entry],
                }

        if (source_ranges := self.cleaned_data.get("source_ranges")) is not None and (
            destination_ranges := self.cleaned_data.get("destination_ranges")
        ):
            if set(destination_ranges) & set(source_ranges):
                error_prefix_entry = "Source and Destination ranges cannot match."
                error_message |= {
                    "destination_ranges": [error_prefix_entry],
                    "source_ranges": [error_prefix_entry],
                }

        if (source_pool := self.cleaned_data.get("source_pool")) is not None and (
            destination_pool := self.cleaned_data.get("destination_pool")
        ):
            if destination_pool == source_pool:
                error_prefix_entry = "Source and Destination pools cannot match."
                error_message |= {
                    "destination_pool": [error_prefix_entry],
                    "source_pool": [error_prefix_entry],
                }

        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class NatRuleFilterForm(PortsForm, NetBoxModelFilterSetForm):
    model = NatRule
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("name", "rule_set_id", "status", "description", name=_("Rule")),
        FieldSet(
            "source_addresses_id",
            "source_prefixes_id",
            "source_ranges_id",
            "source_ports",
            "source_type",
            "source_pool_id",
            name=_("Sources"),
        ),
        FieldSet(
            "destination_addresses_id",
            "destination_prefixes_id",
            "destination_ranges_id",
            "destination_ports",
            "destination_type",
            "destination_pool_id",
            name=_("Destinations"),
        ),
        FieldSet("pool_id", "custom_interface", name=_("Outbound)")),
    )
    rule_set_id = DynamicModelMultipleChoiceField(
        queryset=NatRuleSet.objects.all(),
        label=_("NAT Rule Set"),
        required=False,
    )
    status = forms.MultipleChoiceField(
        choices=RuleStatusChoices, required=False, widget=forms.Select()
    )
    source_addresses_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        label=_("Source Addresses"),
        required=False,
    )
    source_prefixes_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        label=_("Source Prefixes"),
        required=False,
    )
    source_ranges_id = DynamicModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        label=_("Source IP Ranges"),
        required=False,
    )
    source_pool_id = DynamicModelMultipleChoiceField(
        queryset=NatPool.objects.all(),
        label=_("Source NAT Pool"),
        required=False,
    )
    source_type = forms.MultipleChoiceField(
        choices=AddressTypeChoices,
        required=False,
        widget=forms.Select(),
    )
    destination_addresses_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        label=_("Destination Addresses"),
        required=False,
    )
    destination_prefixes_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        label=_("Destination Prefixes"),
        required=False,
    )
    destination_ranges_id = DynamicModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        label=_("Destination Ranges"),
        required=False,
    )
    destination_type = forms.MultipleChoiceField(
        choices=AddressTypeChoices,
        required=False,
        widget=forms.Select(),
    )
    destination_pool_id = DynamicModelMultipleChoiceField(
        queryset=NatPool.objects.all(),
        label=_("Destination Pool"),
        required=False,
    )
    pool_id = DynamicModelMultipleChoiceField(
        queryset=NatPool.objects.all(),
        label=_("NAT Pool"),
        required=False,
    )
    custom_interface = forms.MultipleChoiceField(
        choices=CustomInterfaceChoices, required=False, widget=forms.Select()
    )
    tags = TagFilterField(model)


class NatRuleImportForm(PortsForm, NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    rule_set = CSVModelChoiceField(
        queryset=NatRuleSet.objects.all(),
        required=True,
        to_field_name="name",
        help_text=_("NAT Ruleset (Name)"),
    )
    status = CSVChoiceField(choices=RuleStatusChoices, help_text=_("Status"))
    source_type = CSVChoiceField(
        choices=AddressTypeChoices, required=False, help_text=_("Source Type")
    )
    destination_type = CSVChoiceField(
        choices=AddressTypeChoices, required=False, help_text=_("Destination Type")
    )
    custom_interface = CSVChoiceField(
        required=False,
        choices=CustomInterfaceChoices,
        widget=forms.Select(),
        help_text=_("Standard Interface assignment via Device -> Interface view"),
    )
    source_addresses = CSVModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
    )
    destination_addresses = CSVModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
    )
    source_prefixes = CSVModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
    )
    destination_prefixes = CSVModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
    )
    source_ranges = CSVModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        required=False,
    )
    destination_ranges = CSVModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        required=False,
    )
    source_pool = CSVModelChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
    )
    destination_pool = CSVModelChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
    )
    pool = CSVModelChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
    )

    class Meta:
        model = NatRule
        fields = (
            "name",
            "rule_set",
            "status",
            "description",
            "source_type",
            "destination_type",
            "source_addresses",
            "destination_addresses",
            "source_prefixes",
            "destination_prefixes",
            "source_pool",
            "destination_pool",
            "source_ranges",
            "destination_ranges",
            "source_ports",
            "destination_ports",
            "pool",
            "tags",
        )

    def clean(self):
        super().clean()
        error_message = {}
        if (
            source_addresses := self.cleaned_data.get("source_addresses")
        ) is not None and (
            destination_addresses := self.cleaned_data.get("destination_addresses")
        ):
            if set(destination_addresses) & set(source_addresses):
                error_address_entry = f"Source and Destination addresses cannot match: {source_addresses} - {destination_addresses}"
                error_message |= {
                    "destination_addresses": [error_address_entry],
                    "source_addresses": [error_address_entry],
                }

        if (
            source_prefixes := self.cleaned_data.get("source_prefixes")
        ) is not None and (
            destination_prefixes := self.cleaned_data.get("destination_prefixes")
        ):
            if set(destination_prefixes) & set(source_prefixes):
                error_prefix_entry = "Source and Destination prefixes cannot match."
                error_message |= {
                    "destination_prefixes": [error_prefix_entry],
                    "source_prefixes": [error_prefix_entry],
                }

        if (source_ranges := self.cleaned_data.get("source_ranges")) is not None and (
            destination_ranges := self.cleaned_data.get("destination_ranges")
        ):
            if set(destination_ranges) & set(source_ranges):
                error_prefix_entry = "Source and Destination ranges cannot match."
                error_message |= {
                    "destination_ranges": [error_prefix_entry],
                    "source_ranges": [error_prefix_entry],
                }

        if (source_pool := self.cleaned_data.get("source_pool")) is not None and (
            destination_pool := self.cleaned_data.get("destination_pool")
        ):
            if destination_pool == source_pool:
                error_prefix_entry = "Source and Destination pools cannot match."
                error_message |= {
                    "destination_pool": [error_prefix_entry],
                    "source_pool": [error_prefix_entry],
                }

        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class NatRuleBulkEditForm(PortsForm, NetBoxModelBulkEditForm):
    model = NatRule
    rule_set = DynamicModelMultipleChoiceField(
        queryset=NatRuleSet.objects.all(), required=False
    )
    description = forms.CharField(max_length=200, required=False)
    source_type = forms.ChoiceField(required=False, choices=AddressTypeChoices)
    destination_type = forms.ChoiceField(required=False, choices=AddressTypeChoices)
    source_pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
    )
    destination_pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
    )
    pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
    )
    tags = TagFilterField(model)
    nullable_fields = [
        "description",
    ]
    fieldsets = (
        FieldSet(
            "rule_set",
            "description",
            "source_type",
            "destination_type",
            "source_pool",
            "destination_pool",
            "source_ports",
            "destination_ports",
            "pool",
        ),
        FieldSet("tags", name=_("Tags")),
    )


class NatRuleAssignmentForm(forms.ModelForm):
    rule = DynamicModelChoiceField(label=_("NAT Rule"), queryset=NatRule.objects.all())

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "rule"),)

    class Meta:
        model = NatRuleAssignment
        fields = ("rule",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_rule(self):
        rule = self.cleaned_data["rule"]

        conflicting_assignments = NatRuleAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            rule=rule,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return rule
