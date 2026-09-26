"""Resolve explicit zone membership independently of policy address matching."""

from django.contrib.contenttypes.models import ContentType

from netbox_security.models import SecurityZone, SecurityZoneAssignment

from .hierarchy_limits import HierarchyBudget


def _zone_ids_for_assignments(model, object_ids, *, user, budget):
    if not object_ids:
        return []

    return list(
        budget.take(
            SecurityZoneAssignment.objects.restrict(user, "view")
            .filter(
                assigned_object_type=ContentType.objects.get_for_model(model),
                assigned_object_id__in=object_ids,
                zone_id__in=SecurityZone.objects.restrict(user, "view").values("pk"),
            )
            .order_by("zone_id")
            .values_list("zone_id", flat=True)
            .distinct()
        )
    )


def _direct_zone_ids(target, *, user, budget):
    return _zone_ids_for_assignments(target.__class__, [target.pk], user=user, budget=budget)


def _effective_prefix_zone_ids(prefix, *, user, budget, cache):
    cache_key = prefix.pk
    if cache_key in cache:
        return cache[cache_key]

    direct_zone_ids = _direct_zone_ids(prefix, user=user, budget=budget)
    if direct_zone_ids:
        cache[cache_key] = sorted(set(direct_zone_ids))
        return cache[cache_key]

    inherited_zone_ids = set()
    for parent in budget.take(
        prefix.get_parents().restrict(user, "view").filter(vrf_id=prefix.vrf_id).order_by("pk")
    ):
        inherited_zone_ids.update(
            _effective_prefix_zone_ids(parent, user=user, budget=budget, cache=cache)
        )

    cache[cache_key] = sorted(inherited_zone_ids)
    return cache[cache_key]


def resolve_zone_membership(target, *, user):
    """Return visible zone IDs for IPAM objects with direct or inherited zone context.

    Zone membership is explicit and independent of address-book policy matches.
    An IP can belong to a zone because it is assigned to a zoned interface, or
    because it falls within a zoned prefix or IP range. Prefixes and IP ranges
    can also inherit zone context from containing prefixes unless they have a
    direct assignment of their own.
    """
    if target._meta.label_lower not in {"ipam.ipaddress", "ipam.prefix", "ipam.iprange"}:
        return None

    from dcim.models import Interface
    from ipam.models import IPRange, Prefix

    budget = HierarchyBudget()
    prefix_cache = {}

    if target._meta.label_lower == "ipam.prefix":
        zone_ids = set(
            _effective_prefix_zone_ids(target, user=user, budget=budget, cache=prefix_cache)
        )
        if budget.truncated or not zone_ids:
            return None
        return sorted(zone_ids)

    if target._meta.label_lower == "ipam.iprange":
        direct_zone_ids = _direct_zone_ids(target, user=user, budget=budget)
        if direct_zone_ids:
            if budget.truncated:
                return None
            return sorted(set(direct_zone_ids))

        if target.vrf_id is not None:
            parent_prefixes = Prefix.objects.restrict(user, "view").filter(
                vrf_id=target.vrf_id,
                prefix__net_contains_or_equals=str(target.start_address.ip),
            ).filter(prefix__net_contains_or_equals=str(target.end_address.ip))
        else:
            parent_prefixes = Prefix.objects.restrict(user, "view").filter(
                vrf__isnull=True,
                prefix__net_contains_or_equals=str(target.start_address.ip),
            ).filter(prefix__net_contains_or_equals=str(target.end_address.ip))

        zone_ids = set()
        for prefix in budget.take(parent_prefixes.order_by("pk")):
            zone_ids.update(
                _effective_prefix_zone_ids(
                    prefix, user=user, budget=budget, cache=prefix_cache
                )
            )

        if budget.truncated or not zone_ids:
            return None
        return sorted(zone_ids)

    zone_ids = set()

    # Interface membership remains the direct attachment model.
    object_type = target.assigned_object_type
    if object_type is not None and (object_type.app_label, object_type.model) == (
        "dcim",
        "interface",
    ):
        zone_ids.update(
            _zone_ids_for_assignments(
                Interface, [target.assigned_object_id], user=user, budget=budget
            )
        )

    # Prefix membership: if this IP falls inside a prefix assigned to a zone,
    # that zone is a valid membership context for the address.
    prefix_qs = Prefix.objects.restrict(user, "view")
    if target.vrf_id is not None:
        prefix_qs = prefix_qs.filter(vrf_id=target.vrf_id)
    else:
        prefix_qs = prefix_qs.filter(vrf__isnull=True)
    prefix_qs = prefix_qs.filter(prefix__net_contains_or_equals=str(target.address))
    for prefix in budget.take(prefix_qs.order_by("pk")):
        zone_ids.update(
            _effective_prefix_zone_ids(prefix, user=user, budget=budget, cache=prefix_cache)
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
    for ip_range in budget.take(range_qs.filter(pk__in=range_ids).order_by("pk")):
        direct_zone_ids = _direct_zone_ids(ip_range, user=user, budget=budget)
        if direct_zone_ids:
            zone_ids.update(direct_zone_ids)
            continue

        if ip_range.vrf_id is not None:
            parent_prefixes = Prefix.objects.restrict(user, "view").filter(
                vrf_id=ip_range.vrf_id,
                prefix__net_contains_or_equals=str(ip_range.start_address.ip),
            ).filter(prefix__net_contains_or_equals=str(ip_range.end_address.ip))
        else:
            parent_prefixes = Prefix.objects.restrict(user, "view").filter(
                vrf__isnull=True,
                prefix__net_contains_or_equals=str(ip_range.start_address.ip),
            ).filter(prefix__net_contains_or_equals=str(ip_range.end_address.ip))

        for prefix in budget.take(parent_prefixes.order_by("pk")):
            zone_ids.update(
                _effective_prefix_zone_ids(
                    prefix, user=user, budget=budget, cache=prefix_cache
                )
            )

    if budget.truncated or not zone_ids:
        return None
    return sorted(zone_ids)
