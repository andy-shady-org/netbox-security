from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    CSVModelChoiceField,
)
from ipam.models import IPAddress, Prefix, IPRange
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import (
    NatPool,
    NatPoolMember,
)
from netbox_security.mixins import PortsForm


__all__ = (
    "NatPoolMemberForm",
    "NatPoolMemberFilterForm",
    "NatPoolMemberImportForm",
    "NatPoolMemberBulkEditForm",
)


class NatPoolMemberForm(PortsForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
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

    class Meta:
        model = NatPoolMember
        fields = [
            "name",
            "pool",
            "address",
            "prefix",
            "address_range",
            "source_ports",
            "destination_ports",
            "tags",
        ]

    def clean_address(self):
        if (address := self.cleaned_data.get("address")) is not None:
            try:
                ip = IPAddress.objects.get(address=str(address))
            except MultipleObjectsReturned:
                ip = IPAddress.objects.filter(address=str(address)).first()
            except ObjectDoesNotExist:
                ip = IPAddress.objects.create(address=str(address))
            self.cleaned_data["address"] = ip
        return self.cleaned_data.get("address")

    def clean_prefix(self):
        if (prefix := self.cleaned_data.get("prefix")) is not None:
            try:
                network = Prefix.objects.get(prefix=str(prefix))
            except MultipleObjectsReturned:
                network = Prefix.objects.filter(prefix=str(prefix)).first()
            except ObjectDoesNotExist:
                network = Prefix.objects.create(prefix=str(prefix))
            self.cleaned_data["prefix"] = network
        return self.cleaned_data.get("prefix")

    def clean_address_range(self):
        if (address_range := self.cleaned_data.get("address_range")) is not None:
            try:
                address_range = IPRange.objects.get(
                    start_address=str(address_range.start_address)
                )
            except MultipleObjectsReturned:
                address_range = IPRange.objects.filter(
                    start_address=str(address_range.start_address)
                ).first()
            self.cleaned_data["address_range"] = address_range
        return self.cleaned_data.get("address_range")


class NatPoolMemberFilterForm(PortsForm, NetBoxModelFilterSetForm):
    model = NatPoolMember
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
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


class NatPoolMemberImportForm(PortsForm, NetBoxModelImportForm):
    name = forms.CharField(max_length=200, required=True)
    pool = CSVModelChoiceField(
        queryset=NatPool.objects.all(),
        required=True,
        to_field_name="name",
        help_text=_("NAT Pool (Name)"),
    )
    address = CSVModelChoiceField(
        queryset=IPAddress.objects.filter(),
        required=False,
        to_field_name="address",
        help_text=_("IP Address"),
    )
    prefix = CSVModelChoiceField(
        queryset=Prefix.objects.filter(),
        required=False,
        to_field_name="prefix",
        help_text=_("Prefix"),
    )
    address_range = CSVModelChoiceField(
        queryset=IPRange.objects.filter(),
        required=False,
        to_field_name="start_address",
        help_text=_("IPv4 or IPv6 start address (with mask)"),
    )
    status = CSVChoiceField(choices=IPAddressStatusChoices, help_text=_("Status"))

    class Meta:
        model = NatPoolMember
        fields = (
            "name",
            "pool",
            "status",
            "address",
            "prefix",
            "address_range",
            "source_ports",
            "destination_ports",
            "tags",
        )

    def clean_address(self):
        if (address := self.cleaned_data.get("address")) is not None:
            try:
                ip = IPAddress.objects.get(address=str(address))
            except MultipleObjectsReturned:
                ip = IPAddress.objects.filter(address=str(address)).first()
            except ObjectDoesNotExist:
                ip = IPAddress.objects.create(address=str(address))
            self.cleaned_data["address"] = ip
            return self.cleaned_data["address"]

    def clean_prefix(self):
        if (prefix := self.cleaned_data.get("prefix")) is not None:
            try:
                network = Prefix.objects.get(prefix=str(prefix))
            except MultipleObjectsReturned:
                network = Prefix.objects.filter(prefix=str(prefix)).first()
            except ObjectDoesNotExist:
                network = Prefix.objects.create(prefix=str(prefix))
            self.cleaned_data["prefix"] = network
            return self.cleaned_data["prefix"]


class NatPoolMemberBulkEditForm(PortsForm, NetBoxModelBulkEditForm):
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
