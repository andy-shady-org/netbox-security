"""Resolve explicit zone membership independently of policy address matching."""

from django.contrib.contenttypes.models import ContentType

from netbox_security.models import SecurityZone, SecurityZoneAssignment

from .hierarchy_limits import HierarchyBudget


def resolve_zone_membership(target, *, user):
    """Return visible interface zone IDs, or None if membership is unknown.

    A device assignment lists zones available on that device; it does not place
    every interface/IP in every zone. Policy address books are not membership.
    """
    if target._meta.label_lower != "ipam.ipaddress":
        return None
    object_type = target.assigned_object_type
    if object_type is None or (object_type.app_label, object_type.model) != (
        "dcim",
        "interface",
    ):
        return None

    from dcim.models import Interface

    interface = (
        Interface.objects.restrict(user, "view")
        .filter(pk=target.assigned_object_id)
        .first()
    )
    if interface is None:
        return None

    budget = HierarchyBudget()
    zone_ids = budget.take(
        SecurityZoneAssignment.objects.restrict(user, "view")
        .filter(
            assigned_object_type=ContentType.objects.get_for_model(Interface),
            assigned_object_id=interface.pk,
            zone_id__in=SecurityZone.objects.restrict(user, "view").values("pk"),
        )
        .order_by("zone_id")
        .values_list("zone_id", flat=True)
        .distinct()
    )
    if budget.truncated or not zone_ids:
        return None
    return zone_ids
