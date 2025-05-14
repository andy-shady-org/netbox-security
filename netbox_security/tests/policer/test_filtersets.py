from django.test import TestCase

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import Policer
from netbox_security.filtersets import PolicerFilterSet
from netbox_security.choices import (
    LossPriorityChoices,
    ForwardingClassChoices,
)


class PolicerFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = Policer.objects.all()
    filterset = PolicerFilterSet

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

        cls.policers = (
            Policer(
                name="policer-1",
                loss_priority=LossPriorityChoices.HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
                tenant=cls.tenants[0],
            ),
            Policer(
                name="policer-2",
                loss_priority=LossPriorityChoices.HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
                tenant=cls.tenants[1],
            ),
            Policer(
                name="policer-3",
                loss_priority=LossPriorityChoices.HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
                tenant=cls.tenants[2],
            ),
        )
        for policer in cls.policers:
            policer.save()

    def test_name(self):
        params = {"name": ["policer-1", "policer-2"]}
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

    def test_loss_priority(self):
        params = {"loss_priority": [LossPriorityChoices.HIGH]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_forwarding_class(self):
        params = {"forwarding_class": [ForwardingClassChoices.ASSURED_FORWARDING]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_logical_interface_policer(self):
        params = {"logical_interface_policer": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"logical_interface_policer": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)

    def test_physical_interface_policer(self):
        params = {"physical_interface_policer": False}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"physical_interface_policer": True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
