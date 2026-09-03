from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from dcim.models import Site, Manufacturer
from dcim.models import Device, VirtualDeviceContext, DeviceRole, DeviceType
from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTestMixin

from netbox_security.models import (
    FirewallFilter,
    FirewallFilterRule,
    FirewallFilterAssignment,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
)
from netbox_security.filtersets import (
    FirewallFilterFilterSet,
    FirewallFilterRuleFilterSet,
    FirewallFilterAssignmentFilterSet,
    FirewallRuleFromSettingFilterSet,
    FirewallRuleThenSettingFilterSet,
)
from netbox_security.choices import (
    FamilyChoices,
    FirewallRuleFromSettingChoices,
    FirewallRuleThenSettingChoices,
)


class FirewallFilterFiterSetTestCase(TestCase, ChangeLoggedFilterSetTestMixin):
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


class FirewallFilterRuleFiterSetTestCase(TestCase, ChangeLoggedFilterSetTestMixin):
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


class FirewallFilterAssignmentFilterSetTestCase(
    TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = FirewallFilterAssignment.objects.all()
    filterset = FirewallFilterAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.filters = (
            FirewallFilter(name="filter-4", family=FamilyChoices.INET),
            FirewallFilter(name="filter-5", family=FamilyChoices.INET),
            FirewallFilter(name="filter-6", family=FamilyChoices.INET6),
        )
        FirewallFilter.objects.bulk_create(cls.filters)

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
        cls.assignments = (
            FirewallFilterAssignment(
                firewall_filter=cls.filters[0],
                assigned_object=cls.devices[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[0].pk,),
            ),
            FirewallFilterAssignment(
                firewall_filter=cls.filters[1],
                assigned_object=cls.devices[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[1].pk,),
            ),
            FirewallFilterAssignment(
                firewall_filter=cls.filters[2],
                assigned_object=cls.virtual[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "virtualdevicecontext"
                ),
                assigned_object_id=(cls.virtual[0].pk,),
            ),
        )
        FirewallFilterAssignment.objects.bulk_create(cls.assignments)

    def test_firewall_filter(self):
        params = {"firewall_filter_id": [self.filters[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "firewall_filter_id": [
                self.filters[1].pk,
                self.filters[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"firewall_filter": [self.filters[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "firewall_filter": [
                self.filters[1].name,
                self.filters[2].name,
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


class FirewallRuleFromSettingFilterSetTestCase(
    TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = FirewallRuleFromSetting.objects.all()
    filterset = FirewallRuleFromSettingFilterSet
    ignore_fields = ("from_settings",)

    @classmethod
    def setUpTestData(cls):
        cls.ff = (
            FirewallFilter(name="filter-from-1", family=FamilyChoices.INET),
            FirewallFilter(name="filter-from-2", family=FamilyChoices.INET),
        )
        FirewallFilter.objects.bulk_create(cls.ff)

        cls.rules = (
            FirewallFilterRule(name="rule-from-1", firewall_filter=cls.ff[0], index=10),
            FirewallFilterRule(name="rule-from-2", firewall_filter=cls.ff[1], index=10),
            FirewallFilterRule(name="rule-from-3", firewall_filter=cls.ff[1], index=20),
        )
        for rule in cls.rules:
            rule.save()

        rule_ct = ContentType.objects.get_for_model(FirewallFilterRule)
        cls.settings = (
            FirewallRuleFromSetting(
                key=FirewallRuleFromSettingChoices.ADDRESS,
                value="value-1",
                assigned_object_type=rule_ct,
                assigned_object_id=cls.rules[0].pk,
            ),
            FirewallRuleFromSetting(
                key=FirewallRuleFromSettingChoices.PORT,
                value="value-2",
                assigned_object_type=rule_ct,
                assigned_object_id=cls.rules[1].pk,
            ),
            FirewallRuleFromSetting(
                key=FirewallRuleFromSettingChoices.PROTOCOL,
                value="value-1",
                assigned_object_type=rule_ct,
                assigned_object_id=cls.rules[2].pk,
            ),
        )
        for s in cls.settings:
            s.save()

    def test_key(self):
        params = {"key": [FirewallRuleFromSettingChoices.ADDRESS]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "key": [
                FirewallRuleFromSettingChoices.PORT,
                FirewallRuleFromSettingChoices.PROTOCOL,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_value(self):
        params = {"value": ["value-1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"value": ["value-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_firewall_filter_rule_id(self):
        params = {"firewall_filter_rule_id": [self.rules[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"firewall_filter_rule_id": [self.rules[1].pk, self.rules[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class FirewallRuleThenSettingFilterSetTestCase(
    TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = FirewallRuleThenSetting.objects.all()
    filterset = FirewallRuleThenSettingFilterSet
    ignore_fields = ("then_settings",)

    @classmethod
    def setUpTestData(cls):
        cls.ff = (
            FirewallFilter(name="filter-then-1", family=FamilyChoices.INET),
            FirewallFilter(name="filter-then-2", family=FamilyChoices.INET),
        )
        FirewallFilter.objects.bulk_create(cls.ff)

        cls.rules = (
            FirewallFilterRule(name="rule-then-1", firewall_filter=cls.ff[0], index=10),
            FirewallFilterRule(name="rule-then-2", firewall_filter=cls.ff[1], index=10),
            FirewallFilterRule(name="rule-then-3", firewall_filter=cls.ff[1], index=20),
        )
        for rule in cls.rules:
            rule.save()

        rule_ct = ContentType.objects.get_for_model(FirewallFilterRule)
        cls.settings = (
            FirewallRuleThenSetting(
                key=FirewallRuleThenSettingChoices.ACCEPT,
                value="value-1",
                assigned_object_type=rule_ct,
                assigned_object_id=cls.rules[0].pk,
            ),
            FirewallRuleThenSetting(
                key=FirewallRuleThenSettingChoices.DISCARD,
                value="value-2",
                assigned_object_type=rule_ct,
                assigned_object_id=cls.rules[1].pk,
            ),
            FirewallRuleThenSetting(
                key=FirewallRuleThenSettingChoices.LOG,
                value="value-1",
                assigned_object_type=rule_ct,
                assigned_object_id=cls.rules[2].pk,
            ),
        )
        for s in cls.settings:
            s.save()

    def test_key(self):
        params = {"key": [FirewallRuleThenSettingChoices.ACCEPT]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "key": [
                FirewallRuleThenSettingChoices.DISCARD,
                FirewallRuleThenSettingChoices.LOG,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_value(self):
        params = {"value": ["value-1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"value": ["value-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_firewall_filter_rule_id(self):
        params = {"firewall_filter_rule_id": [self.rules[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"firewall_filter_rule_id": [self.rules[1].pk, self.rules[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
