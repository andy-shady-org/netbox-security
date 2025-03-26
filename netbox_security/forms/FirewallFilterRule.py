from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelFilterSetForm
)

from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CommentField,
)

from netbox_security.models import (
    FirewallFilterRule,
    FirewallFilter,
)

from netbox_security.mixins import FilterRuleFromSettingMixin


__all__ = (
    "FirewallFilterRuleForm",
    "FirewallFilterRuleFilterForm",
)


class FirewallFilterRuleForm(FilterRuleFromSettingMixin, NetBoxModelForm):
    name = forms.CharField(
        max_length=100,
        required=True
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    fieldsets = (
        FieldSet('name', 'filter', 'description', name=_('Firewall Filter Rule')),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = FirewallFilterRule
        fields = ['name', 'filter', ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class FirewallFilterRuleFilterForm(NetBoxModelFilterSetForm):
    filter = DynamicModelMultipleChoiceField(
        queryset=FirewallFilter.objects.all(),
        required=False,
        label=_('Firewall Filter'),
    )
    model = FirewallFilterRule
    fieldsets = (
       FieldSet('q', 'filter_id', 'tag'),
       FieldSet('name', 'filter', 'description', name=_('Firewall Filter Rule')),
    )
    tag = TagFilterField(model)

