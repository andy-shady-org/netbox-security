from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from ipam.choices import IPAddressStatusChoices
from netbox_security.choices import (
    PoolTypeChoices,
)
from netbox_security.tests.mixins import NatPoolMixin, NatPoolMemberMixin


class NatPoolAPITestCase(
    NatPoolMixin,
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
        "description",
        "display",
        "id",
        "member_count",
        "name",
        "pool_type",
        "status",
        "url",
    ]

    create_data = [
        {
            "name": "pool-x",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
        {
            "name": "pool-y",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
        {
            "name": "pool-z",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
    ]

    bulk_update_data = {
        "description": "Test Nat Pool",
    }
    bulk_update_invalid_data = {
        "status": "Test Status",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()


class NatPoolMemberAPITestCase(
    NatPoolMemberMixin,
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
        "ipam.view_prefix",
        "ipam.view_ipaddress",
        "netbox_security.view_natpool",
    )

    brief_fields = [
        "display",
        "id",
        "name",
        "pool",
        "status",
        "url",
    ]

    bulk_update_invalid_data = {
        "status": "invalid status",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.create_data = [
            {
                "name": "member-x",
                "pool": cls.pools[0].pk,
                "status": IPAddressStatusChoices.STATUS_ACTIVE,
                "prefix": cls.prefixes[0].pk,
                "source_ports": [1, 2, 3],
                "destination_ports": [4, 5, 6],
            },
            {
                "name": "member-y",
                "pool": cls.pools[1].pk,
                "status": IPAddressStatusChoices.STATUS_ACTIVE,
                "address": cls.ip_addresses[0].pk,
                "source_ports": [1, 2, 3],
                "destination_ports": [4, 5, 6],
            },
            {
                "name": "member-z",
                "pool": cls.pools[2].pk,
                "status": IPAddressStatusChoices.STATUS_ACTIVE,
                "address_range": cls.ranges[0].pk,
                "source_ports": [1, 2, 3],
                "destination_ports": [4, 5, 6],
            },
        ]

        cls.bulk_update_data = {
            "pool": cls.pools[1].pk,
        }
