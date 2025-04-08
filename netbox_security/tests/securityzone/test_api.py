from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from django.contrib.contenttypes.models import ContentType
from netbox_security.models import (
    SecurityZone,
    SecurityZonePolicy,
    Address,
    AddressList,
)


class SecurityZoneAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = SecurityZone

    brief_fields = ["description", "display", "id", "name", "url"]

    create_data = [
        {"name": "DMZ"},
        {"name": "PUBLIC"},
        {"name": "INTERNAL"},
    ]

    bulk_update_data = {
        "description": "Test Security Zone",
    }

    @classmethod
    def setUpTestData(cls):
        zones = (
            SecurityZone(name="AMBER"),
            SecurityZone(name="RED"),
            SecurityZone(name="GREEN"),
        )
        SecurityZone.objects.bulk_create(zones)


class SecurityZonePolicyAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = SecurityZonePolicy

    brief_fields = [
        "actions",
        "application",
        "description",
        "destination_address",
        "destination_zone",
        "display",
        "id",
        "index",
        "name",
        "source_address",
        "source_zone",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Security Zone Policy",
    }

    @classmethod
    def setUpTestData(cls):
        cls.zones = (
            SecurityZone(name="ZONE-3"),
            SecurityZone(name="ZONE-4"),
        )
        SecurityZone.objects.bulk_create(cls.zones)

        cls.policies = (
            SecurityZonePolicy(
                name="policy-5",
                index=5,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                actions=["permit", "count", "log"],
                application=["test-1", "test-2"],
            ),
            SecurityZonePolicy(
                name="policy-6",
                index=6,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                actions=["permit", "count", "log"],
                application=["test-1", "test-2"],
            ),
        )
        SecurityZonePolicy.objects.bulk_create(cls.policies)

        cls.addresses = (
            Address(name="address-1", value="1.1.1.1/32"),
            Address(name="address-2", value="1.1.1.2/32"),
            Address(name="address-3", value="1.1.1.3/32"),
        )
        Address.objects.bulk_create(cls.addresses)

        cls.addresses_lists = (
            AddressList(
                name="address-list-1",
                assigned_object_id=cls.addresses[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="address"
                ),
            ),
            AddressList(
                name="address-list-2",
                assigned_object_id=cls.addresses[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="address"
                ),
            ),
            AddressList(
                name="address-list-3",
                assigned_object_id=cls.addresses[2].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="address"
                ),
            ),
        )
        cls.destination_addresses = (cls.addresses_lists[1], cls.addresses_lists[2])
        AddressList.objects.bulk_create(cls.addresses_lists)

        cls.policy = SecurityZonePolicy.objects.create(
            name="policy-8",
            index=8,
            source_zone=cls.zones[0],
            destination_zone=cls.zones[1],
            actions=["permit", "count", "log"],
            application=["test-1", "test-2"],
        )
        cls.policy.source_address.add(cls.addresses_lists[0])
        cls.policy.destination_address.add(cls.addresses_lists[1])
        cls.policy.destination_address.set(cls.destination_addresses)

        cls.create_data = [
            {
                "name": "policy-1",
                "index": 1,
                "actions": ["permit", "count", "log"],
                "application": ["test-1", "test-2"],
                "source_zone": cls.zones[0].pk,
                "destination_zone": cls.zones[1].pk,
            },
            {
                "name": "policy-2",
                "index": 2,
                "actions": ["permit", "count", "log"],
                "application": ["test-1", "test-2"],
                "source_zone": cls.zones[0].pk,
                "destination_zone": cls.zones[1].pk,
            },
            {
                "name": "policy-3",
                "index": 3,
                "actions": ["permit", "count", "log"],
                "application": ["test-1", "test-2"],
                "source_zone": cls.zones[0].pk,
                "destination_zone": cls.zones[1].pk,
            },
        ]

    def test_policy(self):
        self.assertEqual(
            set(self.policy.destination_address.all()), set(self.destination_addresses)
        )
