from django import forms
from django.utils.translation import gettext_lazy as _

from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
)


from netbox_security.models import (
    AddressList,
    AddressListAssignment,
)

__all__ = (
    "AddressListForm",
    "AddressListAssignmentForm",
)


class AddressListForm(forms.ModelForm):
    name = forms.CharField(max_length=64, required=True)
    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "name"),)

    class Meta:
        model = AddressList
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
