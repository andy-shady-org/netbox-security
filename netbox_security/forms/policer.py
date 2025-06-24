from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
    NetBoxModelFilterSetForm,
)

from tenancy.forms import TenancyForm, TenancyFilterForm
from utilities.forms.rendering import FieldSet, ObjectAttribute
from utilities.forms.fields import (
    DynamicModelChoiceField,
    TagFilterField,
    CommentField,
    CSVModelChoiceField,
    CSVChoiceField,
)

from tenancy.models import Tenant, TenantGroup

from netbox_security.models import (
    Policer,
    PolicerAssignment,
)
from netbox_security.choices import (
    LossPriorityChoices,
    ForwardingClassChoices,
)


__all__ = (
    "PolicerForm",
    "PolicerFilterForm",
    "PolicerImportForm",
    "PolicerBulkEditForm",
    "PolicerAssignmentForm",
)


class PolicerForm(TenancyForm, NetBoxModelForm):
    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(max_length=200, required=False)
    logical_interface_policer = forms.BooleanField(
        required=False, help_text=_("Policer is logical interface policer")
    )
    physical_interface_policer = forms.BooleanField(
        required=False, help_text=_("Policer is physical interface policer")
    )
    bandwidth_limit = forms.IntegerField(
        required=False,
        help_text=_("Bandwidth limit (32000..50000000000 bits per second)"),
    )
    bandwidth_percent = forms.IntegerField(
        required=False, help_text=_("Bandwidth limit in percentage (1..100 percent)")
    )
    burst_size_limit = forms.IntegerField(
        required=False, help_text=_("Burst size limit (1500..100000000000 bytes)")
    )
    loss_priority = forms.ChoiceField(
        required=False,
        choices=LossPriorityChoices,
        help_text=_("Packet's loss priority"),
    )
    forwarding_class = forms.ChoiceField(
        required=False,
        choices=ForwardingClassChoices,
        help_text=_("Classify packet to forwarding class"),
    )
    discard = forms.BooleanField(required=False, help_text=_("Discard the packet"))
    out_of_profile = forms.BooleanField(
        required=False,
        help_text=_("Discard packets only if both congested and over threshold"),
    )
    fieldsets = (
        FieldSet(
            "name",
            "description",
            "logical_interface_policer",
            "physical_interface_policer",
            name=_("Policer Parameters"),
        ),
        FieldSet(
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            name=_("If Exceeding"),
        ),
        FieldSet(
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            name=_("Then"),
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )
    comments = CommentField()

    class Meta:
        model = Policer
        fields = [
            "name",
            "tenant_group",
            "tenant",
            "description",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "comments",
            "tags",
        ]


class PolicerFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Policer
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet(
            "name",
        ),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenancy")),
    )
    tags = TagFilterField(model)


class PolicerImportForm(NetBoxModelImportForm):
    tenant = CSVModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        label=_("Tenant"),
    )
    logical_interface_policer = forms.BooleanField(
        required=False, help_text=_("Policer is logical interface policer")
    )
    physical_interface_policer = forms.BooleanField(
        required=False, help_text=_("Policer is physical interface policer")
    )
    bandwidth_limit = forms.IntegerField(
        required=False,
        help_text=_("Bandwidth limit (32000..50000000000 bits per second)"),
    )
    bandwidth_percent = forms.IntegerField(
        required=False, help_text=_("Bandwidth limit in percentage (1..100 percent)")
    )
    burst_size_limit = forms.IntegerField(
        required=False, help_text=_("Burst size limit (1500..100000000000 bytes)")
    )
    loss_priority = CSVChoiceField(
        required=False,
        choices=LossPriorityChoices,
        help_text=_("Packet's loss priority"),
    )
    forwarding_class = CSVChoiceField(
        required=False,
        choices=ForwardingClassChoices,
        help_text=_("Classify packet to forwarding class"),
    )
    discard = forms.BooleanField(required=False, help_text=_("Discard the packet"))
    out_of_profile = forms.BooleanField(
        required=False,
        help_text=_("Discard packets only if both congested and over threshold"),
    )

    class Meta:
        model = Policer
        fields = (
            "name",
            "description",
            "tenant",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "tags",
        )


class PolicerBulkEditForm(NetBoxModelBulkEditForm):
    model = Policer
    description = forms.CharField(max_length=200, required=False)
    logical_interface_policer = forms.BooleanField(
        required=False, help_text=_("Policer is logical interface policer")
    )
    physical_interface_policer = forms.BooleanField(
        required=False, help_text=_("Policer is physical interface policer")
    )
    bandwidth_limit = forms.IntegerField(
        required=False,
        help_text=_("Bandwidth limit (32000..50000000000 bits per second)"),
    )
    bandwidth_percent = forms.IntegerField(
        required=False, help_text=_("Bandwidth limit in percentage (1..100 percent)")
    )
    burst_size_limit = forms.IntegerField(
        required=False, help_text=_("Burst size limit (1500..100000000000 bytes)")
    )
    loss_priority = forms.ChoiceField(
        required=False,
        choices=LossPriorityChoices,
        help_text=_("Packet's loss priority"),
    )
    forwarding_class = forms.ChoiceField(
        required=False,
        choices=ForwardingClassChoices,
        help_text=_("Classify packet to forwarding class"),
    )
    discard = forms.BooleanField(required=False, help_text=_("Discard the packet"))
    out_of_profile = forms.BooleanField(
        required=False,
        help_text=_("Discard packets only if both congested and over threshold"),
    )
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
    tags = TagFilterField(model)
    nullable_fields = ["description", "tenant"]
    fieldsets = (
        FieldSet(
            "description",
            "logical_interface_policer",
            "physical_interface_policer",
            name=_("Policer"),
        ),
        FieldSet(
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            name=_("If Exceeding"),
        ),
        FieldSet(
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            name=_("Then"),
        ),
        FieldSet("tenant_group", "tenant", name=_("Tenancy")),
        FieldSet("tags", name=_("Tags")),
    )


class PolicerAssignmentForm(forms.ModelForm):
    policer = DynamicModelChoiceField(
        label=_("Policer"), queryset=Policer.objects.all()
    )

    fieldsets = (FieldSet(ObjectAttribute("assigned_object"), "policer"),)

    class Meta:
        model = PolicerAssignment
        fields = ("policer",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_pool(self):
        policer = self.cleaned_data["policer"]

        conflicting_assignments = PolicerAssignment.objects.filter(
            assigned_object_type=self.instance.assigned_object_type,
            assigned_object_id=self.instance.assigned_object_id,
            policer=policer,
        )
        if self.instance.id:
            conflicting_assignments = conflicting_assignments.exclude(
                id=self.instance.id
            )

        if conflicting_assignments.exists():
            raise forms.ValidationError(_("Assignment already exists"))

        return policer
