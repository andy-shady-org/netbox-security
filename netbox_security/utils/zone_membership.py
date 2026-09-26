"""Resolve explicit zone membership independently of policy address matching."""

from django.contrib.contenttypes.models import ContentType

from netbox_security.models import SecurityZone, SecurityZoneAssignment

from .hierarchy_limits import HierarchyBudget


def resolve_zone_membership(target, *, user):
    """Return visible zone IDs for an IP address, including interface, prefix, and IP range membership.

    Zone membership is explicit and independent of address-book policy matches.
    An IP can belong to a zone because it is assigned to a zoned interface, or
    because it falls within a zoned prefix or IP range.
    """
    if target._meta.label_lower != "ipam.ipaddress":
        return None

    from dcim.models import Interface
    from ipam.models import IPRange, Prefix

    budget = HierarchyBudget()
    zone_ids = set()

    # Interface membership remains the direct attachment model.
    object_type = target.assigned_object_type
    if object_type is not None and (object_type.app_label, object_type.model) == (
        "dcim",
        "interface",
    ):
        interface = (
            Interface.objects.restrict(user, "view")
            .filter(pk=target.assigned_object_id)
            .first()
        )
        if interface is not None:
            zone_ids.update(
                budget.take(
                    SecurityZoneAssignment.objects.restrict(user, "view")
                    .filter(
                        assigned_object_type=ContentType.objects.get_for_model(
                            Interface
                        ),
                        assigned_object_id=interface.pk,
                        zone_id__in=SecurityZone.objects.restrict(user, "view").values(
                            "pk"
                        ),
                    )
                    .order_by("zone_id")
                    .values_list("zone_id", flat=True)
                    .distinct()
                )
            )

    # Prefix membership: if this IP falls inside a prefix assigned to a zone,
    # that zone is a valid membership context for the address.
    prefix_qs = Prefix.objects.restrict(user, "view")
    if target.vrf_id is not None:
        prefix_qs = prefix_qs.filter(vrf_id=target.vrf_id)
    else:
        prefix_qs = prefix_qs.filter(vrf__isnull=True)
    prefix_qs = prefix_qs.filter(prefix__net_contains=str(target.address.ip))
    zone_ids.update(
        budget.take(
            SecurityZoneAssignment.objects.restrict(user, "view")
            .filter(
                assigned_object_type=ContentType.objects.get_for_model(Prefix),
                assigned_object_id__in=prefix_qs.values("pk"),
                zone_id__in=SecurityZone.objects.restrict(user, "view").values("pk"),
            )
            .order_by("zone_id")
            .values_list("zone_id", flat=True)
            .distinct()
        )
    )

    # IP range membership: compare host values explicitly rather than relying on
    # masked address ordering. This matches how IPAM containment logic usually
    # reasons about a range's usable bounds.
    range_qs = IPRange.objects.restrict(user, "view")
    if target.vrf_id is not None:
        range_qs = range_qs.filter(vrf_id=target.vrf_id)
    else:
        range_qs = range_qs.filter(vrf__isnull=True)
    target_host = int(target.address.ip)
    target_version = int(target.address.version)
    range_ids = [
        range_id
        for range_id, start_address, end_address in budget.take(
            range_qs.order_by("pk").values_list("pk", "start_address", "end_address")
        )
        if int(start_address.version) == target_version
        and int(end_address.version) == target_version
        and int(start_address.ip) <= target_host <= int(end_address.ip)
    ]
    zone_ids.update(
        budget.take(
            SecurityZoneAssignment.objects.restrict(user, "view")
            .filter(
                assigned_object_type=ContentType.objects.get_for_model(IPRange),
                assigned_object_id__in=range_ids,
                zone_id__in=SecurityZone.objects.restrict(user, "view").values("pk"),
            )
            .order_by("zone_id")
            .values_list("zone_id", flat=True)
            .distinct()
        )
    )

    if budget.truncated or not zone_ids:
        return None
    return sorted(zone_ids)
