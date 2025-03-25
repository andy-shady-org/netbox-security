from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from ipam.constants import SERVICE_PORT_MIN, SERVICE_PORT_MAX
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm
)
from utilities.forms.rendering import FieldSet, TabbedGroups
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    CSVChoiceField,
    NumericArrayField,
    CSVModelChoiceField
)
from ipam.models import IPAddress, Prefix, IPRange
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import (
    NatPool,
    NatPoolMember,
)


__all__ = (
    "NatPoolMemberForm",
    "NatPoolMemberFilterForm",
    "NatPoolMemberImportForm",
    "NatPoolMemberBulkEditForm",
)


class NatPoolMemberForm(NetBoxModelForm):
    name = forms.CharField(
        max_length=64,
        required=True
    )
    pool = DynamicModelChoiceField(
        queryset=NatPool.objects.all(),
        required=True,
    )
    status = forms.ChoiceField(
        choices=IPAddressStatusChoices,
        widget=forms.Select()
    )
    address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False,
    )
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
    )
    address_range = DynamicModelChoiceField(
        queryset=IPRange.objects.all(),
        required=False,
    )
    source_ports = NumericArrayField(
        base_field=forms.IntegerField(
            min_value=SERVICE_PORT_MIN,
            max_value=SERVICE_PORT_MAX
        ),
        help_text="Comma-separated list of one or more port numbers. A range may be specified using a hyphen.",
        required=False,
    )
    destination_ports = NumericArrayField(
        base_field=forms.IntegerField(
            min_value=SERVICE_PORT_MIN,
            max_value=SERVICE_PORT_MAX
        ),
        help_text="Comma-separated list of one or more port numbers. A range may be specified using a hyphen.",
        required=False,

    )
    fieldsets = (
        FieldSet('name', 'status'),
        FieldSet('pool', name=_('Nat Pool')),
        FieldSet(
            TabbedGroups(
                FieldSet('address', name=_('IP Address')),
                FieldSet('prefix', name=_('Prefix')),
                FieldSet('address_range', name=_('IP Range')),
            ),
            name=_('Pool Prefix/Address/Range')
        ),
        FieldSet('source_ports', 'destination_ports', name=_('Source/Destination Ports')),
        FieldSet("tags", name=_("Tags")),
    )

    class Meta:
        model = NatPoolMember
        fields = [
            'name', 'pool', 'address', 'prefix', 'address_range', 'source_ports', 'destination_ports', 'tags',
        ]

    def clean_address(self):
        if 'address' in self.cleaned_data and self.cleaned_data['address']:
            try:
                ip = IPAddress.objects.get(address=str(self.cleaned_data['address']))
            except MultipleObjectsReturned:
                ip = IPAddress.objects.filter(address=str(self.cleaned_data['address'])).first()
            except ObjectDoesNotExist:
                ip = IPAddress.objects.create(address=str(self.cleaned_data['address']))
            self.cleaned_data['address'] = ip
            return self.cleaned_data['address']

    def clean_prefix(self):
        if 'prefix' in self.cleaned_data and self.cleaned_data['prefix']:
            try:
                network = Prefix.objects.get(prefix=str(self.cleaned_data['prefix']))
            except MultipleObjectsReturned:
                network = Prefix.objects.filter(prefix=str(self.cleaned_data['prefix'])).first()
            except ObjectDoesNotExist:
                network = Prefix.objects.create(prefix=str(self.cleaned_data['prefix']))
            self.cleaned_data['prefix'] = network
            return self.cleaned_data['prefix']

    def clean_address_range(self):
        if 'address_range' in self.cleaned_data and self.cleaned_data['address_range']:
            try:
                address_range = IPRange.objects.get(start_address=str(self.cleaned_data['address_range'].start_address))
            except MultipleObjectsReturned:
                address_range = IPRange.objects.filter(start_address=str(self.cleaned_data['address_range'].start_address)).first()
            self.cleaned_data['address_range'] = address_range
            return self.cleaned_data['address_range']


class NatPoolMemberFilterForm(NetBoxModelFilterSetForm):
    model = NatPoolMember
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet('name', 'pool_type'),
        FieldSet('address', 'prefix', 'address_range', name=_('IPAM')),
        FieldSet('source_ports', 'destination_ports', name=_('Ports')),
    )
    pool = DynamicModelMultipleChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
    )
    address = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False
    )
    prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False
    )
    address_range = DynamicModelChoiceField(
        queryset=IPRange.objects.all(),
        required=False
    )
    source_port = forms.IntegerField(
        required=False,
    )
    destination_port = forms.IntegerField(
        required=False,
    )
    tags = TagFilterField(model)


class NatPoolMemberImportForm(NetBoxModelImportForm):
    pool = CSVModelChoiceField(
        queryset=NatPool.objects.all(),
        required=False,
        to_field_name='name',
        help_text=_('NAT Pool (Name)')
    )
    address = CSVModelChoiceField(
        queryset=IPAddress.objects.filter(),
        required=False,
        to_field_name='address',
        help_text=_('IP Address')
    )
    prefix = CSVModelChoiceField(
        queryset=Prefix.objects.filter(),
        required=False,
        to_field_name='prefix',
        help_text=_('Prefix')
    )
    address_range = CSVModelChoiceField(
        queryset=IPRange.objects.filter(),
        required=False,
        to_field_name='start_address',
        help_text=_('IPv4 or IPv6 start address (with mask)')
    )
    status = CSVChoiceField(
        choices=IPAddressStatusChoices,
        help_text=_('Status')
    )

    class Meta:
        model = NatPoolMember
        fields = ('name', 'pool', 'address', 'prefix', 'address_range', 'source_ports', 'destination_ports', 'tags')


class NatPoolMemberBulkEditForm(NetBoxModelBulkEditForm):
    model = NatPool
    pool = DynamicModelMultipleChoiceField(
        queryset=NatPool.objects.all(),
        required=False
    )
    status = forms.ChoiceField(
        required=False,
        choices=IPAddressStatusChoices,
        widget=forms.Select()
    )
    tags = TagFilterField(model)
    nullable_fields = [
    ]
    fieldsets = (
        FieldSet('pool', 'status'),
        FieldSet("tags", name=_("Tags")),
    )
