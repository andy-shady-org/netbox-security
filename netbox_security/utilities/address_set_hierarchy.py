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
            "direct_address_set_ids": [],
            "all_address_set_ids": [],
            "address_set_paths": [],
            "address_set_object_paths": [],
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
            "direct_address_set_ids": [],
            "all_address_set_ids": [],
            "address_set_paths": [],
            "address_set_object_paths": [],
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
    for direct_id in sorted(direct_address_set_ids):
        addressset_paths.extend(build_addressset_paths(direct_id))
    unique_addressset_paths = sorted({tuple(path) for path in addressset_paths})
    address_set_object_map = {
        obj.pk: obj for obj in AddressSet.objects.filter(id__in=all_address_set_ids)
    }

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

        for policy in source_policies:
            policy_object_map[policy.pk] = policy
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
                }
            )
        for policy in destination_policies:
            policy_object_map[policy.pk] = policy
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
            )
            for row in policy_rows
        }
    )

    return {
        "assigned_object_id": object_id,
        "address_ids": sorted(address_ids),
        "direct_address_set_ids": sorted(direct_address_set_ids),
        "all_address_set_ids": sorted(all_address_set_ids),
        "address_set_paths": [list(path) for path in unique_addressset_paths],
        "address_set_object_paths": [
            [address_set_object_map.get(address_set_id) for address_set_id in path]
            for path in unique_addressset_paths
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
