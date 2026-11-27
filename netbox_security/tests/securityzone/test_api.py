from netaddr import IPNetwork
from rest_framework import status
from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from django.contrib.contenttypes.models import ContentType
from netbox_security.models import (
    SecurityZone,
    SecurityZonePolicy,
    Address,
    AddressList,
    Application,
    ApplicationSet,
    CustomPrefix,
)
from netbox_security.choices import (
    ProtocolChoices,
    ActionChoices,
)

from netbox_security.tests.mixins.api import SecurityZoneMixin, SecurityZonePolicyMixin


class SecurityZoneAPITestCase(
    SecurityZoneMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):

    brief_fields = [
        "allow_intra_zone",
        "description",
        "destination_policy_count",
        "display",
        "id",
        "identifier",
        "name",
        "source_policy_count",
        "url",
    ]

    create_data = [
        {"name": "DMZ"},
        {"name": "PUBLIC"},
        {"name": "INTERNAL"},
    ]

    bulk_update_data = {
        "description": "Test Security Zone",
    }
    bulk_update_invalid_data = {
        "allow_intra_zone": "Test Security Zone",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_list_objects_has_stable_default_ordering(self):
        self.add_permissions("netbox_security.view_securityzone")
        SecurityZone.objects.create(name="A-FIRST", identifier="second")
        SecurityZone.objects.create(name="A-FIRST", identifier="first")
        expected_ids = list(
            SecurityZone.objects.order_by("name", "pk").values_list("pk", flat=True)[:2]
        )

        response = self.client.get(self._get_list_url(), {"limit": 2}, **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [zone["id"] for zone in response.json()["results"]], expected_ids
        )

    def test_update_disallow_intra_zone_rejected_with_same_zone_policies(self):
        self.add_permissions(
            "netbox_security.view_securityzone",
            "netbox_security.change_securityzone",
        )

        zone = SecurityZone.objects.create(name="INTRA-ZONE", allow_intra_zone=True)
        SecurityZonePolicy.objects.create(
            name="intra-zone-policy",
            index=999,
            source_zone=zone,
            destination_zone=zone,
            policy_actions=[ActionChoices.PERMIT],
        )

        response = self.client.patch(
            self._get_detail_url(zone),
            {"allow_intra_zone": False},
            format="json",
            **self.header,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("allow_intra_zone", response_data)


class SecurityZonePolicyAPITestCase(
    SecurityZonePolicyMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    user_permissions = (
        "ipam.view_iprange",
        "ipam.view_ipaddress",
        "ipam.view_prefix",
        "tenancy.view_tenant",
        "tenancy.view_tenantgroup",
        "netbox_security.view_securityzone",
        "netbox_security.view_address",
        "netbox_security.view_addresslist",
        "netbox_security.view_applicationitem",
        "netbox_security.view_application",
        "netbox_security.view_applicationset",
        "netbox_security.view_customprefix",
    )

    # TODO: Remove this override once NetBox fixes enum-backed ArrayLookup
    # auto-filter rendering in utilities.testing.api (_emit_array_lookup_filter_tests).
    graphql_auto_filter_exclude = ("policy_actions",)

    brief_fields = [
        "application_sets",
        "applications",
        "description",
        "destination_address",
        "destination_zone",
        "display",
        "id",
        "identifier",
        "index",
        "name",
        "policy_actions",
        "source_address",
        "source_zone",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Security Zone Policy",
    }
    bulk_update_invalid_data = {
        "policy_actions": "Test Security Zone Policy",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policies[0].applications.add(cls.applications[0])
        cls.policies[1].applications.add(
            cls.applications[1],
            cls.applications[2],
        )
        cls.policies[0].application_sets.add(cls.application_sets[0])
        cls.policies[1].application_sets.add(
            cls.application_sets[1],
            cls.application_sets[2],
        )
        cls.policies[2].source_address.add(cls.address_lists[0])
        cls.policies[2].destination_address.add(cls.address_lists[1])
        cls.policies[2].destination_address.set(cls.destination_addresses)
        cls.policies[2].applications.set(cls.applications)
        cls.policies[2].application_sets.set(cls.application_sets)

        cls.create_data = [
            {
                "name": "policy-x",
                "index": 1,
                "policy_actions": [
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
                "source_zone": cls.zones[0].pk,
                "destination_zone": cls.zones[1].pk,
            },
            {
                "name": "policy-y",
                "index": 2,
                "policy_actions": [
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
                "source_zone": cls.zones[0].pk,
                "destination_zone": cls.zones[1].pk,
            },
            {
                "name": "policy-z",
                "index": 3,
                "policy_actions": [
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
                "source_zone": cls.zones[0].pk,
                "destination_zone": cls.zones[1].pk,
            },
        ]

    def test_policy(self):
        self.assertEqual(
            set(self.policies[2].destination_address.all()),
            set(self.destination_addresses),
        )
        self.assertEqual(
            set(self.policies[2].applications.all()), set(self.applications)
        )
        self.assertEqual(
            set(self.policies[2].application_sets.all()), set(self.application_sets)
        )

    def test_create_same_zone_rejected_when_intra_zone_not_allowed(self):
        self.add_permissions(
            "netbox_security.view_securityzonepolicy",
            "netbox_security.add_securityzonepolicy",
        )

        payload = {
            "name": "policy-same-zone-denied",
            "index": 100,
            "policy_actions": [ActionChoices.PERMIT],
            "source_zone": self.zones[0].pk,
            "destination_zone": self.zones[0].pk,
        }

        response = self.client.post(
            self._get_list_url(), payload, format="json", **self.header
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("source_zone", response_data)
        self.assertIn("destination_zone", response_data)

    def test_create_empty_policy_actions_rejected(self):
        self.add_permissions(
            "netbox_security.view_securityzonepolicy",
            "netbox_security.add_securityzonepolicy",
        )

        payload = {
            "name": "policy-empty-actions",
            "index": 102,
            "policy_actions": [],
            "source_zone": self.zones[0].pk,
            "destination_zone": self.zones[1].pk,
        }

        response = self.client.post(
            self._get_list_url(), payload, format="json", **self.header
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("policy_actions", response_data)

    def test_create_same_zone_allowed_when_intra_zone_enabled(self):
        self.add_permissions(
            "netbox_security.view_securityzonepolicy",
            "netbox_security.add_securityzonepolicy",
        )

        zone = SecurityZone.objects.create(
            name="ZONE-INTRA-ALLOWED", allow_intra_zone=True
        )
        payload = {
            "name": "policy-same-zone-allowed",
            "index": 101,
            "policy_actions": [ActionChoices.PERMIT],
            "source_zone": zone.pk,
            "destination_zone": zone.pk,
        }

        response = self.client.post(
            self._get_list_url(), payload, format="json", **self.header
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
