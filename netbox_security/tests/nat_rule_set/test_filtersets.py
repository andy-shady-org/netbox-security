from django.test import TestCase
from utilities.testing import ChangeLoggedFilterSetTests
from ipam.choices import IPAddressStatusChoices
from ipam.models import IPAddress, Prefix, IPRange

from netbox_security.models import NatPool, NatRuleSet, NatRule, SecurityZone
from netbox_security.filtersets import NatRuleSetFilterSet, NatRuleFilterSet
from netbox_security.choices import (
    PoolTypeChoices,
    RuleStatusChoices,
    AddressTypeChoices,
    RuleDirectionChoices,
    NatTypeChoices,
)


class NatRuleSetFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatRuleSet.objects.all()
    filterset = NatRuleSetFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.zones = (
            SecurityZone(name="DMZ"),
            SecurityZone(name="INTERNAL"),
            SecurityZone(name="PUBLIC"),
            SecurityZone(name="EXTERNAL"),
        )
        for zone in cls.zones:
            zone.save()

        cls.rules = (
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
        for item in cls.rules:
            item.save()
        cls.rules[0].source_zones.add(cls.zones[0])
        cls.rules[0].destination_zones.add(cls.zones[1])
        cls.rules[1].source_zones.set([cls.zones[0], cls.zones[1]])
        cls.rules[1].destination_zones.set([cls.zones[2], cls.zones[3]])
        cls.rules[2].source_zones.set([cls.zones[2], cls.zones[3]])
        cls.rules[2].destination_zones.set([cls.zones[0], cls.zones[1]])

    def test_name(self):
        params = {"name": ["set-4", "set-5"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_nat_type(self):
        params = {"nat_type": [NatTypeChoices.TYPE_STATIC]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"nat_type": [NatTypeChoices.TYPE_IPV4]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_direction(self):
        params = {"direction": [RuleDirectionChoices.DIRECTION_OUTBOUND]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"direction": [RuleDirectionChoices.DIRECTION_INBOUND]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_source_zones(self):
        params = {"source_zone_id": [self.zones[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_zone_id": [self.zones[0].pk, self.zones[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_zone_id": [self.zones[0].pk, self.zones[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"source_zone": [self.zones[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_zone": [self.zones[0].name, self.zones[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"source_zone": [self.zones[0].name, self.zones[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_destination_zones(self):
        params = {"destination_zone_id": [self.zones[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_zone_id": [self.zones[0].pk, self.zones[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_zone_id": [self.zones[1].pk, self.zones[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"destination_zone": [self.zones[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_zone": [self.zones[0].name, self.zones[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"destination_zone": [self.zones[1].name, self.zones[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_security_zones(self):
        params = {"security_zone_id": [self.zones[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"security_zone_id": [self.zones[1].pk, self.zones[3].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class NatRuleFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatRule.objects.all()
    filterset = NatRuleFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.prefixes = (
            Prefix(
                prefix="1.1.1.0/24",
                status="active",
            ),
            Prefix(
                prefix="1.1.2.0/24",
                status="active",
            ),
            Prefix(
                prefix="1.1.3.0/24",
                status="active",
            ),
            Prefix(
                prefix="1.1.4.0/24",
                status="active",
            ),
        )
        Prefix.objects.bulk_create(cls.prefixes)

        cls.addresses = (
            IPAddress(
                address="1.1.1.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.2.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.3.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.4.1/24",
                status="active",
            ),
        )
        IPAddress.objects.bulk_create(cls.addresses)

        cls.ranges = (
            IPRange(
                start_address="1.1.1.2/24",
                end_address="1.1.1.5/24",
                status="active",
                size=4,
            ),
            IPRange(
                start_address="1.1.2.2/24",
                end_address="1.1.2.5/24",
                status="active",
                size=4,
            ),
            IPRange(
                start_address="1.1.3.2/24",
                end_address="1.1.3.5/24",
                status="active",
                size=4,
            ),
            IPRange(
                start_address="1.1.4.2/24",
                end_address="1.1.4.5/24",
                status="active",
                size=4,
            ),
        )
        IPRange.objects.bulk_create(cls.ranges)

        cls.zones = (
            SecurityZone(name="DMZ"),
            SecurityZone(name="INTERNAL"),
            SecurityZone(name="PUBLIC"),
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
        cls.rule_sets[0].source_zones.add(cls.zones[0])
        cls.rule_sets[0].destination_zones.add(cls.zones[1])
        cls.rule_sets[1].source_zones.set([cls.zones[0], cls.zones[1]])
        cls.rule_sets[1].destination_zones.set([cls.zones[2], cls.zones[3]])
        cls.rule_sets[2].source_zones.set([cls.zones[2], cls.zones[3]])
        cls.rule_sets[2].destination_zones.set([cls.zones[0], cls.zones[1]])

        cls.pools = (
            NatPool(
                name="pool-4",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-5",
                pool_type=PoolTypeChoices.HOST_ADDRESS_BASE,
                status=IPAddressStatusChoices.STATUS_RESERVED,
            ),
            NatPool(
                name="pool-6",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-7",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
        )
        for item in cls.pools:
            item.save()

        cls.rules = (
            NatRule(
                name="rule-1",
                rule_set=cls.rule_sets[0],
                pool=cls.pools[0],
                status=RuleStatusChoices.STATUS_RESERVED,
                source_type=AddressTypeChoices.DYNAMIC,
                destination_type=AddressTypeChoices.STATIC,
                source_pool=cls.pools[1],
                destination_pool=cls.pools[2],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            NatRule(
                name="rule-2",
                rule_set=cls.rule_sets[1],
                pool=cls.pools[1],
                status=RuleStatusChoices.STATUS_ACTIVE,
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                source_pool=cls.pools[2],
                destination_pool=cls.pools[0],
                source_ports=[4, 5, 6],
                destination_ports=[1, 2, 3],
            ),
            NatRule(
                name="rule-3",
                rule_set=cls.rule_sets[2],
                pool=cls.pools[2],
                status=RuleStatusChoices.STATUS_ACTIVE,
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.DYNAMIC,
                source_pool=cls.pools[0],
                destination_pool=cls.pools[1],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
        )
        for item in cls.rules:
            item.save()
        cls.rules[0].source_addresses.set([cls.addresses[0], cls.addresses[1]])
        cls.rules[0].destination_addresses.set([cls.addresses[2], cls.addresses[3]])
        cls.rules[1].source_prefixes.set([cls.prefixes[0], cls.prefixes[1]])
        cls.rules[1].destination_prefixes.set([cls.prefixes[2], cls.prefixes[3]])
        cls.rules[2].source_ranges.set([cls.ranges[0], cls.ranges[1]])
        cls.rules[2].destination_ranges.set([cls.ranges[2], cls.ranges[3]])

    def test_name(self):
        params = {"name": ["rule-1", "rule-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_rule_set(self):
        params = {"rule_set_id": [self.rule_sets[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"rule_set_id": [self.rule_sets[0].pk, self.rule_sets[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "rule_set_id": [
                self.rule_sets[0].pk,
                self.rule_sets[1].pk,
                self.rule_sets[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"rule_set": [self.rule_sets[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"rule_set": [self.rule_sets[0].name, self.rule_sets[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "rule_set": [
                self.rule_sets[0].name,
                self.rule_sets[1].name,
                self.rule_sets[2].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_pool(self):
        params = {"pool_id": [self.pools[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"pool_id": [self.pools[0].pk, self.pools[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"pool_id": [self.pools[0].pk, self.pools[1].pk, self.pools[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"pool": [self.pools[0].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"pool": [self.pools[0].name, self.pools[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"pool": [self.pools[0].name, self.pools[1].name, self.pools[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_source_addresses(self):
        params = {"source_address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_address_id": [self.addresses[0].pk, self.addresses[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_address": [self.addresses[0].address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "source_address": [self.addresses[0].address, self.addresses[1].address]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_destination_addresses(self):
        params = {"destination_address_id": [self.addresses[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "destination_address_id": [self.addresses[2].pk, self.addresses[3].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_address": [self.addresses[2].address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "destination_address": [
                self.addresses[2].address,
                self.addresses[3].address,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_source_prefixes(self):
        params = {"source_prefix_id": [self.prefixes[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_prefix_id": [self.prefixes[0].pk, self.prefixes[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_prefix": [self.prefixes[0].prefix]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_prefix": [self.prefixes[0].prefix, self.prefixes[1].prefix]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_destination_prefixes(self):
        params = {"destination_prefix_id": [self.prefixes[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_prefix_id": [self.prefixes[2].pk, self.prefixes[3].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_prefix": [self.prefixes[2].prefix]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "destination_prefix": [self.prefixes[2].prefix, self.prefixes[3].prefix]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_source_ranges(self):
        params = {"source_range_id": [self.ranges[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_range_id": [self.ranges[0].pk, self.ranges[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_range": [self.ranges[0].start_address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "source_range": [self.ranges[0].start_address, self.ranges[1].start_address]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_destination_ranges(self):
        params = {"destination_range_id": [self.ranges[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_range_id": [self.ranges[2].pk, self.ranges[3].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_range": [self.ranges[2].start_address]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {
            "destination_range": [
                self.ranges[2].start_address,
                self.ranges[3].start_address,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_source_pool(self):
        params = {"source_pool_id": [self.pools[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_pool_id": [self.pools[1].pk, self.pools[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "source_pool_id": [self.pools[0].pk, self.pools[1].pk, self.pools[2].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"source_pool": [self.pools[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_pool": [self.pools[1].name, self.pools[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "source_pool": [self.pools[0].pk, self.pools[1].name, self.pools[2].name]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_destination_pool(self):
        params = {"destination_pool_id": [self.pools[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_pool_id": [self.pools[1].pk, self.pools[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "destination_pool_id": [
                self.pools[0].pk,
                self.pools[1].pk,
                self.pools[2].pk,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"destination_pool": [self.pools[1].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_pool": [self.pools[1].name, self.pools[2].name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "destination_pool": [
                self.pools[0].name,
                self.pools[1].name,
                self.pools[2].name,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_status(self):
        params = {"status": [RuleStatusChoices.STATUS_RESERVED]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"status": [RuleStatusChoices.STATUS_ACTIVE]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "status": [
                RuleStatusChoices.STATUS_RESERVED,
                RuleStatusChoices.STATUS_ACTIVE,
            ]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_source_type(self):
        params = {"source_type": [AddressTypeChoices.DYNAMIC]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"source_type": [AddressTypeChoices.STATIC]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "source_type": [AddressTypeChoices.DYNAMIC, AddressTypeChoices.STATIC]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_destination_type(self):
        params = {"destination_type": [AddressTypeChoices.DYNAMIC]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"destination_type": [AddressTypeChoices.STATIC]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "destination_type": [AddressTypeChoices.DYNAMIC, AddressTypeChoices.STATIC]
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

    def test_ip_address_id(self):
        params = {"ip_address_id": [self.addresses[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_prefix_id(self):
        params = {"prefix_id": [self.prefixes[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_ip_range_id(self):
        params = {"ip_range_id": [self.ranges[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
