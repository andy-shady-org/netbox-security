from django.test import TestCase
from utilities.testing import ChangeLoggedFilterSetTests

from ipam.choices import IPAddressStatusChoices
from ipam.models import IPAddress, Prefix, IPRange

from netbox_security.models import NatPool, NatPoolMember
from netbox_security.filtersets import NatPoolFilterSet, NatPoolMemberFilterSet
from netbox_security.choices import (
    PoolTypeChoices,
)


class NatPoolFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatPool.objects.all()
    filterset = NatPoolFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.pools = (
            NatPool(name="pool-4"),
            NatPool(name="pool-5"),
            NatPool(name="pool-6"),
        )
        for item in cls.pools:
            item.save()

    def test_name(self):
        params = {"name": ["pool-4", "pool-5"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filters(self):
        params = {"natpool_id": [self.pools[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natpool_id": [self.pools[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natpool_id": [self.pools[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)


class NatPoolMemberFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatPoolMember.objects.all()
    filterset = NatPoolMemberFilterSet

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
                size=4,
            ),
            IPRange(
                start_address="1.1.2.2/24",
                end_address="1.1.2.5/24",
                status="active",
                size=4,
            ),
            IPRange(
                start_address="1.1.3.2/24",
                end_address="1.1.3.5/24",
                status="active",
                size=4,
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

    def test_name(self):
        params = {"name": ["member-1", "member-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filters(self):
        params = {"natpoolmember_id": [self.members[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natpoolmember_id": [self.members[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natpoolmember_id": [self.members[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
