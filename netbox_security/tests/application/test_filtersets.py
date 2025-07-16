from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from dcim.models import Site, Manufacturer
from dcim.models import Device, VirtualDeviceContext, DeviceRole, DeviceType
from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import (
    ApplicationItem,
    Application,
    ApplicationSet,
    ApplicationAssignment,
    ApplicationSetAssignment,
)
from netbox_security.filtersets import (
    ApplicationItemFilterSet,
    ApplicationFilterSet,
    ApplicationSetFilterSet,
    SecurityZone,
    SecurityZonePolicy,
    ApplicationAssignmentFilterSet,
    ApplicationSetAssignmentFilterSet,
)
from netbox_security.choices import ProtocolChoices, ActionChoices


class ApplicationItemFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationItem.objects.all()
    filterset = ApplicationItemFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.items = (
            ApplicationItem(
                name="item-1",
                protocol=[ProtocolChoices.TCP],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
                index=1,
            ),
            ApplicationItem(
                name="item-2",
                protocol=[ProtocolChoices.TCP],
                source_ports=[4, 5, 6],
                destination_ports=[1, 2, 3],
                index=1,
            ),
            ApplicationItem(
                name="item-3",
                protocol=[ProtocolChoices.UDP],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
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

    def test_ports(self):
        params = {"source_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class ApplicationFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
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
                name="item-7",
                protocol=[ProtocolChoices.TCP],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
                index=1,
            ),
            ApplicationItem(
                name="item-8",
                protocol=[ProtocolChoices.TCP],
                source_ports=[4, 5, 6],
                destination_ports=[1, 2, 3],
                index=1,
            ),
            ApplicationItem(
                name="item-9",
                protocol=[ProtocolChoices.UDP],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-1",
                protocol=[ProtocolChoices.ICMP],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
                tenant=cls.tenants[0],
            ),
            Application(
                name="item-2",
                source_ports=[4, 5, 6],
                destination_ports=[1, 2, 3],
            ),
            Application(
                name="item-3",
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
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

    def test_ports(self):
        params = {"source_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class ApplicationSetFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
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
                name="item-7",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-8",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-9",
                protocol=[ProtocolChoices.UDP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-1",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
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


class ApplicationAssignmentFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationAssignment.objects.all()
    filterset = ApplicationAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.applications = (
            Application(
                name="item-1",
                protocol=[ProtocolChoices.ICMP],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            Application(
                name="item-2",
                source_ports=[4, 5, 6],
                destination_ports=[1, 2, 3],
            ),
            Application(
                name="item-3",
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
        )
        Application.objects.bulk_create(cls.applications)

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
            ApplicationAssignment(
                application=cls.applications[0],
                assigned_object=cls.devices[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[0].pk,),
            ),
            ApplicationAssignment(
                application=cls.applications[1],
                assigned_object=cls.devices[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[1].pk,),
            ),
            ApplicationAssignment(
                application=cls.applications[2],
                assigned_object=cls.virtual[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "virtualdevicecontext"
                ),
                assigned_object_id=(cls.virtual[0].pk,),
            ),
        )
        ApplicationAssignment.objects.bulk_create(cls.assignments)

    def test_application(self):
        params = {"application_id": [self.applications[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "application_id": [
                self.applications[1].pk,
                self.applications[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"application": [self.applications[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "application": [
                self.applications[1].name,
                self.applications[2].name,
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


class ApplicationSetAssignmentFilterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationSetAssignment.objects.all()
    filterset = ApplicationSetAssignmentFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.application_sets = (
            ApplicationSet(
                name="item-1",
            ),
            ApplicationSet(
                name="item-2",
            ),
            ApplicationSet(
                name="item-3",
            ),
        )
        ApplicationSet.objects.bulk_create(cls.application_sets)

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
            ApplicationSetAssignment(
                application_set=cls.application_sets[0],
                assigned_object=cls.devices[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[0].pk,),
            ),
            ApplicationSetAssignment(
                application_set=cls.application_sets[1],
                assigned_object=cls.devices[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "device"
                ),
                assigned_object_id=(cls.devices[1].pk,),
            ),
            ApplicationSetAssignment(
                application_set=cls.application_sets[2],
                assigned_object=cls.virtual[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "dcim", "virtualdevicecontext"
                ),
                assigned_object_id=(cls.virtual[0].pk,),
            ),
        )
        ApplicationSetAssignment.objects.bulk_create(cls.assignments)

    def test_application(self):
        params = {"application_set_id": [self.application_sets[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "application_set_id": [
                self.application_sets[1].pk,
                self.application_sets[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"application_set": [self.application_sets[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "application_set": [
                self.application_sets[1].name,
                self.application_sets[2].name,
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
