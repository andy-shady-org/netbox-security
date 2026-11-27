from netaddr import IPNetwork
from django.contrib.contenttypes.models import ContentType

from tenancy.models import Tenant, TenantGroup
from ipam.models import IPRange, Prefix, IPAddress
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import (
    CustomPrefix,
    Address,
    AddressSet,
    AddressList,
    ApplicationItem,
    Application,
    ApplicationSet,
    FirewallFilter,
    FirewallFilterRule,
    NatPool,
    NatPoolMember,
    NatRuleSet,
    NatRule,
    Policer,
    SecurityZone,
    SecurityZonePolicy,
)

from netbox_security.choices import (
    ProtocolChoices,
    FamilyChoices,
    PoolTypeChoices,
    RuleDirectionChoices,
    NatTypeChoices,
    RuleStatusChoices,
    AddressTypeChoices,
    ActionChoices,
    LossPriorityChoices,
    ForwardingClassChoices,
)


class Base:
    @classmethod
    def setUpTestData(cls):
        pass


class TenantGroupMixin(Base):
    model = TenantGroup

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.tenant_groups = (
            TenantGroupMixin.model(name="tenant-group-1", slug="tenant-group-1"),
            TenantGroupMixin.model(name="tenant-group-2", slug="tenant-group-2"),
            TenantGroupMixin.model(name="tenant-group-3", slug="tenant-group-3"),
        )
        TenantGroupMixin.model.objects.bulk_create(cls.tenant_groups)


class TenantMixin(TenantGroupMixin):
    model = Tenant

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.tenants = (
            TenantMixin.model(
                name="tenant-1", slug="tenant-1", group=cls.tenant_groups[0]
            ),
            TenantMixin.model(
                name="tenant-2", slug="tenant-2", group=cls.tenant_groups[1]
            ),
            TenantMixin.model(
                name="tenant-3", slug="tenant-3", group=cls.tenant_groups[2]
            ),
        )
        TenantMixin.model.objects.bulk_create(cls.tenants)


class IPRangeMixin(Base):
    model = IPRange

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ranges = (
            IPRangeMixin.model(
                start_address=IPNetwork("1.1.1.2/24"),
                end_address=IPNetwork("1.1.1.5/24"),
                status="active",
                size=4,
            ),
            IPRangeMixin.model(
                start_address=IPNetwork("1.1.2.2/24"),
                end_address=IPNetwork("1.1.2.5/24"),
                status="active",
                size=4,
            ),
            IPRangeMixin.model(
                start_address=IPNetwork("1.1.3.2/24"),
                end_address=IPNetwork("1.1.3.5/24"),
                status="active",
                size=4,
            ),
        )
        IPRangeMixin.model.objects.bulk_create(cls.ranges)


class PrefixMixin(Base):
    model = Prefix

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.prefixes = (
            PrefixMixin.model(prefix=IPNetwork("1.1.1.0/24")),
            PrefixMixin.model(prefix=IPNetwork("1.1.2.0/24")),
            PrefixMixin.model(prefix=IPNetwork("1.1.3.0/24")),
        )
        PrefixMixin.model.objects.bulk_create(cls.prefixes)


class IPAddressMixin(Base):
    model = IPAddress

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.ip_addresses = (
            IPAddressMixin.model(address=IPNetwork("1.1.1.1/24")),
            IPAddressMixin.model(address=IPNetwork("1.1.2.1/24")),
            IPAddressMixin.model(address=IPNetwork("1.1.3.1/24")),
        )
        IPAddressMixin.model.objects.bulk_create(cls.ip_addresses)


class CustomPrefixMixin(TenantMixin):
    model = CustomPrefix

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.custom_prefixes = (
            CustomPrefixMixin.model(
                prefix=IPNetwork("1.1.1.1/32"), tenant=cls.tenants[0]
            ),
            CustomPrefixMixin.model(
                prefix=IPNetwork("1.1.1.2/32"), tenant=cls.tenants[1]
            ),
            CustomPrefixMixin.model(
                prefix=IPNetwork("1.1.1.3/32"), tenant=cls.tenants[2]
            ),
        )
        CustomPrefixMixin.model.objects.bulk_create(cls.custom_prefixes)


