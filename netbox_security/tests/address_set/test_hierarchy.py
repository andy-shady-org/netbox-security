from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from netaddr import IPNetwork

from ipam.models import Prefix
from netbox_security.models import (
    Address,
    AddressList,
    AddressSet,
    SecurityZone,
    SecurityZonePolicy,
)
from netbox_security.utilities import get_address_set_hierarchy


class AddressSetHierarchyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prefix = Prefix.objects.create(prefix=IPNetwork("10.1.0.0/24"))
        cls.address = Address.objects.create(
            name="prefix-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="prefix",
            ),
            assigned_object_id=cls.prefix.pk,
        )

        cls.root_set = AddressSet.objects.create(name="root-set")
        cls.leaf_set = AddressSet.objects.create(name="leaf-set")
        cls.root_set.address_sets.add(cls.leaf_set)
        cls.leaf_set.addresses.add(cls.address)

        address_ct = ContentType.objects.get_for_model(Address)
        address_set_ct = ContentType.objects.get_for_model(AddressSet)

        cls.list_from_address = AddressList.objects.create(
            name="list-from-address",
            assigned_object_type=address_ct,
            assigned_object_id=cls.address.pk,
        )
        cls.list_from_root_set = AddressList.objects.create(
            name="list-from-root-set",
            assigned_object_type=address_set_ct,
            assigned_object_id=cls.root_set.pk,
        )

        cls.source_zone = SecurityZone.objects.create(name="source-zone")
        cls.destination_zone = SecurityZone.objects.create(name="destination-zone")

        cls.policy_source = SecurityZonePolicy.objects.create(
            name="policy-source",
            index=10,
            source_zone=cls.source_zone,
            destination_zone=cls.destination_zone,
            policy_actions=["permit"],
        )
        cls.policy_source.source_address.add(cls.list_from_root_set)

        cls.policy_destination = SecurityZonePolicy.objects.create(
            name="policy-destination",
            index=20,
            source_zone=cls.source_zone,
            destination_zone=cls.destination_zone,
            policy_actions=["permit"],
        )
        cls.policy_destination.destination_address.add(cls.list_from_address)

    def test_returns_transitive_addressset_and_policy_context(self):
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="prefix",
            object_id=self.prefix.pk,
        )

        self.assertEqual(result["assigned_object_id"], self.prefix.pk)
        self.assertIn(self.address.pk, result["address_ids"])

        self.assertEqual(
            set(result["direct_address_set_ids"]),
            {self.leaf_set.pk},
        )
        self.assertEqual(
            set(result["all_address_set_ids"]),
            {self.root_set.pk, self.leaf_set.pk},
        )
        self.assertEqual(
            {tuple(path) for path in result["address_set_paths"]},
            {(self.root_set.pk, self.leaf_set.pk)},
        )

        self.assertEqual(
            set(result["address_list_ids"]),
            {self.list_from_address.pk, self.list_from_root_set.pk},
        )

        policy_markers = {
            (row["policy_id"], row["direction"]) for row in result["policy_paths"]
        }
        self.assertEqual(
            policy_markers,
            {
                (self.policy_source.pk, "source"),
                (self.policy_destination.pk, "destination"),
            },
        )

    def test_returns_empty_for_unassigned_ipam_object(self):
        unassigned_prefix = Prefix.objects.create(prefix=IPNetwork("10.2.0.0/24"))

        result = get_address_set_hierarchy(
            app_label="ipam",
            model="prefix",
            object_id=unassigned_prefix.pk,
        )

        self.assertEqual(result["assigned_object_id"], unassigned_prefix.pk)
        self.assertEqual(result["address_ids"], [])
        self.assertEqual(result["direct_address_set_ids"], [])
        self.assertEqual(result["all_address_set_ids"], [])
        self.assertEqual(result["address_set_paths"], [])
        self.assertEqual(result["address_list_ids"], [])
        self.assertEqual(result["policy_paths"], [])

    def test_returns_empty_for_unknown_content_type(self):
        result = get_address_set_hierarchy(
            app_label="not_real",
            model="missing",
            object_id=1,
        )

        self.assertIsNone(result["assigned_object_id"])
        self.assertEqual(result["address_ids"], [])
        self.assertEqual(result["direct_address_set_ids"], [])
        self.assertEqual(result["all_address_set_ids"], [])
        self.assertEqual(result["address_set_paths"], [])
        self.assertEqual(result["address_list_ids"], [])
        self.assertEqual(result["policy_paths"], [])
