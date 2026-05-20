"""Tests for inherited address functionality in Security Policy Context."""

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from netaddr import IPNetwork

from ipam.models import IPAddress, IPRange, Prefix
from netbox_security.models import (
    Address,
    AddressList,
    AddressSet,
    CustomPrefix,
    SecurityZone,
    SecurityZonePolicy,
)
from netbox_security.utilities import get_address_set_hierarchy


class PrefixInheritedAddressTestCase(TestCase):
    """Test that child prefixes inherit addresses from parent prefixes."""

    @classmethod
    def setUpTestData(cls):
        # Create parent and child prefixes
        cls.parent_prefix = Prefix.objects.create(prefix=IPNetwork("10.0.0.0/8"))
        cls.child_prefix = Prefix.objects.create(prefix=IPNetwork("10.1.0.0/24"))
        # A child prefix with NO direct address assignment at all
        cls.child_prefix_no_direct = Prefix.objects.create(
            prefix=IPNetwork("10.2.0.0/24")
        )

        # Create address assigned to parent
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="prefix",
            ),
            assigned_object_id=cls.parent_prefix.pk,
        )

        # Create address assigned to child
        cls.child_address = Address.objects.create(
            name="child-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="prefix",
            ),
            assigned_object_id=cls.child_prefix.pk,
        )

        # Create address sets
        cls.parent_set = AddressSet.objects.create(name="parent-set")
        cls.parent_set.addresses.add(cls.parent_address)

        cls.child_set = AddressSet.objects.create(name="child-set")
        cls.child_set.addresses.add(cls.child_address)

    def test_child_prefix_inherits_parent_addresses(self):
        """Child prefix should show both direct and inherited addresses."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="prefix",
            object_id=self.child_prefix.pk,
        )

        # Should have direct address
        self.assertIn(self.child_address.pk, result["address_ids"])
        self.assertEqual(
            [obj.pk for obj in result["address_objects"]], [self.child_address.pk]
        )

        # Should have inherited address from parent
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])
        self.assertEqual(
            [obj.pk for obj in result["inherited_address_objects"]],
            [self.parent_address.pk],
        )

    def test_child_prefix_no_direct_address_inherits_parent_addresses(self):
        """Child prefix with no direct address should still show inherited addresses."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="prefix",
            object_id=self.child_prefix_no_direct.pk,
        )

        # No direct addresses
        self.assertEqual(result["address_ids"], [])
        self.assertEqual(result["address_objects"], [])

        # Should still have inherited address from parent
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])
        self.assertGreater(len(result["inherited_address_objects"]), 0)

    def test_parent_prefix_shows_own_addresses_not_inherited(self):
        """Parent prefix should not show child addresses as inherited."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="prefix",
            object_id=self.parent_prefix.pk,
        )

        # Should have direct address
        self.assertIn(self.parent_address.pk, result["address_ids"])

        # Should not have child address
        self.assertNotIn(self.child_address.pk, result["address_ids"])
        self.assertEqual(result["inherited_address_ids"], [])


class IPAddressInheritedAddressTestCase(TestCase):
    """Test that IP addresses inherit addresses from parent prefixes."""

    @classmethod
    def setUpTestData(cls):
        # Create parent prefix
        cls.parent_prefix = Prefix.objects.create(prefix=IPNetwork("10.1.0.0/24"))

        # IP address within the prefix that has a direct Address assignment
        cls.ip_address_with_direct = IPAddress.objects.create(
            address=IPNetwork("10.1.0.5/24")
        )

        # IP address within the prefix with NO direct Address assignment
        cls.ip_address_no_direct = IPAddress.objects.create(
            address=IPNetwork("10.1.0.6/24")
        )

        # Create address assigned to parent prefix
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="prefix",
            ),
            assigned_object_id=cls.parent_prefix.pk,
        )

        # Create address assigned directly to the IP address
        cls.ip_direct_address = Address.objects.create(
            name="ip-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="ipaddress",
            ),
            assigned_object_id=cls.ip_address_with_direct.pk,
        )

    def test_ip_address_with_direct_also_inherits_parent(self):
        """IP address with a direct assignment should also show inherited parent addresses."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="ipaddress",
            object_id=self.ip_address_with_direct.pk,
        )

        self.assertIn(self.ip_direct_address.pk, result["address_ids"])
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])

    def test_ip_address_no_direct_inherits_parent(self):
        """IP address with NO direct assignment should show inherited parent addresses."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="ipaddress",
            object_id=self.ip_address_no_direct.pk,
        )

        # No direct addresses
        self.assertEqual(result["address_ids"], [])
        self.assertEqual(result["address_objects"], [])

        # Should still inherit from parent prefix
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])
        self.assertGreater(len(result["inherited_address_objects"]), 0)


class IPRangeInheritedAddressTestCase(TestCase):
    """Test that IP ranges inherit addresses from parent prefixes."""

    @classmethod
    def setUpTestData(cls):
        # Create parent prefix
        cls.parent_prefix = Prefix.objects.create(prefix=IPNetwork("10.1.0.0/24"))

        # IP range fully inside the prefix, with NO direct Address assignment
        cls.ip_range_no_direct = IPRange.objects.create(
            start_address=IPNetwork("10.1.0.10/24"),
            end_address=IPNetwork("10.1.0.20/24"),
        )

        # Create address assigned to parent prefix
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="prefix",
            ),
            assigned_object_id=cls.parent_prefix.pk,
        )

    def test_ip_range_no_direct_inherits_parent(self):
        """IP range with NO direct assignment should show inherited parent prefix addresses."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="iprange",
            object_id=self.ip_range_no_direct.pk,
        )

        # No direct addresses
        self.assertEqual(result["address_ids"], [])

        # Should inherit from parent prefix
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])