class AddressMixin(CustomPrefixMixin, IPRangeMixin, PrefixMixin, IPAddressMixin):
    model = Address

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.addresses = (
            AddressMixin.model(
                name="address-1",
                assigned_object_id=cls.prefixes[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="prefix"
                ),
                tenant=cls.tenants[0],
            ),
            AddressMixin.model(
                name="address-2",
                assigned_object_id=cls.ranges[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="iprange"
                ),
                tenant=cls.tenants[1],
            ),
            AddressMixin.model(
                name="address-3",
                assigned_object_id=cls.custom_prefixes[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
                tenant=cls.tenants[2],
            ),
            AddressMixin.model(
                name="address-4",
                assigned_object_id=cls.ip_addresses[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="ipaddress"
                ),
                tenant=cls.tenants[2],
            ),
            AddressMixin.model(
                name="address-5", dns_name="test.example.com", tenant=cls.tenants[2]
            ),
        )
        AddressMixin.model.objects.bulk_create(cls.addresses)


class AddressSetMixin(AddressMixin):
    model = AddressSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.address_sets = (
            AddressSetMixin.model(name="address-set-1", tenant=cls.tenants[0]),
            AddressSetMixin.model(name="address-set-2", tenant=cls.tenants[1]),
            AddressSetMixin.model(name="address-set-3", tenant=cls.tenants[2]),
        )
        AddressSetMixin.model.objects.bulk_create(cls.address_sets)


class AddressListMixin(AddressSetMixin):
    model = AddressList

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.address_lists = (
            AddressListMixin.model(
                name="address-list-1",
                assigned_object_id=cls.addresses[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="address"
                ),
            ),
            AddressListMixin.model(
                name="address-list-2",
                assigned_object_id=cls.addresses[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="address"
                ),
            ),
            AddressListMixin.model(
                name="address-list-3",
                assigned_object_id=cls.address_sets[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="addressset"
                ),
            ),
            AddressListMixin.model(
                name="address-list-4",
                assigned_object_id=cls.address_sets[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="addressset"
                ),
            ),
        )
        cls.destination_addresses = (cls.address_lists[1], cls.address_lists[2])
        AddressListMixin.model.objects.bulk_create(cls.address_lists)


class ApplicationItemMixin(TenantMixin):
    model = ApplicationItem

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.items = (
            ApplicationItemMixin.model(
                name="item-1",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItemMixin.model(
                name="item-2",
                protocol=[ProtocolChoices.UDP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItemMixin.model(
                name="item-3",
                protocol=[ProtocolChoices.ICMP],
                destination_ports=[4],
                source_ports=[4],
                index=1,
            ),
        )
        ApplicationItemMixin.model.objects.bulk_create(cls.items)


class ApplicationMixin(ApplicationItemMixin):
    model = Application

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.applications = (
            ApplicationMixin.model(
                name="item-1",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                tenant=cls.tenants[0],
            ),
            ApplicationMixin.model(
                name="item-2",
                protocol=[ProtocolChoices.ICMP],
                destination_ports=[1],
                source_ports=[1],
                tenant=cls.tenants[1],
            ),
            ApplicationMixin.model(
                name="item-3",
                protocol=[ProtocolChoices.UDP],
                destination_ports=[4],
                source_ports=[4],
                tenant=cls.tenants[2],
            ),
        )
        ApplicationMixin.model.objects.bulk_create(cls.applications)


class ApplicationSetMixin(ApplicationMixin):
    model = ApplicationSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.application_sets = (
            ApplicationSetMixin.model(name="set-1", tenant=cls.tenants[0]),
            ApplicationSetMixin.model(name="set-2", tenant=cls.tenants[1]),
            ApplicationSetMixin.model(name="set-3", tenant=cls.tenants[2]),
        )
        ApplicationSetMixin.model.objects.bulk_create(cls.application_sets)


class FirewallFilterMixin(Base):
    model = FirewallFilter

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.filters = (
            FirewallFilterMixin.model(name="filter-1", family=FamilyChoices.INET),
            FirewallFilterMixin.model(name="filter-2", family=FamilyChoices.INET),
            FirewallFilterMixin.model(name="filter-3", family=FamilyChoices.INET),
        )
        FirewallFilterMixin.model.objects.bulk_create(cls.filters)


class FirewallFilterRuleMixin(FirewallFilterMixin):
    model = FirewallFilterRule

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.rules = (
            FirewallFilterRuleMixin.model(
                name="rule-1", firewall_filter=cls.filters[0], index=1
            ),
            FirewallFilterRuleMixin.model(
                name="rule-2", firewall_filter=cls.filters[1], index=1
            ),
            FirewallFilterRuleMixin.model(
                name="rule-3", firewall_filter=cls.filters[2], index=1
            ),
        )
        for rule in cls.rules:
            rule.save()


class NatPoolMixin(Base):
    model = NatPool

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.pools = (
            NatPoolMixin.model(
                name="pool-1",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPoolMixin.model(name="pool-2"),
            NatPoolMixin.model(name="pool-3"),
        )
        NatPoolMixin.model.objects.bulk_create(cls.pools)


class NatPoolMemberMixin(NatPoolMixin, IPAddressMixin, PrefixMixin, IPRangeMixin):
    model = NatPoolMember

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.members = (
            NatPoolMemberMixin.model(
                name="member-1",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                prefix=cls.prefixes[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            NatPoolMemberMixin.model(
                name="member-2",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                address=cls.ip_addresses[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            NatPoolMemberMixin.model(
                name="member-3",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                address_range=cls.ranges[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
        )
        NatPoolMemberMixin.model.objects.bulk_create(cls.members)


class NatRuleSetMixin(Base):
    model = NatRuleSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.rule_sets = (
            NatRuleSetMixin.model(
                name="set-4",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSetMixin.model(
                name="set-5",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSetMixin.model(
                name="set-6",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
        )
        NatRuleSetMixin.model.objects.bulk_create(cls.rule_sets)


class NatRuleSetRuleMixin(NatRuleSetMixin):
    model = NatRule

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.nat_rules = (
            NatRuleSetRuleMixin.model(
                name="rule-1",
                rule_set=cls.rule_sets[0],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
            NatRuleSetRuleMixin.model(
                name="rule-2",
                rule_set=cls.rule_sets[1],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
            NatRuleSetRuleMixin.model(
                name="rule-3",
                rule_set=cls.rule_sets[2],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatRuleSetRuleMixin.model.objects.bulk_create(cls.nat_rules)


class PolicerMixin(TenantMixin):
    model = Policer

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policers = (
            PolicerMixin.model(
                name="policer-1",
                loss_priority=LossPriorityChoices.HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
                tenant=cls.tenants[0],
            ),
            PolicerMixin.model(
                name="policer-2",
                loss_priority=LossPriorityChoices.LOW,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
                tenant=cls.tenants[1],
            ),
            PolicerMixin.model(
                name="policer-3",
                loss_priority=LossPriorityChoices.MEDIUM_HIGH,
                forwarding_class=ForwardingClassChoices.ASSURED_FORWARDING,
                logical_interface_policer=True,
                physical_interface_policer=False,
                tenant=cls.tenants[2],
            ),
        )
        PolicerMixin.model.objects.bulk_create(cls.policers)


class SecurityZoneMixin(Base):
    model = SecurityZone

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.zones = (
            SecurityZoneMixin.model(name="zone-1"),
            SecurityZoneMixin.model(name="zone-2"),
            SecurityZoneMixin.model(name="zone-3"),
        )
        SecurityZoneMixin.model.objects.bulk_create(cls.zones)


class SecurityZonePolicyMixin(SecurityZoneMixin, ApplicationSetMixin, AddressListMixin):
    model = SecurityZonePolicy

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.policies = (
            SecurityZonePolicyMixin.model(
                name="policy-1",
                index=1,
                source_zone=cls.zones[0],
                destination_zone=cls.zones[1],
                policy_actions=[
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
            SecurityZonePolicyMixin.model(
                name="policy-2",
                index=2,
                source_zone=cls.zones[1],
                destination_zone=cls.zones[2],
                policy_actions=[
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
            SecurityZonePolicyMixin.model(
                name="policy-3",
                index=3,
                source_zone=cls.zones[2],
                destination_zone=cls.zones[0],
                policy_actions=[
                    ActionChoices.PERMIT,
                    ActionChoices.COUNT,
                    ActionChoices.LOG,
                ],
            ),
        )
        SecurityZonePolicyMixin.model.objects.bulk_create(cls.policies)
