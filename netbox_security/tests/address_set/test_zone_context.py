from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site
from ipam.models import IPAddress, Prefix
from users.models import ObjectPermission

from netbox_security.models import (
    Address,
    AddressList,
    CustomPrefix,
    SecurityZone,
    SecurityZoneAssignment,
    SecurityZonePolicy,
)
from netbox_security.utils import get_address_set_hierarchy


@override_settings(EXEMPT_VIEW_PERMISSIONS=[])
class PolicyZoneContextTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="zone-context-admin", is_superuser=True
        )
        site = Site.objects.create(name="zone-site", slug="zone-site")
        maker = Manufacturer.objects.create(name="zone-maker", slug="zone-maker")
        device_type = DeviceType.objects.create(
            manufacturer=maker, model="zone-type", slug="zone-type"
        )
        role = DeviceRole.objects.create(name="zone-role", slug="zone-role")
        device = Device.objects.create(
            name="zone-device", site=site, device_type=device_type, role=role
        )
        cls.interface = Interface.objects.create(
            device=device, name="zone-interface", type="virtual"
        )
        cls.ip = IPAddress.objects.create(
            address="172.16.2.1/24", assigned_object=cls.interface
        )
        cls.prefix = Prefix.objects.create(prefix="172.16.2.0/24")
        cls.any_prefix = CustomPrefix.objects.create(prefix="0.0.0.0/0")
        cls.host = IPAddress.objects.create(address="172.16.1.1/24")
        cls.zone_x = SecurityZone.objects.create(name="X")
        cls.trust = SecurityZone.objects.create(name="trust")
        cls.untrust = SecurityZone.objects.create(name="untrust")
        cls.membership = SecurityZoneAssignment.objects.create(
            zone=cls.zone_x, assigned_object=cls.interface
        )
        cls.lists = []
        for name, target in (
            ("any", cls.any_prefix),
            ("X-prefix", cls.prefix),
            ("host", cls.host),
        ):
            address = Address.objects.create(name=name, assigned_object=target)
            cls.lists.append(
                AddressList.objects.create(name=name, assigned_object=address)
            )
        cls.any_address = cls.lists[0].assigned_object
        cls.policies = []
        for index, (source, destination, src_list, dst_list) in enumerate(
            (
                (cls.trust, cls.untrust, cls.lists[0], cls.lists[2]),
                (cls.zone_x, cls.trust, cls.lists[1], cls.lists[2]),
                (cls.trust, cls.zone_x, cls.lists[0], cls.lists[1]),
            )
        ):
            policy = SecurityZonePolicy.objects.create(
                name=f"zone-policy-{index}",
                index=index,
                source_zone=source,
                destination_zone=destination,
                policy_actions=["permit"],
            )
            policy.source_address.add(src_list)
            policy.destination_address.add(dst_list)
            cls.policies.append(policy)

    def context(self, **kwargs):
        return get_address_set_hierarchy(
            user=self.user,
            app_label="ipam",
            model="ipaddress",
            object_id=self.ip.pk,
            **kwargs,
        )

    def test_wildcard_does_not_override_interface_zone(self):
        result = self.context()
        self.assertTrue(result["zone_context_known"])
        self.assertEqual(result["member_zone_ids"], [self.zone_x.pk])
        self.assertIn(self.any_address.pk, result["inherited_address_ids"])
        self.assertEqual(
            {(row["policy_id"], row["direction"]) for row in result["policy_paths"]},
            {(self.policies[1].pk, "source"), (self.policies[2].pk, "destination")},
        )

    def test_unknown_membership_keeps_addresses_but_not_policy_claims(self):
        self.membership.delete()
        result = self.context()
        self.assertFalse(result["zone_context_known"])
        self.assertEqual(result["policy_paths"], [])
        self.assertIn(self.any_address.pk, result["inherited_address_ids"])
        warning = render_to_string(
            "netbox_security/inc/zone_context_warning.html", {"policy_context": result}
        )
        self.assertIn("policy applicability is unconfirmed", warning)

    def test_explicit_caller_context_and_explicit_unknown(self):
        result = self.context(member_zone_ids=[self.trust.pk])
        self.assertIn(
            self.policies[0].pk, {row["policy_id"] for row in result["policy_paths"]}
        )
        self.assertEqual(self.context(member_zone_ids=None)["policy_paths"], [])

    def test_device_zone_is_not_assumed_for_every_interface(self):
        self.membership.delete()
        SecurityZoneAssignment.objects.create(
            zone=self.trust, assigned_object=self.interface.device
        )
        self.assertFalse(self.context()["zone_context_known"])

    def test_multiple_explicit_interface_zones_are_preserved(self):
        SecurityZoneAssignment.objects.create(
            zone=self.trust, assigned_object=self.interface
        )
        result = self.context()
        self.assertEqual(
            set(result["member_zone_ids"]), {self.zone_x.pk, self.trust.pk}
        )
        self.assertIn(
            self.policies[0].pk, {row["policy_id"] for row in result["policy_paths"]}
        )

    def test_inaccessible_membership_does_not_reveal_policy_applicability(self):
        user = get_user_model().objects.create_user(username="zone-context-reader")
        permission = ObjectPermission.objects.create(
            name="view-context-except-membership", actions=["view"]
        )
        permission.users.add(user)
        permission.object_types.add(
            *[
                ContentType.objects.get_for_model(model)
                for model in (
                    IPAddress,
                    Prefix,
                    CustomPrefix,
                    Address,
                    AddressList,
                    Interface,
                    SecurityZone,
                    SecurityZonePolicy,
                )
            ]
        )
        result = get_address_set_hierarchy(
            user=user, app_label="ipam", model="ipaddress", object_id=self.ip.pk
        )
        self.assertFalse(result["zone_context_known"])
        self.assertEqual(result["policy_paths"], [])

    def candidate_context(self):
        from netbox_security.utils.policy_candidates import add_policy_candidates

        return add_policy_candidates(
            self.context(include_candidates=True), self.ip, user=self.user
        )

    def test_candidate_table_separates_wildcard_zone_mismatch(self):
        result = self.candidate_context()
        candidates = {
            (row["policy_id"], row["direction"]) for row in result["policy_candidates"]
        }
        self.assertEqual(
            candidates,
            {
                (self.policies[1].pk, "source"),
                (self.policies[2].pk, "destination"),
            },
        )
        wildcard = next(
            row
            for row in result["excluded_policy_candidates"]
            if row["policy_id"] == self.policies[0].pk
        )
        self.assertEqual(wildcard["match_status"], "zone_mismatch")
        self.assertEqual(wildcard["address_book"], "Global")
        html = render_to_string(
            "netbox_security/inc/policy_candidates_table.html", {"rows": [wildcard]}
        )
        self.assertIn("Zone mismatch", html)
        self.assertIn(self.policies[0].name, html)
        self.assertIn("trust", html)

    def test_unknown_zone_shows_unconfirmed_candidates(self):
        self.membership.delete()
        result = self.candidate_context()
        self.assertTrue(result["policy_candidates"])
        self.assertTrue(
            all(
                row["match_status"] == "unconfirmed"
                for row in result["policy_candidates"]
            )
        )
        html = render_to_string(
            "netbox_security/inc/policy_candidates_table.html",
            {"rows": result["policy_candidates"]},
        )
        self.assertIn("Address match only", html)
        self.assertNotIn("Address and zone match", html)

    def test_zone_book_scope_does_not_establish_membership(self):
        from netbox_security.models import AddressAssignment

        AddressAssignment.objects.create(
            address=self.lists[1].assigned_object, assigned_object=self.trust
        )
        result = self.candidate_context()
        row = next(
            row
            for row in result["excluded_policy_candidates"]
            if row["policy_id"] == self.policies[1].pk
        )
        self.assertEqual(row["match_status"], "scope_mismatch")
        self.assertEqual(result["member_zone_ids"], [self.zone_x.pk])

    def test_correct_zone_book_and_visible_criteria(self):
        from netbox_security.models import AddressAssignment

        AddressAssignment.objects.create(
            address=self.lists[1].assigned_object, assigned_object=self.zone_x
        )
        result = self.candidate_context()
        row = next(
            row
            for row in result["policy_candidates"]
            if row["policy_id"] == self.policies[1].pk
        )
        self.assertEqual(row["match_status"], "zone_confirmed")
        self.assertEqual(row["address_book"], "Zone-specific")
        self.assertEqual(row["criteria"]["source_address"], [self.lists[1]])
        self.assertEqual(row["criteria"]["destination_address"], [self.lists[2]])
        self.assertTrue(row["matched_path"])

    def test_nested_set_cannot_make_zone_entry_global(self):
        from netbox_security.models import AddressAssignment, AddressSet
        from netbox_security.utils.policy_candidates import add_policy_candidates

        address_set = AddressSet.objects.create(name="nested-book")
        address_set.addresses.add(self.lists[1].assigned_object)
        wrapper = AddressList.objects.create(
            name="nested-wrapper", assigned_object=address_set
        )
        self.policies[1].source_address.set([wrapper])
        AddressAssignment.objects.create(
            address=self.lists[1].assigned_object, assigned_object=self.trust
        )
        result = add_policy_candidates(
            self.context(include_candidates=True), self.ip, user=self.user
        )
        row = next(
            row
            for row in result["excluded_policy_candidates"]
            if row["policy_id"] == self.policies[1].pk
        )
        self.assertEqual(row["match_status"], "scope_mismatch")
