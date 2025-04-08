from django.test import TestCase

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import SecurityZone, SecurityZonePolicy
from netbox_security.filtersets import SecurityZoneFilterSet, SecurityZonePolicyFilterSet


class SecurityZoneFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = SecurityZone.objects.all()
    filterset = SecurityZoneFilterSet

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

        cls.zones = (
            SecurityZone(name="DMZ", tenant=cls.tenants[0]),
            SecurityZone(name="INTERNAL", tenant=cls.tenants[1]),
            SecurityZone(name="PUBLIC", tenant=cls.tenants[2]),
        )
        for zone in cls.zones:
            zone.save()

    def test_name(self):
        params = {"name": ["DMZ", "INTERNAL"]}
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

    def test_zones(self):
        params = {"securityzone_id": [self.zones[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"securityzone_id": [self.zones[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"securityzone_id": [self.zones[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)


class SecurityZonePolicyFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = SecurityZonePolicy.objects.all()
    filterset = SecurityZonePolicyFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.zones = (
            SecurityZone(name="ZONE-3"),
            SecurityZone(name="ZONE-4"),
        )
        for zone in cls.zones:
            zone.save()

        cls.policies = (
            SecurityZonePolicy(name="policy-1", index=5,
                               source_zone=cls.zones[0],
                               destination_zone=cls.zones[1],
                               actions=["permit", "count", "log"],
                               application=['test-1', 'test-2']),
            SecurityZonePolicy(name="policy-2", index=6,
                               source_zone=cls.zones[0],
                               destination_zone=cls.zones[1],
                               actions=["permit", "count", "log"],
                               application=['test-1', 'test-2']),
            SecurityZonePolicy(name="policy-3", index=6,
                               source_zone=cls.zones[0],
                               destination_zone=cls.zones[1],
                               actions=["permit", "count", "log"],
                               application=['test-1', 'test-2']),
        )
        for policy in cls.policies:
            policy.save()

    def test_name(self):
        params = {"name": ["policy-1", "policy-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_zone(self):
        params = {"securityzone_id": [self.zones[0].pk, self.zones[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"securityzone": [self.zones[0].name, self.zones[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_policies(self):
        params = {"securityzonepolicy_id": [self.policies[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"securityzonepolicy_id": [self.policies[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"securityzonepolicy_id": [self.policies[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
