from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import NatPool, NatPoolMember
from ipam.models import IPAddress, Prefix, IPRange
from ipam.choices import IPAddressStatusChoices
from netbox_security.choices import (
    PoolTypeChoices,
)


class NatPoolAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = NatPool

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
            "name": "pool-1",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
        {
            "name": "pool-2",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
        {
            "name": "pool-3",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
    ]

    bulk_update_data = {
        "description": "Test Nat Pool",
    }

    @classmethod
    def setUpTestData(cls):
        filters = (
            NatPool(
                name="pool-4",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-5",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-6",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatPool.objects.bulk_create(filters)


class NatPoolMemberAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = NatPoolMember

    brief_fields = [
        "display",
        "id",
        "name",
        "pool",
        "status",
        "url",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.pools = (
            NatPool(
                name="pool-1",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-2",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-3",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatPool.objects.bulk_create(cls.pools)

        cls.prefixes = (
            Prefix(
                prefix="1.1.1.0/24",
                status="active",
            ),
            Prefix(
                prefix="1.1.2.0/24",
                status="active",
            ),
            Prefix(
                prefix="1.1.3.0/24",
                status="active",
            ),
        )
        Prefix.objects.bulk_create(cls.prefixes)

        cls.addresses = (
            IPAddress(
                address="1.1.1.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.2.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.3.1/24",
                status="active",
            ),
        )
        IPAddress.objects.bulk_create(cls.addresses)

        cls.ranges = (
            IPRange(
                start_address="1.1.1.2/24",
                end_address="1.1.1.5/24",
                status="active",
                size=4
            ),
            IPRange(
                start_address="1.1.2.2/24",
                end_address="1.1.2.5/24",
                status="active",
                size=4
            ),
            IPRange(
                start_address="1.1.3.2/24",
                end_address="1.1.3.5/24",
                status="active",
                size=4
            ),
        )
        IPRange.objects.bulk_create(cls.ranges)

        cls.members = (
            NatPoolMember(
                name="member-1",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                prefix=cls.prefixes[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            NatPoolMember(
                name="member-2",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                address=cls.addresses[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            NatPoolMember(
                name="member-3",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                address_range=cls.ranges[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
        )
        NatPoolMember.objects.bulk_create(cls.members)

        cls.create_data = [
            {
                "name": "member-4",
                "pool": cls.pools[0].pk,
                "status": IPAddressStatusChoices.STATUS_ACTIVE,
                "prefix": cls.prefixes[0].pk,
                "source_ports": [1, 2, 3],
                "destination_ports": [4, 5, 6],
            },
            {
                "name": "member-5",
                "pool": cls.pools[1].pk,
                "status": IPAddressStatusChoices.STATUS_ACTIVE,
                "address": cls.addresses[0].pk,
                "source_ports": [1, 2, 3],
                "destination_ports": [4, 5, 6],
            },
            {
                "name": "member-6",
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
