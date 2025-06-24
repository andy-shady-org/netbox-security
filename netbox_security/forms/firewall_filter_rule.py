from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
    NetBoxModelImportForm,
)

from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
)

from netbox_security.models import (
    FirewallFilterRule,
    FirewallFilter,
)

from netbox_security.mixins import (
    FilterRuleSettingFormMixin,
)


__all__ = (
    "FirewallFilterRuleForm",
    "FirewallFilterRuleFilterForm",
    "FirewallFilterRuleImportForm",
    "FirewallFilterRuleBulkEditForm",
)


class FirewallFilterRuleForm(FilterRuleSettingFormMixin, NetBoxModelForm):
    name = forms.CharField(max_length=100, required=True)
    index = forms.IntegerField(required=True)
    firewall_filter = DynamicModelChoiceField(
        queryset=FirewallFilter.objects.all(),
        required=True,
        quick_add=True,
        label=_("Firewall Filter"),
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet(
            "name",
            "index",
            "firewall_filter",
            "description",
            name=_("Firewall Filter Rule Parameters"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = FirewallFilterRule
        fields = [
            "name",
            "description",
            "index",
            "firewall_filter",
            "tags",
        ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class FirewallFilterRuleFilterForm(NetBoxModelFilterSetForm):
    firewall_filter_id = DynamicModelMultipleChoiceField(
        queryset=FirewallFilter.objects.all(),
        required=False,
        label=_("Firewall Filter"),
    )
    index = forms.IntegerField(required=False)
    model = FirewallFilterRule
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "name",
            "index",
            "firewall_filter_id",
            "description",
            name=_("Firewall Filter Rule"),
        ),
    )
    tag = TagFilterField(model)


class FirewallFilterRuleImportForm(NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    index = forms.IntegerField(required=True)
    description = forms.CharField(max_length=200, required=False)
    firewall_filter = CSVModelChoiceField(
        queryset=FirewallFilter.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Firewall Filter"),
    )

    class Meta:
        model = FirewallFilterRule
        fields = (
            "name",
            "index",
            "firewall_filter",
            "description",
            "tags",
        )


class FirewallFilterRuleBulkEditForm(NetBoxModelBulkEditForm):
    model = FirewallFilterRule
    index = forms.IntegerField(required=False)
    description = forms.CharField(max_length=200, required=False)
    firewall_filter = DynamicModelChoiceField(
        queryset=FirewallFilter.objects.all(),
        required=False,
        label=_("Firewall Filter"),
    )

    tags = TagFilterField(model)
    nullable_fields = ["description"]
    fieldsets = (
        FieldSet("index", "firewall_filter", "description"),
        FieldSet("tags", name=_("Tags")),
    )
