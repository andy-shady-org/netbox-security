from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm
)

from tenancy.forms import TenancyForm, TenancyFilterForm
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
)


from netbox_security.models import (
    SecurityZone,
    SecurityZoneAssignment,
)

__all__ = (
    "SecurityZoneForm",
    "SecurityZoneFilterForm",
    "SecurityZoneImportForm",
    "SecurityZoneBulkEditForm",
    "SecurityZoneAssignmentForm",
)


class SecurityZoneForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(
        max_length=64,
        required=True
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    fieldsets = (
        FieldSet('name', 'description', name=_('Security Zone')),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = SecurityZone
        fields = [
            'name', 'tenant_group', 'tenant', 'description', 'comments', 'tags',
        ]


class SecurityZoneFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = SecurityZone
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet('name',),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    tags = TagFilterField(model)


class SecurityZoneImportForm(NetBoxModelImportForm):

    class Meta:
        model = SecurityZone
        fields = (
            'name', 'description', 'tenant', 'tags',
        )


class SecurityZoneBulkEditForm(NetBoxModelBulkEditForm):
    model = SecurityZone
    description = forms.CharField(
        max_length=200,
        required=False
    )
    tags = TagFilterField(model)
    nullable_fields = [
    ]
    fieldsets = (
        FieldSet('description'),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class SecurityZoneAssignmentForm(forms.ModelForm):
    zone = DynamicModelChoiceField(
        label=_('Security Zone'),
        queryset=SecurityZone.objects.all()
    )

    fieldsets = (
        FieldSet(ObjectAttribute('assigned_object'), 'zone'),
    )

    class Meta:
        model = SecurityZoneAssignment
        fields = ('zone',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_zone(self):
        zone = self.cleaned_data['zone']

        conflicting_assignments = SecurityZoneAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            zone=zone
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(id=self.instance.id)

        if conflicting_assignments.exists():
            raise forms.ValidationError(
                _('Assignment already exists')
            )

        return zone
