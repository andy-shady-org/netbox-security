from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelForm,
)

from tenancy.forms import TenancyForm, TenancyFilterForm
from ipam.formfields import IPNetworkFormField
from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
)

from ipam.models import IPRange
from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    CustomPrefix,
)

__all__ = (
    "CustomPrefixForm",
    "CustomPrefixFilterForm",
    "CustomPrefixImportForm",
    "CustomPrefixBulkEditForm",
)


class CustomPrefixForm(TenancyForm, PrimaryModelForm):
    prefix = IPNetworkFormField(
        required=False,
        label=_("Custom Prefix"),
        help_text=_("The IP address or prefix value in x.x.x.x/yy format"),
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet(
            "prefix",
            "description",
            name=_("Prefix Parameters"),
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = CustomPrefix
        fields = [
            "prefix",
            "owner",
            "tenant_group",
            "tenant",
            "description",
            "comments",
            "tags",
        ]


class CustomPrefixFilterForm(TenancyFilterForm, PrimaryModelFilterSetForm):
    model = CustomPrefix
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet(
            "prefix",
            name=_("Custom Prefix"),
        ),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    tags = TagFilterField(model)


class CustomPrefixImportForm(PrimaryModelImportForm):
    prefix = forms.CharField(
        max_length=64,
        required=False,
        help_text=_("The IP address or prefix value in x.x.x.x/yy format"),
    )
    description = forms.CharField(max_length=200, required=False)
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )

    class Meta:
        model = CustomPrefix
        fields = (
            "prefix",
            "owner",
            "description",
            "tenant",
            "tags",
        )


class CustomPrefixBulkEditForm(PrimaryModelBulkEditForm):
    model = CustomPrefix
    prefix = forms.CharField(
        max_length=64,
        required=False,
        help_text=_("The IP address or prefix value in x.x.x.x/yy format"),
    )
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
    nullable_fields = ["description", "tenant"]
    fieldsets = (
        FieldSet("prefix", "description"),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
