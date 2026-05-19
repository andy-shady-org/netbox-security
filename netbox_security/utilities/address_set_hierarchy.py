from collections import defaultdict

from django.contrib.contenttypes.models import ContentType

from netbox_security.models import Address, AddressList, AddressSet, SecurityZonePolicy


def get_address_set_hierarchy(*, app_label, model, object_id):
    """Return transitive security context for an assigned IPAM object.

    Traversal:
    assigned object -> Address -> AddressSet (direct + parent hierarchy) ->
    AddressList -> SecurityZonePolicy (source/destination)
    """
    content_type = ContentType.objects.filter(app_label=app_label, model=model).first()
    if not content_type:
        return {
            "assigned_object_id": None,
            "address_ids": [],
            "address_objects": [],
            "direct_address_set_ids": [],
            "all_address_set_ids": [],
            "address_set_paths": [],
            "address_set_object_paths": [],
            "address_set_hierarchy_rows": [],
            "address_set_name_paths": [],
            "address_list_ids": [],
            "address_list_names": [],
            "policy_paths": [],
        }

    address_ids = list(
        Address.objects.filter(
            assigned_object_type=content_type,
            assigned_object_id=object_id,
        ).values_list("id", flat=True)
    )
    if not address_ids:
        return {
            "assigned_object_id": object_id,
            "address_ids": [],
            "address_objects": [],
            "direct_address_set_ids": [],
            "all_address_set_ids": [],
            "address_set_paths": [],
            "address_set_object_paths": [],
            "address_set_hierarchy_rows": [],
            "address_set_name_paths": [],
            "address_list_ids": [],
            "address_list_names": [],
            "policy_paths": [],
        }

    direct_address_set_ids = set(
        AddressSet.objects.filter(addresses__id__in=address_ids)
        .values_list("id", flat=True)
        .distinct()
    )

    relation_field = AddressSet._meta.get_field("address_sets")
    parent_field = relation_field.m2m_field_name()
    child_field = relation_field.m2m_reverse_field_name()
    through_model = relation_field.remote_field.through

    parent_map = defaultdict(set)
    all_address_set_ids = set(direct_address_set_ids)
    frontier = set(direct_address_set_ids)

    while frontier:
        relation_rows = through_model.objects.filter(
            **{f"{child_field}_id__in": list(frontier)}
        ).values_list(f"{parent_field}_id", f"{child_field}_id")

        new_frontier = set()
        for parent_id, child_id in relation_rows:
            parent_map[child_id].add(parent_id)
            if parent_id not in all_address_set_ids:
                all_address_set_ids.add(parent_id)
                new_frontier.add(parent_id)

        frontier = new_frontier

    def build_addressset_paths(child_id, trail=None):
        if trail is None:
            trail = set()
        if child_id in trail:
            return []

        parents = sorted(parent_map.get(child_id, ()))
        if not parents:
            return [[child_id]]

        paths = []
        for parent_id in parents:
            for parent_path in build_addressset_paths(parent_id, trail | {child_id}):
                paths.append([*parent_path, child_id])
        return paths

    addressset_paths = []
    paths_by_direct_set = {}
    for direct_id in sorted(direct_address_set_ids):
        direct_paths = build_addressset_paths(direct_id)
        paths_by_direct_set[direct_id] = direct_paths
        addressset_paths.extend(direct_paths)
    unique_addressset_paths = sorted({tuple(path) for path in addressset_paths})
    direct_memberships = (
        AddressSet.objects.filter(addresses__id__in=address_ids)
        .values_list("addresses__id", "id")
        .distinct()
    )
    direct_sets_by_address = defaultdict(set)
    for address_id, address_set_id in direct_memberships:
        direct_sets_by_address[address_id].add(address_set_id)

    address_object_map = {
        obj.pk: obj for obj in Address.objects.filter(id__in=address_ids)
    }
    address_set_object_map = {
        obj.pk: obj for obj in AddressSet.objects.filter(id__in=all_address_set_ids)
    }

    hierarchy_rows = set()
    for address_id in sorted(address_ids):
        for direct_set_id in sorted(direct_sets_by_address.get(address_id, ())):
            for path in paths_by_direct_set.get(direct_set_id, [[direct_set_id]]):
                hierarchy_rows.add((tuple(path), address_id))
    sorted_hierarchy_rows = sorted(hierarchy_rows)

    address_ct = ContentType.objects.get_for_model(Address)
    address_set_ct = ContentType.objects.get_for_model(AddressSet)

    address_list_ids = set(
        AddressList.objects.filter(
            assigned_object_type=address_ct,
            assigned_object_id__in=address_ids,
        ).values_list("id", flat=True)
    )
    if all_address_set_ids:
        address_list_ids.update(
            AddressList.objects.filter(
                assigned_object_type=address_set_ct,
                assigned_object_id__in=all_address_set_ids,
            ).values_list("id", flat=True)
        )
    address_list_object_map = {
        obj.pk: obj for obj in AddressList.objects.filter(id__in=address_list_ids)
    }

    policy_rows = []
    policy_object_map = {}
    if address_list_ids:
        source_policies = SecurityZonePolicy.objects.filter(
            source_address__id__in=address_list_ids
        ).distinct()
        destination_policies = SecurityZonePolicy.objects.filter(
            destination_address__id__in=address_list_ids
        ).distinct()

        source_policy_ids = set(source_policies.values_list("id", flat=True))
        destination_policy_ids = set(destination_policies.values_list("id", flat=True))

        for policy in source_policies:
            policy_object_map[policy.pk] = policy
        for policy in destination_policies:
            policy_object_map[policy.pk] = policy

        source_links = SecurityZonePolicy.source_address.through.objects.filter(
            securityzonepolicy_id__in=source_policy_ids,
            addresslist_id__in=address_list_ids,
        ).values_list("securityzonepolicy_id", "addresslist_id")
        destination_links = (
            SecurityZonePolicy.destination_address.through.objects.filter(
                securityzonepolicy_id__in=destination_policy_ids,
                addresslist_id__in=address_list_ids,
            ).values_list("securityzonepolicy_id", "addresslist_id")
        )

        for policy_id, address_list_id in source_links:
            policy = policy_object_map.get(policy_id)
            address_list = address_list_object_map.get(address_list_id)
            if not policy:
                continue
            policy_rows.append(
                {
                    "policy_id": policy.pk,
                    "policy_name": policy.name,
                    "policy_index": policy.index,
                    "policy_actions": list(policy.policy_actions or []),
                    "direction": "source",
                    "source_zone_id": policy.source_zone_id,
                    "destination_zone_id": policy.destination_zone_id,
                    "source_zone_name": policy.source_zone.name,
                    "destination_zone_name": policy.destination_zone.name,
                    "address_list_id": address_list_id,
                    "address_list_name": address_list.name if address_list else "",
                    "context_model": (
                        address_list.assigned_object_type.model
                        if address_list and address_list.assigned_object_type_id
                        else ""
                    ),
                    "context_object_id": (
                        address_list.assigned_object_id
                        if address_list and address_list.assigned_object_id
                        else 0
                    ),
                }
            )

        for policy_id, address_list_id in destination_links:
            policy = policy_object_map.get(policy_id)
            address_list = address_list_object_map.get(address_list_id)
            if not policy:
                continue
            policy_rows.append(
                {
                    "policy_id": policy.pk,
                    "policy_name": policy.name,
                    "policy_index": policy.index,
                    "policy_actions": list(policy.policy_actions or []),
                    "direction": "destination",
                    "source_zone_id": policy.source_zone_id,
                    "destination_zone_id": policy.destination_zone_id,
                    "source_zone_name": policy.source_zone.name,
                    "destination_zone_name": policy.destination_zone.name,
                    "address_list_id": address_list_id,
                    "address_list_name": address_list.name if address_list else "",
                    "context_model": (
                        address_list.assigned_object_type.model
                        if address_list and address_list.assigned_object_type_id
                        else ""
                    ),
                    "context_object_id": (
                        address_list.assigned_object_id
                        if address_list and address_list.assigned_object_id
                        else 0
                    ),
                }
            )

    unique_policy_rows = sorted(
        {
            (
                row["policy_id"],
                row["policy_name"],
                row["policy_index"],
                tuple(row["policy_actions"]),
                row["direction"],
                row["source_zone_id"],
                row["destination_zone_id"],
                row["source_zone_name"],
                row["destination_zone_name"],
                row["address_list_id"],
                row["address_list_name"],
                row["context_model"],
                row["context_object_id"],
            )
            for row in policy_rows
        }
    )

    return {
        "assigned_object_id": object_id,
        "address_ids": sorted(address_ids),
        "address_objects": list(
            Address.objects.filter(id__in=address_ids).order_by("name", "pk")
        ),
        "direct_address_set_ids": sorted(direct_address_set_ids),
        "all_address_set_ids": sorted(all_address_set_ids),
        "address_set_paths": [list(path) for path in unique_addressset_paths],
        "address_set_object_paths": [
            [address_set_object_map.get(address_set_id) for address_set_id in path]
            for path in unique_addressset_paths
        ],
        "address_set_hierarchy_rows": [
            {
                "path": [
                    address_set_object_map.get(address_set_id)
                    for address_set_id in path
                ],
                "address": address_object_map.get(address_id),
            }
            for path, address_id in sorted_hierarchy_rows
        ],
        "address_set_name_paths": [
            [
                (
                    address_set_object_map.get(address_set_id).name
                    if address_set_object_map.get(address_set_id)
                    else str(address_set_id)
                )
                for address_set_id in path
            ]
            for path in unique_addressset_paths
        ],
        "address_list_ids": sorted(address_list_ids),
        "address_list_objects": [
            address_list_object_map[address_list_id]
            for address_list_id in sorted(address_list_ids)
            if address_list_id in address_list_object_map
        ],
        "address_list_names": [
            address_list_object_map[address_list_id].name
            for address_list_id in sorted(address_list_ids)
            if address_list_id in address_list_object_map
        ],
        "policy_paths": [
            {
                "policy_id": row[0],
                "policy_name": row[1],
                "policy_index": row[2],
                "policy_actions": list(row[3]),
                "direction": row[4],
                "source_zone_id": row[5],
                "destination_zone_id": row[6],
                "source_zone_name": row[7],
                "destination_zone_name": row[8],
                "address_list_id": row[9],
                "address_list_name": row[10],
                "address_list": address_list_object_map.get(row[9]),
                "context_model": row[11],
                "context_object_id": row[12],
                "context_object": (
                    address_list_object_map.get(row[9]).assigned_object
                    if address_list_object_map.get(row[9])
                    else None
                ),
                "policy": policy_object_map.get(row[0]),
                "source_zone": (
                    policy_object_map.get(row[0]).source_zone
                    if policy_object_map.get(row[0])
                    else None
                ),
                "destination_zone": (
                    policy_object_map.get(row[0]).destination_zone
                    if policy_object_map.get(row[0])
                    else None
                ),
            }
            for row in unique_policy_rows
        ],
    }
