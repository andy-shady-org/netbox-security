from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import (
    SecurityZonePolicy,
    SecurityZone,
    Address,
    AddressSet,
    AddressList,
    NatRuleSet,
)

from netbox_security.filtersets import (
    SecurityZoneFilterSet,
    SecurityZonePolicyFilterSet,
    RuleDirectionChoices,
    NatTypeChoices,
    ActionChoices,
)


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
            SecurityZone(name="EXTERNAL"),
        )
        for zone in cls.zones:
            zone.save()

        cls.rule_sets = (
            NatRuleSet(
                name="set-4",
                nat_type=NatTypeChoices.TYPE_IPV4,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-5",
                nat_type=NatTypeChoices.TYPE_IPV4,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-6",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_OUTBOUND,
            ),
        )
        for item in cls.rule_sets:
            item.save()
            item.source_zones.set([cls.zones[0], cls.zones[1]])
            item.destination_zones.set([cls.zones[2], cls.zones[3]])

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

    def test_natruleset_source_zones(self):
        params = {"natruleset_source_zone_id": [self.rule_sets[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 4)

    def test_natruleset_destination_zones(self):
        params = {"natruleset_destination_zone_id": [self.rule_sets[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 4)


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

        cls.addresses = (
            Address(name="address-1", value="1.1.1.4/32"),
            Address(name="address-2", value="1.1.1.5/32"),
            Address(name="address-3", value="1.1.1.6/32"),
        )
        Address.objects.bulk_create(cls.addresses)

        cls.address_sets = (
            AddressSet(name="address-set-1"),
            AddressSet(name="address-set-2"),
        )
        AddressSet.objects.bulk_create(cls.address_sets)
        cls.address_sets[0].addresses.add(cls.addresses[0])
        cls.address_sets[1].addresses.add(cls.addresses[1])

        cls.assignments = (
            AddressList(
                name="address-list-1",
                assigned_object=cls.address_sets[0],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "netbox_security", "addressset"
                ),
                assigned_object_id=cls.addresses[0].pk,
            ),
            AddressList(
                name="address-list-2",
                assigned_object=cls.address_sets[1],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "netbox_security", "addressset"
                ),
                assigned_object_id=cls.address_sets[1].pk,
            ),
            AddressList(
                name="address-list-3",
                assigned_object=cls.addresses[2],
                assigned_object_type=ContentType.objects.get_by_natural_key(
                    "netbox_security", "address"
                ),
                assigned_object_id=cls.addresses[2].pk,
            ),
        )
        for assignment in cls.assignments:
            assignment.save()
        cls.policies = (
            SecurityZonePolicy(
                name="policy-1",
                index=5,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                actions=[ActionChoices.PERMIT, ActionChoices.COUNT, ActionChoices.LOG],
                application=["test-1", "test-2"],
            ),
            SecurityZonePolicy(
                name="policy-2",
                index=6,
                source_zone=cls.zones[1],
                destination_zone=cls.zones[0],
                actions=[ActionChoices.PERMIT, ActionChoices.COUNT, ActionChoices.LOG],
                application=["test-1", "test-2"],
            ),
            SecurityZonePolicy(
                name="policy-3",
                index=6,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                actions=[ActionChoices.DENY, ActionChoices.COUNT, ActionChoices.LOG],
                application=["test-1", "test-2"],
            ),
        )
        for policy in cls.policies:
            policy.save()
        cls.policies[0].source_address.add(cls.assignments[0])
        cls.policies[0].destination_address.add(cls.assignments[1])
        cls.policies[1].source_address.add(cls.assignments[1])
        cls.policies[1].destination_address.add(cls.assignments[0])
        cls.policies[2].source_address.add(cls.assignments[2])
        cls.policies[2].destination_address.add(cls.assignments[0])

    def test_name(self):
        params = {"name": ["policy-1", "policy-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_source_zone(self):
        params = {"source_zone_id": [self.zones[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_zone_id": [self.zones[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_zone": [self.zones[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_zone": [self.zones[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_destination_zone(self):
        params = {"destination_zone_id": [self.zones[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_zone_id": [self.zones[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_zone": [self.zones[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_zone": [self.zones[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_source_address(self):
        params = {"source_address_id": [self.assignments[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_address_id": [self.assignments[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_address_id": [self.assignments[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_address": [self.assignments[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_address": [self.assignments[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_address": [self.assignments[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_destination_address(self):
        params = {"destination_address_id": [self.assignments[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_address_id": [self.assignments[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_address_id": [self.assignments[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
        params = {"destination_address": [self.assignments[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_address": [self.assignments[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_address": [self.assignments[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
