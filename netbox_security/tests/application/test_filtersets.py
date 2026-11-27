from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from dcim.models import Site, Manufacturer
from dcim.models import Device, VirtualDeviceContext, DeviceRole, DeviceType
from utilities.testing import ChangeLoggedFilterSetTestMixin

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
    ApplicationAssignmentFilterSet,
    ApplicationSetAssignmentFilterSet,
)
from netbox_security.choices import ProtocolChoices
from netbox_security.tests.mixins import ApplicationSetMixin, SecurityZonePolicyMixin


class ApplicationItemFilterSetTestCase(
    ApplicationSetMixin, TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = ApplicationItem.objects.all()
    filterset = ApplicationItemFilterSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.applications[0].application_items.set([cls.items[0], cls.items[1]])
        cls.applications[1].application_items.set([cls.items[2]])

    def test_name(self):
        params = {"name": ["item-1", "item-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["item-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_protocol(self):
        params = {"protocol": [ProtocolChoices.TCP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"protocol": [ProtocolChoices.UDP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"protocol": [ProtocolChoices.UDP, ProtocolChoices.ICMP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"protocol": [ProtocolChoices.GRE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)

    def test_ports(self):
        params = {"source_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_ports": 1}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_application_id(self):
        params = {"application_id": [self.applications[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"application_id": [self.applications[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_application(self):
        params = {"application": [self.applications[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"application": [self.applications[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class ApplicationFilterSetTestCase(
    SecurityZonePolicyMixin, TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = Application.objects.all()
    filterset = ApplicationFilterSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.applications[1].application_items.set(
            [
                cls.items[0],
                cls.items[2],
            ]
        )
        cls.applications[2].application_items.set([cls.items[1], cls.items[2]])
        cls.policies[0].applications.set([cls.applications[0]])
        cls.policies[1].applications.set([cls.applications[0], cls.applications[1]])
        cls.policies[2].applications.set([cls.applications[0], cls.applications[2]])

    def test_name(self):
        params = {"name": ["item-1", "item-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["item-3"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_tenant(self):
        params = {"tenant_id": [self.tenants[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"tenant_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"tenant": [self.tenants[0].slug, self.tenants[2].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_protocol(self):
        params = {"protocol": [ProtocolChoices.ICMP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"protocol": [ProtocolChoices.UDP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"protocol": [ProtocolChoices.TCP]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"protocol": [ProtocolChoices.GRE]}
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
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_ports": 4}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class ApplicationSetFilterSetTestCase(
    SecurityZonePolicyMixin, TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = ApplicationSet.objects.all()
    filterset = ApplicationSetFilterSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.applications[1].application_items.set([cls.items[0]])
        cls.applications[2].application_items.set([cls.items[1]])
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
        cls.policies[0].application_sets.set([cls.application_sets[0]])
        cls.policies[1].application_sets.set(
            [cls.application_sets[0], cls.application_sets[1]]
        )
        cls.policies[2].application_sets.set(
            [cls.application_sets[0], cls.application_sets[2]]
        )

    def test_name(self):
        params = {"name": ["set-1", "set-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"name": ["set-3"]}
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


class ApplicationAssignmentFilterSetTestCase(
    SecurityZonePolicyMixin, TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = ApplicationAssignment.objects.all()
    filterset = ApplicationAssignmentFilterSet

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


class ApplicationSetAssignmentFilterSetTestCase(
    SecurityZonePolicyMixin, TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = ApplicationSetAssignment.objects.all()
    filterset = ApplicationSetAssignmentFilterSet

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
