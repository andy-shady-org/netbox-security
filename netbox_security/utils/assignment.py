from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404


def get_assigned_object(request, *, allowed_content_type_filter):
    ct_id = request.GET.get("assigned_object_type")
    obj_id = request.GET.get("assigned_object_id")

    if not ct_id or not obj_id:
        raise Http404

    content_type = get_object_or_404(ContentType, pk=ct_id)
    if (
        not ContentType.objects.filter(pk=content_type.pk)
        .filter(allowed_content_type_filter)
        .exists()
    ):
        raise Http404

    model = content_type.model_class()

    queryset = model.objects.all()

    # NetBox-style permission scoping if the model supports it
    if hasattr(queryset, "restrict"):
        queryset = queryset.restrict(request.user, "view")

    return get_object_or_404(queryset, pk=obj_id)
