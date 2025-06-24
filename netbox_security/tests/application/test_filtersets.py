from django.test import TestCase

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import ApplicationItem, Application, ApplicationSet
from netbox_security.filtersets import (
    ApplicationItemFilterSet,
    ApplicationFilterSet,
    ApplicationSetFilterSet,
    SecurityZone,
    SecurityZonePolicy,
)
from netbox_security.choices import ProtocolChoices, ActionChoices


class ApplicationItemFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationItem.objects.all()
    filterset = ApplicationItemFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.items = (
            ApplicationItem(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-3",
                protocol=ProtocolChoices.UDP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

    def test_name(self):
        params = {"name": ["item-1", "item-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["item-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_protocol(self):
        params = {"protocol": [ProtocolChoices.TCP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"protocol": [ProtocolChoices.UDP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class ApplicationFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Application.objects.all()
    filterset = ApplicationFilterSet

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

        cls.items = (
            ApplicationItem(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-3",
                protocol=ProtocolChoices.UDP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-1",
                protocol=ProtocolChoices.ICMP,
                destination_port=1,
                source_port=1,
                tenant=cls.tenants[0],
            ),
            Application(name="item-2"),
            Application(
                name="item-3",
                tenant=cls.tenants[2],
            ),
        )
        Application.objects.bulk_create(cls.applications)
        cls.applications[1].application_items.set(
            [
                cls.items[0],
                cls.items[2],
            ]
        )
        cls.applications[2].application_items.set([cls.items[1], cls.items[2]])

        cls.zones = (
            SecurityZone(name="DMZ", tenant=cls.tenants[0]),
            SecurityZone(name="INTERNAL", tenant=cls.tenants[1]),
            SecurityZone(name="PUBLIC", tenant=cls.tenants[2]),
            SecurityZone(name="EXTERNAL"),
        )
        for zone in cls.zones:
            zone.save()

        cls.policies = (
            SecurityZonePolicy(
                name="policy-1",
                index=5,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                policy_actions=[
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
            SecurityZonePolicy(
                name="policy-2",
                index=6,
                source_zone=cls.zones[1],
                destination_zone=cls.zones[0],
                policy_actions=[
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
            SecurityZonePolicy(
                name="policy-3",
                index=6,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                policy_actions=[
                    ActionChoices.DENY,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
        )
        for policy in cls.policies:
            policy.save()

        cls.policies[0].applications.set([cls.applications[0]])
        cls.policies[1].applications.set([cls.applications[0], cls.applications[1]])
        cls.policies[2].applications.set([cls.applications[0], cls.applications[2]])

    def test_name(self):
        params = {"name": ["item-1", "item-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["item-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_tenant(self):
        params = {"tenant_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"tenant": [self.tenants[0].slug, self.tenants[2].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_protocol(self):
        params = {"protocol": [ProtocolChoices.ICMP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"protocol": [ProtocolChoices.UDP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)

    def test_items(self):
        params = {"application_items": [self.items[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"application_items": [self.items[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"application_items": [self.items[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"application_items": [self.items[0].name, self.items[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "application_items_id": [
                self.items[0].pk,
                self.items[1].pk,
                self.items[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_security_zone_policies(self):
        params = {"security_zone_policy_id": [self.policies[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"security_zone_policy_id": [self.policies[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"security_zone_policy_id": [self.policies[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "security_zone_policy_id": [
                self.policies[1].pk,
                self.policies[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)


class ApplicationSetFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationSet.objects.all()
    filterset = ApplicationSetFilterSet

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

        cls.items = (
            ApplicationItem(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-3",
                protocol=ProtocolChoices.UDP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                tenant=cls.tenants[0],
            ),
            Application(name="item-2", tenant=cls.tenants[1]),
            Application(
                name="item-3",
                tenant=cls.tenants[2],
            ),
        )
        Application.objects.bulk_create(cls.applications)
        cls.applications[1].application_items.set([cls.items[0]])
        cls.applications[2].application_items.set([cls.items[1]])

        cls.application_sets = (
            ApplicationSet(name="item-1", tenant=cls.tenants[0]),
            ApplicationSet(
                name="item-2",
                tenant=cls.tenants[1],
            ),
            ApplicationSet(
                name="item-3",
                tenant=cls.tenants[2],
            ),
        )
        ApplicationSet.objects.bulk_create(cls.application_sets)
        cls.application_sets[0].applications.set(
            [
                cls.applications[0],
            ]
        )
        cls.application_sets[1].applications.set(
            [
                cls.applications[0],
                cls.applications[1],
            ]
        )
        cls.application_sets[2].applications.set(
            [
                cls.applications[0],
                cls.applications[1],
                cls.applications[2],
            ]
        )
        cls.zones = (
            SecurityZone(name="DMZ", tenant=cls.tenants[0]),
            SecurityZone(name="INTERNAL", tenant=cls.tenants[1]),
            SecurityZone(name="PUBLIC", tenant=cls.tenants[2]),
            SecurityZone(name="EXTERNAL"),
        )
        for zone in cls.zones:
            zone.save()

        cls.policies = (
            SecurityZonePolicy(
                name="policy-1",
                index=5,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                policy_actions=[
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
            SecurityZonePolicy(
                name="policy-2",
                index=6,
                source_zone=cls.zones[1],
                destination_zone=cls.zones[0],
                policy_actions=[
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
            SecurityZonePolicy(
                name="policy-3",
                index=6,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                policy_actions=[
                    ActionChoices.DENY,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
        )
        for policy in cls.policies:
            policy.save()

        cls.policies[0].application_sets.set([cls.application_sets[0]])
        cls.policies[1].application_sets.set(
            [cls.application_sets[0], cls.application_sets[1]]
        )
        cls.policies[2].application_sets.set(
            [cls.application_sets[0], cls.application_sets[2]]
        )

    def test_name(self):
        params = {"name": ["item-1", "item-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["item-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_tenant(self):
        params = {"tenant_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"tenant": [self.tenants[0].slug, self.tenants[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_applications(self):
        params = {"applications": [self.applications[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"applications": [self.applications[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"applications": [self.applications[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "applications_id": [
                self.applications[0].pk,
                self.applications[1].pk,
                self.applications[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_security_zone_policies(self):
        params = {"security_zone_policy_id": [self.policies[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"security_zone_policy_id": [self.policies[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"security_zone_policy_id": [self.policies[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "security_zone_policy_id": [
                self.policies[1].pk,
                self.policies[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
