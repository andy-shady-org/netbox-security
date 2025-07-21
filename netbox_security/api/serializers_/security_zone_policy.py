from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ListField,
    ValidationError,
    ChoiceField,
)
from netbox.api.serializers import NetBoxModelSerializer
from netbox_security.api.serializers import (
    SecurityZoneSerializer,
    AddressListSerializer,
    ApplicationSerializer,
    ApplicationSetSerializer,
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
    applications = ApplicationSerializer(
        nested=True, required=False, allow_null=True, many=True
    )
    application_sets = ApplicationSetSerializer(
        nested=True, required=False, allow_null=True, many=True
    )
    policy_actions = ListField(
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
            "identifier",
            "index",
            "description",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "applications",
            "application_sets",
            "policy_actions",
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
            "identifier",
            "index",
            "description",
            "source_zone",
            "source_address",
            "destination_zone",
            "destination_address",
            "applications",
            "application_sets",
            "policy_actions",
        )

    def validate(self, data):
        if not isinstance(data, dict):
            return super().validate(data)

        errors = {}

        # Check for same source and destination zones
        source_zone = data.get("source_zone")
        destination_zone = data.get("destination_zone")
        if source_zone and destination_zone and source_zone == destination_zone:
            message = (
                "Cannot have the same source and destination zones within a policy."
            )
            errors["source_zone"] = [message]
            errors["destination_zone"] = [message]

        # Check for overlapping source and destination addresses
        source_address = data.get("source_address")
        destination_address = data.get("destination_address")
        if source_address and destination_address:
            overlap = set(source_address) & set(destination_address)
            if overlap:
                message = "Cannot have the same source and destination addresses within a policy."
                errors["source_address"] = [message]
                errors["destination_address"] = [message]

        if errors:
            raise ValidationError(errors)

        return super().validate(data)

    def create(self, validated_data):
        source_address = validated_data.pop("source_address", None)
        destination_address = validated_data.pop("destination_address", None)
        applications = validated_data.pop("applications", None)
        application_sets = validated_data.pop("application_sets", None)
        policy = super().create(validated_data)

        if source_address is not None:
            policy.source_address.set(source_address)
        if destination_address is not None:
            policy.destination_address.set(destination_address)
        if applications is not None:
            policy.applications.set(applications)
        if application_sets is not None:
            policy.application_sets.set(application_sets)
        return policy

    def update(self, instance, validated_data):
        source_address = validated_data.pop("source_address", None)
        destination_address = validated_data.pop("destination_address", None)
        applications = validated_data.pop("applications", None)
        application_sets = validated_data.pop("application_sets", None)
        policy = super().update(instance, validated_data)

        if source_address is not None:
            policy.source_address.set(source_address)
        if destination_address is not None:
            policy.destination_address.set(destination_address)
        if applications is not None:
            policy.applications.set(applications)
        if application_sets is not None:
            policy.application_sets.set(application_sets)
        return policy
