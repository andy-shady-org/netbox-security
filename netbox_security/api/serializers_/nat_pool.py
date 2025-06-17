from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ChoiceField,
    SerializerMethodField,
    JSONField,
    IntegerField,
)
from drf_spectacular.utils import extend_schema_field

from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from utilities.api import get_serializer_for_model

from netbox_security.models import NatPool, NatPoolAssignment

from netbox_security.choices import (
    PoolTypeChoices,
)
from netbox_security.constants import (
    POOL_ASSIGNMENT_MODELS,
)


class NatPoolSerializer(NetBoxModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="plugins-api:netbox_security-api:natpool-detail"
    )
    pool_type = ChoiceField(choices=PoolTypeChoices, required=True)
    member_count = IntegerField(read_only=True)

    class Meta:
        model = NatPool
        fields = (
            "id",
            "url",
            "display",
            "name",
            "pool_type",
            "status",
            "description",
            "member_count",
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
            "status",
            "pool_type",
            "description",
            "member_count",
        )


class NatPoolAssignmentSerializer(NetBoxModelSerializer):
    pool = NatPoolSerializer(nested=True, required=True, allow_null=False)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(POOL_ASSIGNMENT_MODELS)
    )
    assigned_object = SerializerMethodField(read_only=True)

    class Meta:
        model = NatPoolAssignment
        fields = [
            "id",
            "url",
            "display",
            "pool",
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
            "pool",
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
