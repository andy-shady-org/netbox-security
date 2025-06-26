from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)

from utilities.forms.rendering import FieldSet
from utilities.forms.fields import (
    TagFilterField,
    CommentField,
    CSVMultipleChoiceField,
)

from netbox_security.models import (
    ApplicationItem,
)
from netbox_security.choices import ProtocolChoices
from netbox_security.mixins import PortsForm

__all__ = (
    "ApplicationItemForm",
    "ApplicationItemFilterForm",
    "ApplicationItemImportForm",
    "ApplicationItemBulkEditForm",
)


class ApplicationItemForm(PortsForm, NetBoxModelForm):
    name = forms.CharField(max_length=255, required=True)
    index = forms.IntegerField(required=True)
    protocol = forms.MultipleChoiceField(
        choices=ProtocolChoices,
        required=True,
    )
    description = forms.CharField(max_length=200, required=False)
    fieldsets = (
        FieldSet(
            "name",
            "index",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
            name=_("Application Items"),
        ),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = ApplicationItem
        fields = [
            "name",
            "index",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
            "comments",
            "tags",
        ]


class ApplicationItemFilterForm(PortsForm, NetBoxModelFilterSetForm):
    model = ApplicationItem
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "name",
            "index",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
            name=_("Application Items"),
        ),
    )
    index = forms.IntegerField(required=False)
    protocol = forms.MultipleChoiceField(
        choices=ProtocolChoices,
        required=False,
    )
    tags = TagFilterField(model)


class ApplicationItemImportForm(PortsForm, NetBoxModelImportForm):
    name = forms.CharField(max_length=255, required=True)
    index = forms.IntegerField(
        required=True,
        label=_("Index"),
    )
    description = forms.CharField(max_length=200, required=False)
    protocol = CSVMultipleChoiceField(
        choices=ProtocolChoices,
        required=True,
    )

    class Meta:
        model = ApplicationItem
        fields = (
            "name",
            "index",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
            "tags",
        )


class ApplicationItemBulkEditForm(NetBoxModelBulkEditForm):
    model = ApplicationItem
    description = forms.CharField(max_length=200, required=False)
    tags = TagFilterField(model)
    protocol = forms.MultipleChoiceField(
        choices=ProtocolChoices,
        required=False,
    )
    nullable_fields = [
        "description",
    ]
    fieldsets = (
        FieldSet("protocol", "description"),
        FieldSet("tags", name=_("Tags")),
    )
