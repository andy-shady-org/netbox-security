from rest_framework.serializers import HyperlinkedIdentityField, ChoiceField
from netbox.api.serializers import NetBoxModelSerializer
from netbox_security.models import ApplicationItem
from netbox_security.choices import ProtocolChoices


class ApplicationItemSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:applicationitem-detail"
    )
    protocol = ChoiceField(choices=ProtocolChoices, required=False)

    class Meta:
        model = ApplicationItem
        fields = (
            "id",
            "url",
            "display",
            "name",
            "index",
            "protocol",
            "destination_port",
            "source_port",
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
            "destination_port",
            "source_port",
            "description",
        )
