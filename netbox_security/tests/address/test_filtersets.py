from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from dcim.models import Site, Manufacturer
from dcim.models import Device, VirtualDeviceContext, DeviceRole, DeviceType
from utilities.testing import ChangeLoggedFilterSetTestMixin

from netbox_security.models import (
    Address,
    AddressList,
    AddressAssignment,
)

from netbox_security.filtersets import (
    AddressFilterSet,
    AddressListFilterSet,
    AddressAssignmentFilterSet,
)
from netbox_security.tests.mixins import AddressListMixin


class AddressFiterSetTestCase(AddressListMixin, TestCase, ChangeLoggedFilterSetTestMixin):
    queryset = Address.objects.all()
    filterset = AddressFilterSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.address_sets[0].addresses.set(cls.addresses)
        cls.address_sets[1].addresses.set(cls.addresses)
        cls.address_sets[2].addresses.set(cls.addresses)

    def test_name(self):
        params = {"name": ["address-1", "address-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_dns_name(self):
        params = {"dns_name": ["test.example.com"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_custom_prefix(self):
        params = {"custom_prefix_id": [self.custom_prefixes[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"custom_prefix": [self.custom_prefixes[0].prefix]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ip_range(self):
        params = {"ip_range_id": [self.ranges[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ip_range": [self.ranges[0].start_address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_prefix(self):
        params = {"prefix_id": [self.prefixes[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"prefix": [self.prefixes[0].prefix]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ip_address(self):
        params = {"ip_address_id": [self.ip_addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"ip_address": [self.ip_addresses[0].address]}
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

    def test_address_sets(self):
        params = {
            "address_set_id": [
                self.address_sets[0].pk,
                self.address_sets[1].pk,
                self.address_sets[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)

    def test_assignment(self):
        self.filterset = AddressListFilterSet
        self.queryset = AddressList.objects.all()
        params = {"name": [self.address_lists[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [self.addresses[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class AddressAssignmentFilterSetTestCase(AddressListMixin, TestCase, ChangeLoggedFilterSetTestMixin):
    queryset = AddressAssignment.objects.all()
    filterset = AddressAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sites = (Site(name="site-1", slug="site-1"),)
        Site.objects.bulk_create(cls.sites)

        cls.manu = (Manufacturer(name="manufacturer-1", slug="manufacturer-1"),)
        Manufacturer.objects.bulk_create(cls.manu)

        cls.types = (
            DeviceType(model="type-1", slug="type-1", manufacturer=cls.manu[0]),
        )
        DeviceType.objects.bulk_create(cls.types)

        cls.roles = (DeviceRole(name="role-1", slug="role-1"),)
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
        cls.address_assignments = (
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
        AddressAssignment.objects.bulk_create(cls.address_assignments)

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
