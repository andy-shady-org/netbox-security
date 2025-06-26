from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ChoiceField,
    ListField,
    IntegerField,
)
from netbox.api.serializers import NetBoxModelSerializer
from netbox_security.models import ApplicationItem
from netbox_security.choices import ProtocolChoices


class ApplicationItemSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:applicationitem-detail"
    )
    protocol = ListField(
        child=ChoiceField(choices=ProtocolChoices, required=False),
        required=False,
        default=[],
    )
    source_ports = ListField(
        child=IntegerField(),
        required=False,
        allow_empty=True,
        default=[],
    )
    destination_ports = ListField(
        child=IntegerField(),
        required=False,
        allow_empty=True,
        default=[],
    )

    class Meta:
        model = ApplicationItem
        fields = (
            "id",
            "url",
            "display",
            "name",
            "index",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
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
            "index",
            "protocol",
            "destination_ports",
            "source_ports",
            "description",
        )
