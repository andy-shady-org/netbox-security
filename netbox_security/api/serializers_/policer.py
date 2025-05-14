from rest_framework.serializers import (
    HyperlinkedIdentityField,
    IntegerField,
    BooleanField,
    ChoiceField,
)
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers import TenantSerializer

from netbox_security.models import Policer
from netbox_security.choices import (
    LossPriorityChoices,
    ForwardingClassChoices,
)


class PolicerSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:policer-detail"
    )
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    logical_interface_policer = BooleanField(required=False, allow_null=True)
    physical_interface_policer = BooleanField(required=False, allow_null=True)
    discard = BooleanField(required=False, allow_null=True)
    out_of_profile = BooleanField(required=False, allow_null=True)
    bandwidth_limit = IntegerField(required=False, allow_null=True)
    bandwidth_percent = IntegerField(required=False, allow_null=True)
    burst_size_limit = IntegerField(required=False, allow_null=True)
    loss_priority = ChoiceField(choices=LossPriorityChoices, required=False)
    forwarding_class = ChoiceField(choices=ForwardingClassChoices, required=False)

    class Meta:
        model = Policer
        fields = (
            "id",
            "url",
            "display",
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
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "logical_interface_policer",
            "physical_interface_policer",
            "bandwidth_limit",
            "bandwidth_percent",
            "burst_size_limit",
            "loss_priority",
            "forwarding_class",
            "discard",
            "out_of_profile",
            "description",
        )
