from django.contrib.contenttypes.models import ContentType
from netaddr import IPNetwork
from django.test import TestCase
from utilities.testing import ChangeLoggedFilterSetTests
from dcim.models import Site, Manufacturer
from dcim.models import Device, VirtualDeviceContext, DeviceRole, DeviceType
from ipam.models import IPAddress, Prefix, IPRange
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import NatPool, NatPoolMember, NatPoolAssignment
from netbox_security.filtersets import (
    NatPoolFilterSet,
    NatPoolMemberFilterSet,
    NatPoolAssignmentFilterSet,
)
from netbox_security.choices import (
    PoolTypeChoices,
)


class NatPoolFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatPool.objects.all()
    filterset = NatPoolFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.pools = (
            NatPool(
                name="pool-4",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-5",
                pool_type=PoolTypeChoices.HOST_ADDRESS_BASE,
                status=IPAddressStatusChoices.STATUS_RESERVED,
            ),
            NatPool(
                name="pool-6",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
        )
        for item in cls.pools:
            item.save()

    def test_name(self):
        params = {"name": ["pool-4", "pool-5"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filters(self):
        params = {"pool_type": [PoolTypeChoices.ADDRESS]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"pool_type": [PoolTypeChoices.HOST_ADDRESS_BASE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"status": [IPAddressStatusChoices.STATUS_ACTIVE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"status": [IPAddressStatusChoices.STATUS_RESERVED]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


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
                start_address=IPNetwork("1.1.1.2/24"),
                end_address=IPNetwork("1.1.1.5/24"),
                status="active",
                size=4,
            ),
            IPRange(
                start_address=IPNetwork("1.1.2.2/24"),
                end_address=IPNetwork("1.1.2.5/24"),
                status="active",
                size=4,
            ),
            IPRange(
                start_address=IPNetwork("1.1.3.2/24"),
                end_address=IPNetwork("1.1.3.5/24"),
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
                source_ports=[1, 2, 3, 4],
                destination_ports=[4, 5, 6],
            ),
            NatPoolMember(
                name="member-2",
                pool=cls.pools[1],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                address=cls.addresses[0],
                source_ports=[4, 5, 6],
                destination_ports=[1, 2, 3],
            ),
            NatPoolMember(
                name="member-3",
                pool=cls.pools[1],
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

    def test_pool(self):
        params = {"pool_id": [self.pools[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"pool": [self.pools[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"pool_id": [self.pools[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"pool": [self.pools[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_prefix(self):
        params = {"prefix_id": [self.prefixes[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"prefix": [self.prefixes[0].prefix]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_address(self):
        params = {"address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [self.addresses[0].address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_address_range(self):
        params = {"address_range_id": [self.ranges[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address_range": [self.ranges[0].start_address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_status(self):
        params = {"status": [IPAddressStatusChoices.STATUS_ACTIVE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_source_ports(self):
        params = {"source_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_destination_ports(self):
        params = {"destination_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class NatPoolAssignmentFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatPoolAssignment.objects.all()
    filterset = NatPoolAssignmentFilterSet

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

        cls.sites = (Site(name="site-1", slug="site-1"),)
        Site.objects.bulk_create(cls.sites)

        cls.manu = (Manufacturer(name="manufacturer-1", slug="manufacturer-1"),)
        Manufacturer.objects.bulk_create(cls.manu)

        cls.types = (
            DeviceType(model="type-1", slug="type-1", manufacturer=cls.manu[0]),
        )
        DeviceType.objects.bulk_create(cls.types)

        cls.roles = (
            DeviceRole(name="role-1", slug="role-1", level=0, lft=1, rght=2, tree_id=1),
        )
        DeviceRole.objects.bulk_create(cls.roles)
        cls.devices = (
            Device(
                name="device-1",
                status="active",
                site=cls.sites[0],
                role=cls.roles[0],
                device_type=cls.types[0],
            ),
            Device(
                name="device-2",
                status="active",
                site=cls.sites[0],
                role=cls.roles[0],
                device_type=cls.types[0],
            ),
        )
        Device.objects.bulk_create(cls.devices)
        cls.virtual = (
            VirtualDeviceContext(name="vd-1", device=cls.devices[0], status="active"),
        )
        VirtualDeviceContext.objects.bulk_create(cls.virtual)
        cls.assignments = (
            NatPoolAssignment(
                pool=cls.pools[0],
                assigned_object=cls.devices[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[0].pk,),
            ),
            NatPoolAssignment(
                pool=cls.pools[1],
                assigned_object=cls.devices[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[1].pk,),
            ),
            NatPoolAssignment(
                pool=cls.pools[2],
                assigned_object=cls.virtual[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "virtualdevicecontext"
                ),
                assigned_object_id=(cls.virtual[0].pk,),
            ),
        )
        NatPoolAssignment.objects.bulk_create(cls.assignments)

    def test_pool(self):
        params = {"pool_id": [self.pools[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "pool_id": [
                self.pools[1].pk,
                self.pools[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"pool": [self.pools[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "pool": [
                self.pools[1].name,
                self.pools[2].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_device(self):
        params = {"device_id": [self.devices[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"device_id": [self.devices[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"device_id": [self.devices[0].pk, self.devices[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"device": [self.devices[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"device": [self.devices[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"device": [self.devices[0].name, self.devices[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_virtual(self):
        params = {"virtualdevicecontext_id": [self.virtual[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"virtualdevicecontext": [self.virtual[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
