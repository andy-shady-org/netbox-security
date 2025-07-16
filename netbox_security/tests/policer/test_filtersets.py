from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from dcim.models import Site, Manufacturer
from dcim.models import Device, VirtualDeviceContext, DeviceRole, DeviceType
from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import Policer, PolicerAssignment
from netbox_security.filtersets import PolicerFilterSet, PolicerAssignmentFilterSet
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


class PolicerAssignmentFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = PolicerAssignment.objects.all()
    filterset = PolicerAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.policers = (
            Policer(
                name="policer-1",
                loss_priority=LossPriorityChoices.HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
            ),
            Policer(
                name="policer-2",
                loss_priority=LossPriorityChoices.HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
            ),
            Policer(
                name="policer-3",
                loss_priority=LossPriorityChoices.HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
            ),
        )
        Policer.objects.bulk_create(cls.policers)

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
            PolicerAssignment(
                policer=cls.policers[0],
                assigned_object=cls.devices[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[0].pk,),
            ),
            PolicerAssignment(
                policer=cls.policers[1],
                assigned_object=cls.devices[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[1].pk,),
            ),
            PolicerAssignment(
                policer=cls.policers[2],
                assigned_object=cls.virtual[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "virtualdevicecontext"
                ),
                assigned_object_id=(cls.virtual[0].pk,),
            ),
        )
        PolicerAssignment.objects.bulk_create(cls.assignments)

    def test_policer(self):
        params = {"policer_id": [self.policers[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "policer_id": [
                self.policers[1].pk,
                self.policers[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"policer": [self.policers[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "policer": [
                self.policers[1].name,
                self.policers[2].name,
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
