from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ListField,
    CharField,
    ValidationError,
    ChoiceField,
)
from netbox.api.serializers import NetBoxModelSerializer
from netbox_security.api.serializers import (
    SecurityZoneSerializer,
    AddressListSerializer,
)
from netbox_security.models import (
    SecurityZonePolicy,
)

from netbox_security.choices import ActionChoices


class SecurityZonePolicySerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:securityzonepolicy-detail"
    )
    source_zone = SecurityZoneSerializer(nested=True, required=True)
    destination_zone = SecurityZoneSerializer(nested=True, required=True)
    source_address = AddressListSerializer(
        nested=True, required=False, allow_null=True, many=True
    )
    destination_address = AddressListSerializer(
        nested=True, required=False, allow_null=True, many=True
    )
    application = ListField(
        child=CharField(),
        required=False,
        allow_empty=True,
        default=[],
    )
    actions = ListField(
        child=ChoiceField(choices=ActionChoices, required=False),
        required=True,
    )

    class Meta:
        model = SecurityZonePolicy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "index",
            "description",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "application",
            "actions",
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
            "description",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "application",
            "actions",
        )

    def validate(self, data):
        error_message = {}
        if isinstance(data, dict):
            if (source_zone := data.get("source_zone")) is not None and (
                destination_zone := data.get("destination_zone")
            ) is not None:
                if source_zone == destination_zone:
                    error_message_mismatch_zones = "Cannot have the same source and destination zones within a policy"
                    error_message["source_zones"] = [error_message_mismatch_zones]
                    error_message["destination_zones"] = [error_message_mismatch_zones]
            if (source_address := data.get("source_address")) is not None and (
                destination_address := data.get("destination_address")
            ) is not None:
                if set(source_address) & set(destination_address):
                    error_message_mismatch_zones = "Cannot have the same source and destination addresses within a policy"
                    error_message["source_address"] = [error_message_mismatch_zones]
                    error_message["destination_address"] = [
                        error_message_mismatch_zones
                    ]
        if error_message:
            raise ValidationError(error_message)
        return super().validate(data)

    def create(self, validated_data):
        source_address = validated_data.pop("source_address", None)
        destination_address = validated_data.pop("destination_address", None)
        policy = super().create(validated_data)

        if source_address is not None:
            policy.source_address.set(source_address)
        if destination_address is not None:
            policy.destination_address.set(destination_address)
        return policy

    def update(self, instance, validated_data):
        source_address = validated_data.pop("source_address", None)
        destination_address = validated_data.pop("destination_address", None)
        policy = super().update(instance, validated_data)

        if source_address is not None:
            policy.source_address.set(source_address)
        if destination_address is not None:
            policy.destination_address.set(destination_address)
        return policy
