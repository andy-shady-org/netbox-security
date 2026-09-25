from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from typing import cast

from netbox.forms import (
    PrimaryModelBulkEditForm,
    PrimaryModelFilterSetForm,
    PrimaryModelImportForm,
    PrimaryModelForm,
)
from netaddr import IPNetwork
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    CSVModelChoiceField,
    CommentField,
)
from ipam.choices import IPAddressStatusChoices
from ipam.models import IPAddress, Prefix, IPRange, VRF
from tenancy.models import Tenant

from netbox_security.models import NatPool, NatPoolMember
from netbox_security.mixins import PortsForm

__all__ = (
    "NatPoolMemberForm",
    "NatPoolMemberFilterForm",
    "NatPoolMemberImportForm",
    "NatPoolMemberBulkEditForm",
)


class NatPoolMemberForm(PortsForm, PrimaryModelForm):
    request_user = None
    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(max_length=200, required=False)
    pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        quick_add=True,
        required=True,
    )
    status = forms.ChoiceField(choices=IPAddressStatusChoices)
    address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        quick_add=True,
    )
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        quick_add=True,
        required=False,
    )
    address_range = DynamicModelChoiceField(
        queryset=IPRange.objects.all(),
        quick_add=True,
        required=False,
    )
    fieldsets = (
        FieldSet("name", "status"),
        FieldSet("pool", name=_("Nat Pool")),
        FieldSet(
            TabbedGroups(
                FieldSet("address", name=_("IP Address")),
                FieldSet("prefix", name=_("Prefix")),
                FieldSet("address_range", name=_("IP Range")),
            ),
            name=_("Pool Prefix/Address/Range"),
        ),
        FieldSet(
            "source_ports", "destination_ports", name=_("Source/Destination Ports")
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = NatPoolMember
        fields = [
            "name",
            "owner",
            "pool",
            "status",
            "address",
            "prefix",
            "address_range",
            "description",
            "source_ports",
            "destination_ports",
            "comments",
            "tags",
        ]

    def save(self, *args, **kwargs):
        if self.request_user is not None:
            self.instance._status_sync_user = self.request_user
        return super().save(*args, **kwargs)


class NatPoolMemberFilterForm(PortsForm, PrimaryModelFilterSetForm):
    model = NatPoolMember
    fieldsets = (
        FieldSet("q", "filter_id", "tag", "owner_id"),
        FieldSet("name", "pool_id", "pool_type", "status"),
        FieldSet("address_id", "prefix_id", "address_range_id", name=_("IPAM")),
        FieldSet("source_ports", "destination_ports", name=_("Ports")),
    )
    status = forms.MultipleChoiceField(
        choices=IPAddressStatusChoices,
        required=False,
    )
    pool_id = DynamicModelMultipleChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
        label=_("NAT Pool"),
    )
    address_id = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
        label=_("Address"),
        required=False,
    )
    prefix_id = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        label=_("Prefix"),
        required=False,
    )
    address_range_id = DynamicModelMultipleChoiceField(
        queryset=IPRange.objects.all(),
        label=_("Address Range"),
        required=False,
    )
    tags = TagFilterField(model)


class NatPoolMemberImportForm(PortsForm, PrimaryModelImportForm):
    request_user = None
    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(max_length=200, required=False)
    vrf = CSVModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Optional VRF used to disambiguate text lookups"),
    )
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Optional tenant used to disambiguate text lookups"),
    )
    pool = CSVModelChoiceField(
        queryset=NatPool.objects.all(),
        required=True,
        to_field_name="name",
        help_text=_("NAT Pool (Name)"),
    )
    address = CSVModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
        to_field_name="address",
        help_text=_("IP Address"),
    )
    prefix = CSVModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        to_field_name="prefix",
        help_text=_("Prefix"),
    )
    address_range_end = forms.CharField(
        required=False,
        help_text=_("Ending address for an IP range (used to disambiguate ranges)"),
    )
    address_range = CSVModelChoiceField(
        queryset=IPRange.objects.all(),
        required=False,
        to_field_name="start_address",
        help_text=_("IPv4 or IPv6 start address (with mask)"),
    )
    status = CSVChoiceField(choices=IPAddressStatusChoices, help_text=_("Status"))

    @staticmethod
    def _scope_filters_from_data(data):
        vrf = data.get("vrf")
        tenant = data.get("tenant")

        if vrf and tenant:
            return {"vrf__name": vrf, "tenant__name": tenant}
        if vrf:
            return {"vrf__name": vrf}
        if tenant:
            return {"tenant__name": tenant}
        return {"vrf__isnull": True, "tenant__isnull": True}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.data:
            return

        scope_filters = self._scope_filters_from_data(self.data)
        address_field = cast(CSVModelChoiceField, self.fields["address"])
        prefix_field = cast(CSVModelChoiceField, self.fields["prefix"])
        address_range_field = cast(CSVModelChoiceField, self.fields["address_range"])

        if address := self.data.get("address"):
            address_field.queryset = IPAddress.objects.filter(
                address=address,
                **scope_filters,
            )
        if prefix := self.data.get("prefix"):
            prefix_field.queryset = Prefix.objects.filter(
                prefix=prefix,
                **scope_filters,
            )
        if address_range := self.data.get("address_range"):
            queryset = IPRange.objects.filter(
                start_address=address_range,
                **scope_filters,
            )
            if address_range_end := self.data.get("address_range_end"):
                try:
                    queryset = queryset.filter(
                        end_address=str(IPNetwork(str(address_range_end)))
                    )
                except Exception:
                    pass
            address_range_field.queryset = queryset

    class Meta:
        model = NatPoolMember
        fields = (
            "name",
            "owner",
            "pool",
            "vrf",
            "tenant",
            "status",
            "address",
            "prefix",
            "address_range",
            "address_range_end",
            "source_ports",
            "destination_ports",
            "tags",
        )

    def clean_address_range_end(self):
        if not (end_value := self.cleaned_data.get("address_range_end")):
            return None
        try:
            return str(IPNetwork(str(end_value)))
        except Exception as exc:
            raise ValidationError(
                _("Enter a valid IPv4 or IPv6 address with mask.")
            ) from exc

    def save(self, *args, **kwargs):
        if self.request_user is not None:
            self.instance._status_sync_user = self.request_user
        return super().save(*args, **kwargs)


class NatPoolMemberBulkEditForm(PortsForm, PrimaryModelBulkEditForm):
    model = NatPoolMember
    pool = DynamicModelChoiceField(queryset=NatPool.objects.all(), required=False)
    status = forms.ChoiceField(required=False, choices=IPAddressStatusChoices)
    tags = TagFilterField(model)
    nullable_fields = []
    fieldsets = (
        FieldSet(
            "pool",
            "status",
            "source_ports",
            "destination_ports",
        ),
        FieldSet("tags", name=_("Tags")),
    )
