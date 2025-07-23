from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    JSONField,
)
from drf_spectacular.utils import extend_schema_field
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model
from tenancy.api.serializers import TenantSerializer
from netbox_security.models import ApplicationSet, ApplicationSetAssignment
from netbox_security.constants import APPLICATION_ASSIGNMENT_MODELS
from netbox_security.api.serializers import ApplicationSerializer


class NestedApplicationSetSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:applicationset-detail"
    )

    class Meta:
        model = ApplicationSet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "applications",
            "application_sets",
            "description",
            "tenant",
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
            "applications",
            "application_sets",
            "description",
        )


class ApplicationSetSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:applicationset-detail"
    )
    tenant = TenantSerializer(nested=True, required=False, allow_null=True)
    applications = ApplicationSerializer(
        nested=True, required=False, allow_null=True, many=True
    )
    application_sets = NestedApplicationSetSerializer(
        nested=True, required=False, allow_null=True, many=True
    )

    class Meta:
        model = ApplicationSet
        fields = (
            "id",
            "url",
            "display",
            "name",
            "identifier",
            "applications",
            "application_sets",
            "description",
            "tenant",
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
            "applications",
            "application_sets",
            "description",
        )

    def create(self, validated_data):
        applications = validated_data.pop("applications", None)
        application_sets = validated_data.pop("application_sets", None)
        obj = super().create(validated_data)
        if applications is not None:
            obj.applications.set(applications)
        if application_sets is not None:
            obj.application_sets.set(application_sets)
        return obj

    def update(self, instance, validated_data):
        applications = validated_data.pop("applications", None)
        application_sets = validated_data.pop("application_sets", None)
        obj = super().update(instance, validated_data)
        if applications is not None:
            obj.applications.set(applications)
        if application_sets is not None:
            obj.application_sets.set(application_sets)
        return obj


class ApplicationSetAssignmentSerializer(NetBoxModelSerializer):
    application_set = ApplicationSetSerializer(
        nested=True, required=True, allow_null=False
    )
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(APPLICATION_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = ApplicationSetAssignment
        fields = [
            "id",
            "url",
            "display",
            "application_set",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "created",
            "last_updated",
        ]
        brief_fields = (
            "id",
            "url",
            "display",
            "application_set",
            "assigned_object_type",
            "assigned_object_id",
        )

    @extend_schema_field(JSONField(allow_null=True))
    def get_assigned_object(self, obj):
        if obj.assigned_object is None:
            return None
        serializer = get_serializer_for_model(obj.assigned_object)
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, nested=True, context=context).data
