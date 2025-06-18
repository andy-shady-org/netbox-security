from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ipam.models import IPRange
from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import Address, AddressList, AddressSet
from netbox_security.filtersets import AddressFilterSet, AddressListFilterSet


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
