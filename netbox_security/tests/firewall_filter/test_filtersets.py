from django.test import TestCase

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import FirewallFilter, FirewallFilterRule
from netbox_security.filtersets import (
    FirewallFilterFilterSet,
    FirewallFilterRuleFilterSet,
)
from netbox_security.choices import FamilyChoices


class FirewallFilterFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = FirewallFilter.objects.all()
    filterset = FirewallFilterFilterSet

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

        cls.filters = (
            FirewallFilter(
                name="filter-4", tenant=cls.tenants[0], family=FamilyChoices.INET
            ),
            FirewallFilter(
                name="filter-5", tenant=cls.tenants[1], family=FamilyChoices.INET
            ),
            FirewallFilter(
                name="filter-6", tenant=cls.tenants[2], family=FamilyChoices.INET6
            ),
        )
        for item in cls.filters:
            item.save()

    def test_name(self):
        params = {"name": ["filter-4", "filter-5"]}
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

    def test_family(self):
        params = {"family": [FamilyChoices.INET]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"family": [FamilyChoices.INET6]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class FirewallFilterRuleFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = FirewallFilterRule.objects.all()
    filterset = FirewallFilterRuleFilterSet

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

        cls.filters = (
            FirewallFilter(
                name="filter-4", tenant=cls.tenants[0], family=FamilyChoices.INET
            ),
            FirewallFilter(
                name="filter-5", tenant=cls.tenants[1], family=FamilyChoices.INET
            ),
            FirewallFilter(
                name="filter-6", tenant=cls.tenants[2], family=FamilyChoices.INET6
            ),
        )
        for item in cls.filters:
            item.save()

        cls.rules = (
            FirewallFilterRule(name="rule-1", firewall_filter=cls.filters[0], index=10),
            FirewallFilterRule(name="rule-2", firewall_filter=cls.filters[1], index=10),
            FirewallFilterRule(name="rule-3", firewall_filter=cls.filters[2], index=10),
        )
        for rule in cls.rules:
            rule.save()

    def test_name(self):
        params = {"name": ["rule-1", "rule-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_firewall_filter(self):
        params = {"firewall_filter_id": [self.filters[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"firewall_filter_id": [self.filters[1].pk, self.filters[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"firewall_filter": [self.filters[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"firewall_filter": [self.filters[1].name, self.filters[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
