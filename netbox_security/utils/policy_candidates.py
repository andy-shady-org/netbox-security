"""Presentation of address matches without claiming an effective firewall verdict."""

from collections import defaultdict

from django.db.models import Exists, OuterRef

from netbox_security.models import (
    Address,
    AddressAssignment,
    AddressList,
    AddressListAssignment,
    AddressSet,
    AddressSetAssignment,
    Application,
    ApplicationSet,
    SecurityZone,
    SecurityZonePolicy,
)
from netbox_security.mixins.assignment_validation import restrict_generic_assignments
from .hierarchy_limits import HierarchyBudget


def classify_match(zone_id, member_zone_ids, scope_allowed):
    if member_zone_ids is not None and zone_id not in member_zone_ids:
        return "zone_mismatch"
    if scope_allowed is False:
        return "scope_mismatch"
    if member_zone_ids is None or scope_allowed is None:
        return "unconfirmed"
    return "zone_confirmed"


def _interface_context(target, user):
    from dcim.models import Device, Interface

    ct = getattr(target, "assigned_object_type", None)
    if ct is None or (ct.app_label, ct.model) != ("dcim", "interface"):
        return None, None
    interface = (
        Interface.objects.restrict(user, "view")
        .filter(pk=target.assigned_object_id)
        .first()
    )
    device = (
        Device.objects.restrict(user, "view").filter(pk=interface.device_id).first()
        if interface
        else None
    )
    return interface, device


def _load_scopes(objects, user, budget):
    """Do not mistake inaccessible assignments for an unassigned/global entry."""
    scopes = {}
    for model, assignment_model, field in (
        (Address, AddressAssignment, "address"),
        (AddressList, AddressListAssignment, "address_list"),
        (AddressSet, AddressSetAssignment, "address_set"),
    ):
        ids = {obj.pk for obj in objects if isinstance(obj, model)}
        if not ids:
            continue
        assignments = assignment_model.objects.filter(**{f"{field}_id__in": ids})
        visible = assignments.restrict(user, "view")
        metadata = budget.take(
            model.objects.restrict(user, "view")
            .filter(pk__in=ids)
            .annotate(
                scope_hidden=Exists(
                    assignments.filter(**{f"{field}_id": OuterRef("pk")}).exclude(
                        pk__in=visible.values("pk")
                    )
                )
            )
            .order_by("pk")
            .values_list("pk", "scope_hidden")
        )
        rows = budget.take(
            visible.order_by("pk").values_list(
                f"{field}_id",
                "assigned_object_type__app_label",
                "assigned_object_type__model",
                "assigned_object_id",
            )
        )
        by_id = defaultdict(list)
        for pk, app, name, target_id in rows:
            by_id[pk].append((app, name, target_id))
        for pk, hidden in metadata:
            scopes[(model._meta.model_name, pk)] = (
                None if hidden or budget.truncated else by_id[pk]
            )
    return scopes


def _path_scope(path, scopes, zone_id, device_id):
    """Each definition on a matched path must be available in this context."""
    labels = set()
    uncertain = False
    for obj in path:
        assignments = scopes.get((obj._meta.model_name, obj.pk))
        if assignments is None:
            uncertain = True
            continue
        if not assignments:
            continue  # Unassigned definitions are global within the plugin.
        allowed = False
        unknown = False
        for app, model, pk in assignments:
            if (app, model) == ("netbox_security", "securityzone"):
                if pk == zone_id:
                    allowed = True
                    labels.add("zone")
            elif (app, model) == ("dcim", "device"):
                if device_id is None:
                    unknown = True
                elif pk == device_id:
                    allowed = True
                    labels.add("device")
            else:
                # VM/VDC scope needs its own independently established context.
                unknown = True
        if not allowed and not unknown:
            return False, "Zone/context-specific"
        if not allowed:
            uncertain = True
    if uncertain:
        return None, "Scope unconfirmed"
    if "zone" in labels:
        return True, "Zone-specific"
    if "device" in labels:
        return True, "Global on this device"
    return True, "Global"


