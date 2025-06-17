from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import Address, AddressSet, AddressList
from netbox_security.filtersets import AddressSetFilterSet, AddressListFilterSet


class AddressSetFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = AddressSet.objects.all()
    filterset = AddressSetFilterSet

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

        cls.addresses = (
            Address(name="address-1", address="1.1.1.4/32", tenant=cls.tenants[0]),
            Address(name="address-2", address="1.1.1.5/32", tenant=cls.tenants[1]),
            Address(name="address-3", address="1.1.1.6/32", tenant=cls.tenants[2]),
        )
        Address.objects.bulk_create(cls.addresses)

        cls.address_sets = (
            AddressSet(name="address-set-1", tenant=cls.tenants[0]),
            AddressSet(name="address-set-2", tenant=cls.tenants[1]),
            AddressSet(name="address-set-3", tenant=cls.tenants[2]),
        )
        AddressSet.objects.bulk_create(cls.address_sets)
        cls.address_sets[0].addresses.add(cls.addresses[0])
        cls.address_sets[1].addresses.add(cls.addresses[1])
        cls.address_sets[1].addresses.add(cls.addresses[2])

        cls.assignments = (
            AddressList(
                name="address-list-1",
                assigned_object=cls.address_sets[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "netbox_security", "addressset"
                ),
                assigned_object_id=cls.address_sets[0].pk,
            ),
        )
        for assignment in cls.assignments:
            assignment.save()

    def test_name(self):
        params = {"name": ["address-set-1", "address-set-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

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
        params = {"address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [self.addresses[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address_id": [self.addresses[1].pk, self.addresses[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"address": [self.addresses[1].name, self.addresses[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_assignment(self):
        self.filterset = AddressListFilterSet
        self.queryset = AddressList.objects.all()
        params = {"name": [self.assignments[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"addressset_id": [self.address_sets[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"addressset": [self.address_sets[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
