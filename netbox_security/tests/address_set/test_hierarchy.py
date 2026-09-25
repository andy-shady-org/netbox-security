from django.contrib.auth import get_user_model
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
from netbox_security.utils import get_address_set_hierarchy


class AddressSetHierarchyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="hierarchy-test-user", is_superuser=True
        )
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
            member_zone_ids=[self.source_zone.pk, self.destination_zone.pk],
            user=self.user,
            app_label="ipam",
            model="prefix",
            object_id=self.prefix.pk,
        )

        self.assertEqual(result["assigned_object_id"], self.prefix.pk)
        self.assertIn(self.address.pk, result["address_ids"])
        self.assertEqual(
            [obj.pk for obj in result["address_objects"]], [self.address.pk]
        )

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
        self.assertEqual(len(result["address_set_hierarchy_rows"]), 1)
        self.assertEqual(
            [obj.pk for obj in result["address_set_hierarchy_rows"][0]["path"]],
            [self.root_set.pk, self.leaf_set.pk],
        )
        self.assertEqual(
            result["address_set_hierarchy_rows"][0]["address"].pk,
            self.address.pk,
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
        for row in result["policy_paths"]:
            self.assertIn("context_object", row)
            self.assertIn("address_list", row)
        self.assertTrue(any(row["context_object"] for row in result["policy_paths"]))

    def test_returns_empty_for_unassigned_ipam_object(self):
        unassigned_prefix = Prefix.objects.create(prefix=IPNetwork("10.2.0.0/24"))

        result = get_address_set_hierarchy(
            user=self.user,
            app_label="ipam",
            model="prefix",
            object_id=unassigned_prefix.pk,
        )

        self.assertEqual(result["assigned_object_id"], unassigned_prefix.pk)
        self.assertEqual(result["address_ids"], [])
        self.assertEqual(result["address_objects"], [])
        self.assertEqual(result["direct_address_set_ids"], [])
        self.assertEqual(result["all_address_set_ids"], [])
        self.assertEqual(result["address_set_paths"], [])
        self.assertEqual(result["address_set_hierarchy_rows"], [])
        self.assertEqual(result["address_list_ids"], [])
        self.assertEqual(result["policy_paths"], [])

    def test_returns_empty_for_unknown_content_type(self):
        result = get_address_set_hierarchy(
            user=self.user,
            app_label="not_real",
            model="missing",
            object_id=1,
        )

        self.assertIsNone(result["assigned_object_id"])
        self.assertEqual(result["address_ids"], [])
        self.assertEqual(result["address_objects"], [])
        self.assertEqual(result["direct_address_set_ids"], [])
        self.assertEqual(result["all_address_set_ids"], [])
        self.assertEqual(result["address_set_paths"], [])
        self.assertEqual(result["address_set_hierarchy_rows"], [])
        self.assertEqual(result["address_list_ids"], [])
        self.assertEqual(result["policy_paths"], [])

    def test_returns_empty_for_inaccessible_root(self):
        user = get_user_model().objects.create_user(
            username="restricted-hierarchy-user"
        )

        result = get_address_set_hierarchy(
            user=user,
            app_label="ipam",
            model="prefix",
            object_id=self.prefix.pk,
        )

        self.assertIsNone(result["assigned_object_id"])
        self.assertEqual(result["address_ids"], [])
        self.assertEqual(result["all_address_set_ids"], [])
        self.assertEqual(result["policy_paths"], [])

    def test_branching_hierarchy_is_truncated_and_warns(self):
        from unittest.mock import patch
        from django.template.loader import render_to_string
        from netbox_security.utils.hierarchy_limits import (
            HierarchyBudget,
            HierarchyLimits,
        )

        other_root = AddressSet.objects.create(name="other-root")
        other_root.address_sets.add(self.leaf_set)
        budget = HierarchyBudget(HierarchyLimits(paths=1))
        with patch(
            "netbox_security.utils.address_set_hierarchy.HierarchyBudget",
            return_value=budget,
        ):
            result = get_address_set_hierarchy(
                user=self.user,
                app_label="ipam",
                model="prefix",
                object_id=self.prefix.pk,
            )
        self.assertTrue(result["hierarchy_truncated"])
        self.assertEqual(len(result["address_set_paths"]), 1)
        html = render_to_string(
            "netbox_security/inc/hierarchy_warning.html", {"policy_context": result}
        )
        self.assertIn("not a complete list", html)

    def test_deep_hierarchy_discovery_is_bounded(self):
        from unittest.mock import patch
        from netbox_security.utils.hierarchy_limits import (
            HierarchyBudget,
            HierarchyLimits,
        )

        child = self.root_set
        for index in range(8):
            parent = AddressSet.objects.create(name=f"deep-parent-{index}")
            parent.address_sets.add(child)
            child = parent
        with patch(
            "netbox_security.utils.address_set_hierarchy.HierarchyBudget",
            return_value=HierarchyBudget(HierarchyLimits(depth=3)),
        ):
            result = get_address_set_hierarchy(
                user=self.user,
                app_label="ipam",
                model="prefix",
                object_id=self.prefix.pk,
            )
        self.assertTrue(result["hierarchy_truncated"])
        self.assertEqual(len(result["all_address_set_ids"]), 3)
        self.assertTrue(all(len(path) <= 3 for path in result["address_set_paths"]))

    def test_address_path_multiplication_is_bounded(self):
        from unittest.mock import patch
        from netbox_security.utils.hierarchy_limits import (
            HierarchyBudget,
            HierarchyLimits,
        )

        for index in range(4):
            parent = AddressSet.objects.create(name=f"wide-parent-{index}")
            parent.address_sets.add(self.leaf_set)
        for index in range(2):
            address = Address.objects.create(
                name=f"extra-address-{index}",
                assigned_object_type=self.address.assigned_object_type,
                assigned_object_id=self.prefix.pk,
            )
            self.leaf_set.addresses.add(address)
        with patch(
            "netbox_security.utils.address_set_hierarchy.HierarchyBudget",
            return_value=HierarchyBudget(HierarchyLimits(rows=4)),
        ):
            result = get_address_set_hierarchy(
                user=self.user,
                app_label="ipam",
                model="prefix",
                object_id=self.prefix.pk,
            )
        self.assertTrue(result["hierarchy_truncated"])
        self.assertEqual(len(result["address_set_hierarchy_rows"]), 4)
        self.assertLessEqual(len(result["policy_paths"]), 4)

    def test_badge_does_not_expand_hierarchy(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        from netbox.context import current_request
        from netbox_security.views.tabs import _prefix_related_total_count

        token = current_request.set(SimpleNamespace(user=self.user))
        try:
            with patch(
                "netbox_security.views.tabs.get_address_set_hierarchy",
                side_effect=AssertionError("Badge must not expand hierarchy"),
            ):
                self.assertGreaterEqual(_prefix_related_total_count(self.prefix), 1)
        finally:
            current_request.reset(token)
