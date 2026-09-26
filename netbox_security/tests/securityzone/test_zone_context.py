from django.contrib.contenttypes.models import ContentType
from netaddr import IPNetwork

from ipam.models import IPAddress, IPRange, Prefix
from netbox_security.models import (
    Address,
    AddressList,
    SecurityZone,
    SecurityZoneAssignment,
    SecurityZonePolicy,
)
from netbox_security.tests.custom import APITestCase
from netbox_security.utils import get_address_set_hierarchy
from netbox_security.utils.policy_candidates import add_policy_candidates
from netbox_security.utils.zone_membership import resolve_zone_membership


class ZoneContextRegressionTestCase(APITestCase):
    model = SecurityZone
    user_permissions = (
        "ipam.view_ipaddress",
        "ipam.view_iprange",
        "ipam.view_prefix",
        "netbox_security.view_address",
        "netbox_security.view_addresslist",
        "netbox_security.view_securityzone",
        "netbox_security.view_securityzoneassignment",
        "netbox_security.view_securityzonepolicy",
    )

    @classmethod
    def setUpTestData(cls):
        cls.external_zone = SecurityZone.objects.create(name="RFC1918-EXTERNAL")
        cls.shady_zone = SecurityZone.objects.create(name="RFC1918-SHADY")

        cls.destination_prefix = Prefix.objects.create(
            prefix=IPNetwork("10.16.38.160/28")
        )
        cls.destination_ip = IPAddress.objects.create(
            address=IPNetwork("10.16.38.162/32")
        )
        cls.destination_range = IPRange.objects.create(
            start_address=IPNetwork("10.16.48.161/28"),
            end_address=IPNetwork("10.16.48.174/28"),
        )
        cls.range_member_ip = IPAddress.objects.create(
            address=IPNetwork("10.16.48.170/32")
        )

        prefix_type = ContentType.objects.get_for_model(Prefix)
        iprange_type = ContentType.objects.get_for_model(IPRange)
        address_type = ContentType.objects.get_for_model(Address)

        SecurityZoneAssignment.objects.create(
            assigned_object_type=prefix_type,
            assigned_object_id=cls.destination_prefix.pk,
            zone=cls.shady_zone,
        )
        SecurityZoneAssignment.objects.create(
            assigned_object_type=iprange_type,
            assigned_object_id=cls.destination_range.pk,
            zone=cls.shady_zone,
        )

        cls.destination_address = Address.objects.create(
            name="rfc1918-destination-subnet",
            assigned_object_type=prefix_type,
            assigned_object_id=cls.destination_prefix.pk,
        )
        cls.destination_address_list = AddressList.objects.create(
            name="rfc1918-destination-address-list",
            assigned_object_type=address_type,
            assigned_object_id=cls.destination_address.pk,
        )
        cls.policy = SecurityZonePolicy.objects.create(
            name="allow-rfc1918-shady",
            index=10,
            source_zone=cls.external_zone,
            destination_zone=cls.shady_zone,
            policy_actions=["permit"],
        )
        cls.policy.destination_address.set([cls.destination_address_list])

    def test_resolve_zone_membership_includes_containing_prefix_zone(self):
        self.assertEqual(
            resolve_zone_membership(self.destination_ip, user=self.user),
            [self.shady_zone.pk],
        )

    def test_resolve_zone_membership_includes_containing_iprange_zone(self):
        self.assertEqual(
            resolve_zone_membership(self.range_member_ip, user=self.user),
            [self.shady_zone.pk],
        )

    def test_get_address_set_hierarchy_uses_direct_prefix_zone_assignment(self):
        context = get_address_set_hierarchy(
            user=self.user,
            app_label="ipam",
            model="prefix",
            object_id=self.destination_prefix.pk,
        )

        self.assertTrue(context["zone_context_known"])
        self.assertEqual(context["member_zone_ids"], [self.shady_zone.pk])

    def test_get_address_set_hierarchy_uses_direct_iprange_zone_assignment(self):
        context = get_address_set_hierarchy(
            user=self.user,
            app_label="ipam",
            model="iprange",
            object_id=self.destination_range.pk,
        )

        self.assertTrue(context["zone_context_known"])
        self.assertEqual(context["member_zone_ids"], [self.shady_zone.pk])

    def test_policy_candidate_moves_from_unconfirmed_to_zone_confirmed(self):
        unknown = add_policy_candidates(
            get_address_set_hierarchy(
                user=self.user,
                app_label="ipam",
                model="ipaddress",
                object_id=self.destination_ip.pk,
                member_zone_ids=None,
                include_candidates=True,
            ),
            self.destination_ip,
            user=self.user,
        )

        self.assertFalse(unknown["zone_context_known"])
        self.assertEqual(len(unknown["policy_candidates"]), 1)
        self.assertEqual(unknown["policy_candidates"][0]["policy_id"], self.policy.pk)
        self.assertEqual(unknown["policy_candidates"][0]["match_status"], "unconfirmed")

        confirmed = add_policy_candidates(
            get_address_set_hierarchy(
                user=self.user,
                app_label="ipam",
                model="ipaddress",
                object_id=self.destination_ip.pk,
                include_candidates=True,
            ),
            self.destination_ip,
            user=self.user,
        )

        self.assertTrue(confirmed["zone_context_known"])
        self.assertEqual(confirmed["member_zone_ids"], [self.shady_zone.pk])
        self.assertEqual(len(confirmed["policy_candidates"]), 1)
        self.assertEqual(confirmed["policy_candidates"][0]["policy_id"], self.policy.pk)
        self.assertEqual(
            confirmed["policy_candidates"][0]["match_status"],
            "zone_confirmed",
        )
