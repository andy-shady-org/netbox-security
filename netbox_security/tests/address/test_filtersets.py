from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from netaddr import IPNetwork
from dcim.models import Site, Manufacturer
from dcim.models import Device, VirtualDeviceContext, DeviceRole, DeviceType
from ipam.models import IPRange
from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import Address, AddressList, AddressSet, AddressAssignment
from netbox_security.filtersets import (
    AddressFilterSet,
    AddressListFilterSet,
    AddressAssignmentFilterSet,
)


class AddressFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Address.objects.all()
    filterset = AddressFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.tenant_groups = (
            TenantGroup(name="Tenant group 1", slug="tenant-group-1"),
            TenantGroup(name="Tenant group 2", slug="tenant-group-2"),
            TenantGroup(name="Tenant group 3", slug="tenant-group-3"),
        )
        for tenantgroup in cls.tenant_groups:
            tenantgroup.save()

        cls.tenants = (
            Tenant(name="Tenant 1", slug="tenant-1", group=cls.tenant_groups[0]),
            Tenant(name="Tenant 2", slug="tenant-2", group=cls.tenant_groups[1]),
            Tenant(name="Tenant 3", slug="tenant-3", group=cls.tenant_groups[2]),
        )
        Tenant.objects.bulk_create(cls.tenants)

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

        cls.addresses = (
            Address(name="address-1", address="1.1.1.4/32", tenant=cls.tenants[0]),
            Address(name="address-2", address="1.1.1.5/32", tenant=cls.tenants[1]),
            Address(name="address-3", address="1.1.1.6/32", tenant=cls.tenants[2]),
            Address(name="address-4", ip_range=cls.ranges[0], tenant=cls.tenants[2]),
            Address(name="address-5", ip_range=cls.ranges[1], tenant=cls.tenants[2]),
            Address(
                name="address-6", dns_name="test.example.com", tenant=cls.tenants[2]
            ),
        )
        for address in cls.addresses:
            address.save()

        cls.address_sets = (
            AddressSet(name="address-set-1", tenant=cls.tenants[0]),
            AddressSet(name="address-set-2", tenant=cls.tenants[1]),
            AddressSet(name="address-set-3", tenant=cls.tenants[2]),
        )
        AddressSet.objects.bulk_create(cls.address_sets)
        cls.address_sets[0].addresses.set(cls.addresses)
        cls.address_sets[1].addresses.set(cls.addresses)
        cls.address_sets[2].addresses.set(cls.addresses)

        cls.assignments = (
            AddressList(
                name="address-list-1",
                assigned_object=cls.addresses[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "netbox_security", "address"
                ),
                assigned_object_id=cls.addresses[0].pk,
            ),
        )
        for assignment in cls.assignments:
            assignment.save()

    def test_name(self):
        params = {"name": ["address-1", "address-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_dns_name(self):
        params = {"dns_name": ["test.example.com"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ip_range(self):
        params = {"ip_range_id": [self.ranges[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ip_range": [self.ranges[0].start_address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_tenant(self):
        params = {"tenant_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"tenant": [self.tenants[0].slug, self.tenants[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant_group(self):
        params = {
            "tenant_group_id": [self.tenant_groups[0].pk, self.tenant_groups[1].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "tenant_group": [self.tenant_groups[0].slug, self.tenant_groups[1].slug]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_addresses(self):
        params = {
            "address_set_id": [
                self.address_sets[0].pk,
                self.address_sets[1].pk,
                self.address_sets[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 6)
        params = {"address": self.addresses[0].address}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_assignment(self):
        self.filterset = AddressListFilterSet
        self.queryset = AddressList.objects.all()
        params = {"name": [self.assignments[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [self.addresses[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class AddressAssignmentFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = AddressAssignment.objects.all()
    filterset = AddressAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
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

        cls.addresses = (
            Address(
                name="address-1",
                address="1.1.1.4/32",
            ),
            Address(
                name="address-2",
                address="1.1.1.5/32",
            ),
            Address(name="address-3", address="1.1.1.6/32"),
            Address(name="address-4", ip_range=cls.ranges[0]),
            Address(name="address-5", ip_range=cls.ranges[1]),
            Address(name="address-6", dns_name="test.example.com"),
        )
        Address.objects.bulk_create(cls.addresses)

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
            AddressAssignment(
                address=cls.addresses[0],
                assigned_object=cls.devices[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[0].pk,),
            ),
            AddressAssignment(
                address=cls.addresses[1],
                assigned_object=cls.devices[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[1].pk,),
            ),
            AddressAssignment(
                address=cls.addresses[2],
                assigned_object=cls.virtual[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "virtualdevicecontext"
                ),
                assigned_object_id=(cls.virtual[0].pk,),
            ),
        )
        AddressAssignment.objects.bulk_create(cls.assignments)

    def test_address(self):
        params = {"address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "address_id": [
                self.addresses[1].pk,
                self.addresses[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"address": [self.addresses[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "address": [
                self.addresses[1].name,
                self.addresses[2].name,
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
