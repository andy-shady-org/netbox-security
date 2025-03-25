from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm
)
from utilities.forms.rendering import FieldSet,  ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CSVChoiceField,
    CommentField,
)

from netbox_security.choices import (
    PoolTypeChoices
)

from netbox_security.models import (
    NatPool,
    NatPoolAssignment,
)


__all__ = (
    "NatPoolForm",
    "NatPoolFilterForm",
    "NatPoolImportForm",
    "NatPoolBulkEditForm",
    "NatPoolAssignmentForm",
)


class NatPoolForm(NetBoxModelForm):
    name = forms.CharField(
        max_length=64,
        required=True
    )
    pool_type = forms.ChoiceField(
        required=False,
        choices=PoolTypeChoices,
        widget=forms.Select()
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    fieldsets = (
        FieldSet('name', 'pool_type', 'description'),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = NatPool
        fields = [
            'name', 'pool_type', 'description', 'comments', 'tags',
        ]


class NatPoolFilterForm(NetBoxModelFilterSetForm):
    model = NatPool
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet('name', 'pool_type'),
    )
    pool_type = forms.ChoiceField(
        required=False,
        choices=PoolTypeChoices,
        widget=forms.Select()
    )
    tags = TagFilterField(model)


class NatPoolImportForm(NetBoxModelImportForm):
    pool_type = CSVChoiceField(
        choices=PoolTypeChoices,
        help_text=_('NAT Pool Type')
    )

    class Meta:
        model = NatPool
        fields = ('name', 'pool_type', 'description', 'tags')


class NatPoolBulkEditForm(NetBoxModelBulkEditForm):
    model = NatPool
    pool_type = forms.ChoiceField(
        required=False,
        choices=PoolTypeChoices,
        widget=forms.Select()
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    tags = TagFilterField(model)
    nullable_fields = [
       'description',
    ]
    fieldsets = (
        FieldSet('pool_type', 'description'),
        FieldSet("tags", name=_("Tags")),
    )


class NatPoolAssignmentForm(forms.ModelForm):
    pool = DynamicModelChoiceField(
        label=_('NAT Pool'),
        queryset=NatPool.objects.all()
    )

    fieldsets = (
        FieldSet(ObjectAttribute('assigned_object'), 'pool'),
    )

    class Meta:
        model = NatPoolAssignment
        fields = ('pool',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_pool(self):
        pool = self.cleaned_data['pool']

        conflicting_assignments = NatPoolAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            pool=pool
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(id=self.instance.id)

        if conflicting_assignments.exists():
            raise forms.ValidationError(
                _('Assignment already exists')
            )

        return pool