class InheritedAddressSetHierarchyTestCase(TestCase):
    """Test that inherited addresses are included in address set hierarchy."""

    @classmethod
    def setUpTestData(cls):
        # Create parent and child prefixes
        cls.parent_prefix = Prefix.objects.create(prefix=IPNetwork("10.0.0.0/8"))
        cls.child_prefix = Prefix.objects.create(prefix=IPNetwork("10.1.0.0/24"))

        # Create address assigned to parent
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="prefix",
            ),
            assigned_object_id=cls.parent_prefix.pk,
        )

        # Create address set hierarchy
        cls.root_set = AddressSet.objects.create(name="root-set")
        cls.leaf_set = AddressSet.objects.create(name="leaf-set")
        cls.root_set.address_sets.add(cls.leaf_set)
        cls.leaf_set.addresses.add(cls.parent_address)

    def test_child_prefix_shows_inherited_address_set_hierarchy(self):
        """Child prefix should show address set hierarchy for inherited addresses."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="prefix",
            object_id=self.child_prefix.pk,
        )

        # Should have inherited address from parent
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])

        # Should have address set hierarchy rows (transitive)
        hierarchy_rows = result["address_set_hierarchy_rows"]
        self.assertTrue(len(hierarchy_rows) > 0)

        # Verify the hierarchy includes the root and leaf sets
        address_set_ids_in_rows = set()
        for row in hierarchy_rows:
            for address_set in row["path"]:
                if address_set:
                    address_set_ids_in_rows.add(address_set.pk)

        self.assertIn(self.root_set.pk, address_set_ids_in_rows)
        self.assertIn(self.leaf_set.pk, address_set_ids_in_rows)


class InheritedAddressPolicyContextTestCase(TestCase):
    """Test that inherited addresses are used in policy context."""

    @classmethod
    def setUpTestData(cls):
        # Create parent and child prefixes
        cls.parent_prefix = Prefix.objects.create(prefix=IPNetwork("10.0.0.0/8"))
        cls.child_prefix = Prefix.objects.create(prefix=IPNetwork("10.1.0.0/24"))

        # Create address assigned to parent
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="ipam",
                model="prefix",
            ),
            assigned_object_id=cls.parent_prefix.pk,
        )

        # Create address set
        cls.address_set = AddressSet.objects.create(name="address-set")
        cls.address_set.addresses.add(cls.parent_address)

        # Create address list
        address_set_ct = ContentType.objects.get_for_model(AddressSet)
        cls.address_list = AddressList.objects.create(
            name="policy-list",
            assigned_object_type=address_set_ct,
            assigned_object_id=cls.address_set.pk,
        )

        # Create security zones and policy
        cls.source_zone = SecurityZone.objects.create(name="source-zone")
        cls.destination_zone = SecurityZone.objects.create(name="dest-zone")
        cls.policy = SecurityZonePolicy.objects.create(
            name="test-policy",
            index=10,
            source_zone=cls.source_zone,
            destination_zone=cls.destination_zone,
            policy_actions=["permit"],
        )
        cls.policy.source_address.add(cls.address_list)

    def test_child_prefix_shows_policy_from_inherited_addresses(self):
        """Child prefix should show policy derived from inherited addresses."""
        result = get_address_set_hierarchy(
            app_label="ipam",
            model="prefix",
            object_id=self.child_prefix.pk,
        )

        # Should have policy paths
        policy_paths = result["policy_paths"]
        self.assertTrue(len(policy_paths) > 0)

        # Verify the policy is included
        policy_ids = [p["policy_id"] for p in policy_paths]
        self.assertIn(self.policy.pk, policy_ids)


class CustomPrefixInheritedAddressTestCase(TestCase):
    """Test that child custom prefixes inherit addresses from parent custom prefixes."""

    @classmethod
    def setUpTestData(cls):
        # Create parent and child custom prefixes
        cls.parent_custom_prefix = CustomPrefix.objects.create(
            prefix=IPNetwork("10.0.0.0/8")
        )
        cls.child_custom_prefix = CustomPrefix.objects.create(
            prefix=IPNetwork("10.1.0.0/24")
        )

        # Create address assigned to parent
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="netbox_security",
                model="customprefix",
            ),
            assigned_object_id=cls.parent_custom_prefix.pk,
        )

        # Create address assigned to child
        cls.child_address = Address.objects.create(
            name="child-address",
            assigned_object_type=ContentType.objects.get(
                app_label="netbox_security",
                model="customprefix",
            ),
            assigned_object_id=cls.child_custom_prefix.pk,
        )

    def test_child_custom_prefix_inherits_parent_addresses(self):
        """Child custom prefix should show both direct and inherited addresses."""
        result = get_address_set_hierarchy(
            app_label="netbox_security",
            model="customprefix",
            object_id=self.child_custom_prefix.pk,
        )

        # Should have direct address
        self.assertIn(self.child_address.pk, result["address_ids"])
        self.assertEqual(
            [obj.pk for obj in result["address_objects"]], [self.child_address.pk]
        )

        # Should have inherited address from parent
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])
        self.assertEqual(
            [obj.pk for obj in result["inherited_address_objects"]],
            [self.parent_address.pk],
        )

    def test_parent_custom_prefix_shows_own_addresses_not_inherited(self):
        """Parent custom prefix should not show child addresses as inherited."""
        result = get_address_set_hierarchy(
            app_label="netbox_security",
            model="customprefix",
            object_id=self.parent_custom_prefix.pk,
        )

        # Should have direct address
        self.assertIn(self.parent_address.pk, result["address_ids"])

        # Should not have child address
        self.assertNotIn(self.child_address.pk, result["address_ids"])
        self.assertEqual(result["inherited_address_ids"], [])


class CustomPrefixInheritedAddressSetHierarchyTestCase(TestCase):
    """Test that inherited addresses from custom prefixes are included in hierarchy."""

    @classmethod
    def setUpTestData(cls):
        # Create parent and child custom prefixes
        cls.parent_custom_prefix = CustomPrefix.objects.create(
            prefix=IPNetwork("10.0.0.0/8")
        )
        cls.child_custom_prefix = CustomPrefix.objects.create(
            prefix=IPNetwork("10.1.0.0/24")
        )

        # Create address assigned to parent
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="netbox_security",
                model="customprefix",
            ),
            assigned_object_id=cls.parent_custom_prefix.pk,
        )

        # Create address set hierarchy
        cls.root_set = AddressSet.objects.create(name="root-set")
        cls.leaf_set = AddressSet.objects.create(name="leaf-set")
        cls.root_set.address_sets.add(cls.leaf_set)
        cls.leaf_set.addresses.add(cls.parent_address)

    def test_child_custom_prefix_shows_inherited_address_set_hierarchy(self):
        """Child custom prefix should show address set hierarchy for inherited addresses."""
        result = get_address_set_hierarchy(
            app_label="netbox_security",
            model="customprefix",
            object_id=self.child_custom_prefix.pk,
        )

        # Should have inherited address from parent
        self.assertIn(self.parent_address.pk, result["inherited_address_ids"])

        # Should have address set hierarchy rows (transitive)
        hierarchy_rows = result["address_set_hierarchy_rows"]
        self.assertTrue(len(hierarchy_rows) > 0)

        # Verify the hierarchy includes the root and leaf sets
        address_set_ids_in_rows = set()
        for row in hierarchy_rows:
            for address_set in row["path"]:
                if address_set:
                    address_set_ids_in_rows.add(address_set.pk)

        self.assertIn(self.root_set.pk, address_set_ids_in_rows)
        self.assertIn(self.leaf_set.pk, address_set_ids_in_rows)


class CustomPrefixInheritedAddressPolicyContextTestCase(TestCase):
    """Test that inherited addresses from custom prefixes are used in policy context."""

    @classmethod
    def setUpTestData(cls):
        # Create parent and child custom prefixes
        cls.parent_custom_prefix = CustomPrefix.objects.create(
            prefix=IPNetwork("10.0.0.0/8")
        )
        cls.child_custom_prefix = CustomPrefix.objects.create(
            prefix=IPNetwork("10.1.0.0/24")
        )

        # Create address assigned to parent
        cls.parent_address = Address.objects.create(
            name="parent-address",
            assigned_object_type=ContentType.objects.get(
                app_label="netbox_security",
                model="customprefix",
            ),
            assigned_object_id=cls.parent_custom_prefix.pk,
        )

        # Create address set
        cls.address_set = AddressSet.objects.create(name="address-set")
        cls.address_set.addresses.add(cls.parent_address)

        # Create address list
        address_set_ct = ContentType.objects.get_for_model(AddressSet)
        cls.address_list = AddressList.objects.create(
            name="policy-list",
            assigned_object_type=address_set_ct,
            assigned_object_id=cls.address_set.pk,
        )

        # Create security zones and policy
        cls.source_zone = SecurityZone.objects.create(name="source-zone")
        cls.destination_zone = SecurityZone.objects.create(name="dest-zone")
        cls.policy = SecurityZonePolicy.objects.create(
            name="test-policy",
            index=10,
            source_zone=cls.source_zone,
            destination_zone=cls.destination_zone,
            policy_actions=["permit"],
        )
        cls.policy.source_address.add(cls.address_list)

    def test_child_custom_prefix_shows_policy_from_inherited_addresses(self):
        """Child custom prefix should show policy derived from inherited addresses."""
        result = get_address_set_hierarchy(
            app_label="netbox_security",
            model="customprefix",
            object_id=self.child_custom_prefix.pk,
        )

        # Should have policy paths
        policy_paths = result["policy_paths"]
        self.assertTrue(len(policy_paths) > 0)

        # Verify the policy is included
        policy_ids = [p["policy_id"] for p in policy_paths]
        self.assertIn(self.policy.pk, policy_ids)
