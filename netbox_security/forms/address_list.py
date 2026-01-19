from django import forms
from django.utils.translation import gettext_lazy as _

from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
)
from dcim.models import Device, VirtualDeviceContext

from netbox.forms import (
    NetBoxModelFilterSetForm,
)

from netbox_security.models import (
    AddressList,
    AddressListAssignment,
    SecurityZone,
    Address,
    AddressSet,
)

__all__ = (
    "AddressListForm",
    "AddressListFilterForm",
    "AddressListAssignmentForm",
    "AddressListAssignmentFilterForm",
)


class AddressListForm(forms.ModelForm):
    name = forms.CharField(max_length=64, required=True)
    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "name"),)

    class Meta:
        model = AddressList
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AddressListFilterForm(NetBoxModelFilterSetForm):
    model = AddressList
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "device_id",
            "virtualdevicecontext_id",
            "securityzone_id",
            name="Assignments",
        ),
    )
    device_id = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_("Device"),
    )
    virtualdevicecontext_id = DynamicModelChoiceField(
        queryset=VirtualDeviceContext.objects.all(),
        required=False,
        label=_("Virtual Device Context"),
        query_params={"device_id": "$device_id"},
    )
    securityzone_id = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
        label=_("Security Zone"),
    )


class AddressListAssignmentForm(forms.ModelForm):
    address_list = DynamicModelChoiceField(
        label=_("AddressList"), queryset=AddressList.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "address_list"),)

    class Meta:
        model = AddressListAssignment
        fields = ("address_list",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_address_list(self):
        address_list = self.cleaned_data["address_list"]

        conflicting_assignments = AddressListAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            address_list=address_list,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return address_list


class AddressListAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = AddressListAssignment
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "address_id",
            "addressset_id",
            "device_id",
            "virtualdevicecontext_id",
            "security_zone_id",
            name="Assignments",
        ),
    )
    address_id = DynamicModelChoiceField(
        queryset=Address.objects.all(),
        required=False,
        label=_("Address"),
    )
    addressset_id = DynamicModelChoiceField(
        queryset=AddressSet.objects.all(),
        required=False,
        label=_("Address Set"),
    )
    device_id = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_("Device"),
    )
    virtualdevicecontext_id = DynamicModelChoiceField(
        queryset=VirtualDeviceContext.objects.all(),
        required=False,
        label=_("Virtual Device Context"),
    )
    security_zone_id = DynamicModelChoiceField(
        queryset=SecurityZone.objects.all(),
        required=False,
        label=_("Security Zone"),
    )