def _policy_details(rows, user, budget):
    """Batch-load visible criteria; never render unrestricted related managers."""
    policy_ids = {row["policy_id"] for row in rows}
    details = {pk: {} for pk in policy_ids}
    for field_name, model in (
        ("source_address", AddressList),
        ("destination_address", AddressList),
        ("applications", Application),
        ("application_sets", ApplicationSet),
    ):
        field = SecurityZonePolicy._meta.get_field(field_name)
        through = field.remote_field.through
        source = f"{field.m2m_field_name()}_id"
        dest = f"{field.m2m_reverse_field_name()}_id"
        objects = model.objects.restrict(user, "view")
        if model is AddressList:
            objects = restrict_generic_assignments(objects, user)
        links = budget.take(
            through.objects.filter(
                **{
                    f"{source}__in": policy_ids,
                    f"{dest}__in": objects.values("pk"),
                }
            )
            .order_by(source, dest)
            .values_list(source, dest)
        )
        object_map = {
            obj.pk: obj for obj in objects.filter(pk__in={pk for _, pk in links})
        }
        for policy_id, pk in links:
            if pk in object_map:
                details[policy_id].setdefault(field_name, []).append(object_map[pk])
    return details


def add_policy_candidates(result, target, *, user):
    budget = HierarchyBudget()
    interface, device = _interface_context(target, user)
    zones = budget.take(
        SecurityZone.objects.restrict(user, "view")
        .filter(pk__in=result["member_zone_ids"])
        .order_by("name", "pk")
    )
    rows = result["policy_paths"]
    objects = list(result["address_objects"]) + list(
        result["inherited_address_objects"]
    )
    objects += list(result.get("address_list_objects", []))
    for row in result["address_set_hierarchy_rows"]:
        objects.extend(obj for obj in row["path"] if obj is not None)
    scopes = _load_scopes(objects, user, budget)
    direct_addresses = {obj.pk: obj for obj in objects if isinstance(obj, Address)}
    # Compact provenance index: retain references to existing bounded paths.
    by_set = defaultdict(list)
    steps = 0
    for row in result["address_set_hierarchy_rows"]:
        for index, obj in enumerate(row["path"]):
            if steps >= budget.limits.steps:
                budget.truncated = True
                break
            steps += 1
            if obj is not None:
                by_set[obj.pk].append((row, index))
        if steps >= budget.limits.steps:
            break
    remaining_steps = budget.limits.steps
    candidates, excluded = [], []
    members = set(result["member_zone_ids"]) if result["zone_context_known"] else None
    for row in rows:
        address_list = row["address_list"]
        target_obj = row["context_object"]
        zone_id = row[f'{row["direction"]}_zone_id']
        scope_allowed, book, matched_path = None, "Scope unconfirmed", []
        if isinstance(target_obj, Address):
            address = direct_addresses.get(target_obj.pk)
            paths = [([address], None)] if address else []
        elif isinstance(target_obj, AddressSet):
            paths = by_set.get(target_obj.pk, [])
        else:
            paths = []
        outcomes = []
        for path_info, index in paths:
            if remaining_steps <= 0:
                budget.truncated = True
                break
            path = (
                path_info["path"][index:] + [path_info["address"]]
                if index is not None
                else path_info
            )
            path = [obj for obj in path if obj is not None]
            remaining_steps -= len(path) + 1
            if remaining_steps < 0:
                budget.truncated = True
                break
            allowed, label = _path_scope(
                [address_list, *path], scopes, zone_id, device.pk if device else None
            )
            outcomes.append(allowed)
            if allowed is True:
                scope_allowed, book, matched_path = True, label, path
                break
        else:
            if (
                outcomes
                and all(value is False for value in outcomes)
                and not (budget.truncated or result["hierarchy_truncated"])
            ):
                scope_allowed, book = False, "Zone/context-specific"
        status = classify_match(zone_id, members, scope_allowed)
        row.update(
            match_status=status,
            address_book=book,
            matched_path=matched_path,
            required_zone=row[f'{row["direction"]}_zone'],
        )
        (
            excluded if status in ("zone_mismatch", "scope_mismatch") else candidates
        ).append(row)
    details = _policy_details(rows, user, budget)
    for row in rows:
        row["criteria"] = details.get(row["policy_id"], {})
    result.update(
        policy_candidates=candidates,
        excluded_policy_candidates=excluded,
        member_zones=zones,
        zone_interface=interface,
        zone_device=device,
        hierarchy_truncated=result["hierarchy_truncated"] or budget.truncated,
    )
    return result
