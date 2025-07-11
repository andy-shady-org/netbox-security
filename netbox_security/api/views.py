from rest_framework.routers import APIRootView
from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import Count

from .serializers import (
    AddressListSerializer,
    AddressListAssignmentSerializer,
    AddressSetSerializer,
    AddressSetAssignmentSerializer,
    AddressSerializer,
    AddressAssignmentSerializer,
    ApplicationItemSerializer,
    ApplicationSerializer,
    ApplicationAssignmentSerializer,
    ApplicationSetSerializer,
    ApplicationSetAssignmentSerializer,
    SecurityZoneSerializer,
    SecurityZoneAssignmentSerializer,
    SecurityZonePolicySerializer,
    NatPoolSerializer,
    NatPoolAssignmentSerializer,
    NatPoolMemberSerializer,
    NatRuleSetSerializer,
    NatRuleSetAssignmentSerializer,
    NatRuleSerializer,
    NatRuleAssignmentSerializer,
    PolicerSerializer,
    PolicerAssignmentSerializer,
    FirewallFilterSerializer,
    FirewallFilterAssignmentSerializer,
    FirewallFilterRuleSerializer,
    FirewallRuleFromSettingSerializer,
    FirewallRuleThenSettingSerializer,
)

from netbox_security.models import (
    AddressList,
    AddressListAssignment,
    AddressSet,
    AddressSetAssignment,
    Address,
    AddressAssignment,
    ApplicationItem,
    Application,
    ApplicationAssignment,
    ApplicationSet,
    ApplicationSetAssignment,
    SecurityZone,
    SecurityZoneAssignment,
    SecurityZonePolicy,
    NatPool,
    NatPoolAssignment,
    NatPoolMember,
    NatRuleSet,
    NatRuleSetAssignment,
    NatRule,
    NatRuleAssignment,
    Policer,
    PolicerAssignment,
    FirewallFilter,
    FirewallFilterAssignment,
    FirewallFilterRule,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
)

from netbox_security.filtersets import (
    AddressListFilterSet,
    AddressListAssignmentFilterSet,
    AddressSetFilterSet,
    AddressSetAssignmentFilterSet,
    AddressFilterSet,
    AddressAssignmentFilterSet,
    ApplicationItemFilterSet,
    ApplicationFilterSet,
    ApplicationAssignmentFilterSet,
    ApplicationSetFilterSet,
    ApplicationSetAssignmentFilterSet,
    SecurityZoneFilterSet,
    SecurityZoneAssignmentFilterSet,
    SecurityZonePolicyFilterSet,
    NatPoolFilterSet,
    NatPoolAssignmentFilterSet,
    NatPoolMemberFilterSet,
    NatRuleSetFilterSet,
    NatRuleSetAssignmentFilterSet,
    NatRuleFilterSet,
    NatRuleAssignmentFilterSet,
    PolicerFilterSet,
    PolicerAssignmentFilterSet,
    FirewallFilterFilterSet,
    FirewallFilterAssignmentFilterSet,
    FirewallFilterRuleFilterSet,
    FirewallFilterRuleFromSettingFilterSet,
    FirewallFilterRuleThenSettingFilterSet,
)


class NetBoxSecurityRootView(APIRootView):
    def get_view_name(self):
        return "NetBoxSecurity"


class AddressListViewSet(NetBoxModelViewSet):
    queryset = AddressList.objects.all()
    serializer_class = AddressListSerializer
    filterset_class = AddressListFilterSet


class AddressListAssignmentViewSet(NetBoxModelViewSet):
    queryset = AddressListAssignment.objects.all()
    serializer_class = AddressListAssignmentSerializer
    filterset_class = AddressListAssignmentFilterSet


class AddressSetViewSet(NetBoxModelViewSet):
    queryset = AddressSet.objects.prefetch_related("tenant", "tags")
    serializer_class = AddressSetSerializer
    filterset_class = AddressSetFilterSet


class AddressSetAssignmentViewSet(NetBoxModelViewSet):
    queryset = AddressSetAssignment.objects.all()
    serializer_class = AddressSetAssignmentSerializer
    filterset_class = AddressSetAssignmentFilterSet


class AddressViewSet(NetBoxModelViewSet):
    queryset = Address.objects.prefetch_related("tenant", "tags")
    serializer_class = AddressSerializer
    filterset_class = AddressFilterSet


class AddressAssignmentViewSet(NetBoxModelViewSet):
    queryset = AddressAssignment.objects.all()
    serializer_class = AddressAssignmentSerializer
    filterset_class = AddressAssignmentFilterSet


class ApplicationItemViewSet(NetBoxModelViewSet):
    queryset = ApplicationItem.objects.prefetch_related("tags")
    serializer_class = ApplicationItemSerializer
    filterset_class = ApplicationItemFilterSet


class ApplicationViewSet(NetBoxModelViewSet):
    queryset = Application.objects.prefetch_related("tenant", "tags")
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilterSet


class ApplicationAssignmentViewSet(NetBoxModelViewSet):
    queryset = ApplicationAssignment.objects.all()
    serializer_class = ApplicationAssignmentSerializer
    filterset_class = ApplicationAssignmentFilterSet


class ApplicationSetViewSet(NetBoxModelViewSet):
    queryset = ApplicationSet.objects.prefetch_related("tenant", "tags")
    serializer_class = ApplicationSetSerializer
    filterset_class = ApplicationSetFilterSet


class ApplicationSetAssignmentViewSet(NetBoxModelViewSet):
    queryset = ApplicationSetAssignment.objects.all()
    serializer_class = ApplicationSetAssignmentSerializer
    filterset_class = ApplicationSetAssignmentFilterSet


class SecurityZoneViewSet(NetBoxModelViewSet):
    queryset = SecurityZone.objects.prefetch_related("tenant", "tags").annotate(
        source_policy_count=Count("source_zone_policies"),
        destination_policy_count=Count("destination_zone_policies"),
    )
    serializer_class = SecurityZoneSerializer
    filterset_class = SecurityZoneFilterSet


class SecurityZoneAssignmentViewSet(NetBoxModelViewSet):
    queryset = SecurityZoneAssignment.objects.all()
    serializer_class = SecurityZoneAssignmentSerializer
    filterset_class = SecurityZoneAssignmentFilterSet


class SecurityZonePolicyViewSet(NetBoxModelViewSet):
    queryset = SecurityZonePolicy.objects.prefetch_related(
        "source_zone",
        "destination_zone",
        "source_address",
        "destination_address",
        "tags",
    )
    serializer_class = SecurityZonePolicySerializer
    filterset_class = SecurityZonePolicyFilterSet


class NatPoolViewSet(NetBoxModelViewSet):
    queryset = NatPool.objects.prefetch_related("tags").annotate(
        member_count=Count("natpoolmember_pools")
    )
    serializer_class = NatPoolSerializer
    filterset_class = NatPoolFilterSet


class NatPoolAssignmentViewSet(NetBoxModelViewSet):
    queryset = NatPoolAssignment.objects.all()
    serializer_class = NatPoolAssignmentSerializer
    filterset_class = NatPoolAssignmentFilterSet


class NatPoolMemberViewSet(NetBoxModelViewSet):
    queryset = NatPoolMember.objects.prefetch_related(
        "pool", "address", "prefix", "address_range", "tags"
    )
    serializer_class = NatPoolMemberSerializer
    filterset_class = NatPoolMemberFilterSet


class NatRuleSetViewSet(NetBoxModelViewSet):
    queryset = NatRuleSet.objects.prefetch_related("tags").annotate(
        rule_count=Count("natrule_rules")
    )
    serializer_class = NatRuleSetSerializer
    filterset_class = NatRuleSetFilterSet


class NatRuleSetAssignmentViewSet(NetBoxModelViewSet):
    queryset = NatRuleSetAssignment.objects.all()
    serializer_class = NatRuleSetAssignmentSerializer
    filterset_class = NatRuleSetAssignmentFilterSet


class NatRuleViewSet(NetBoxModelViewSet):
    queryset = NatRule.objects.prefetch_related(
        "source_addresses",
        "destination_addresses",
        "source_prefixes",
        "destination_prefixes",
        "source_ranges",
        "destination_ranges",
        "source_pool",
        "destination_pool",
        "pool",
        "tags",
    )
    serializer_class = NatRuleSerializer
    filterset_class = NatRuleFilterSet


class NatRuleAssignmentViewSet(NetBoxModelViewSet):
    queryset = NatRuleAssignment.objects.all()
    serializer_class = NatRuleAssignmentSerializer
    filterset_class = NatRuleAssignmentFilterSet


class PolicerViewSet(NetBoxModelViewSet):
    queryset = Policer.objects.all()
    serializer_class = PolicerSerializer
    filterset_class = PolicerFilterSet


class PolicerAssignmentViewSet(NetBoxModelViewSet):
    queryset = PolicerAssignment.objects.all()
    serializer_class = PolicerAssignmentSerializer
    filterset_class = PolicerAssignmentFilterSet


class FirewallFilterViewSet(NetBoxModelViewSet):
    queryset = FirewallFilter.objects.prefetch_related("tenant", "tags").annotate(
        rule_count=Count("firewallfilterrule_rules")
    )
    serializer_class = FirewallFilterSerializer
    filterset_class = FirewallFilterFilterSet


class FirewallFilterAssignmentViewSet(NetBoxModelViewSet):
    queryset = FirewallFilterAssignment.objects.all()
    serializer_class = FirewallFilterAssignmentSerializer
    filterset_class = FirewallFilterAssignmentFilterSet


class FirewallFilterRuleViewSet(NetBoxModelViewSet):
    queryset = FirewallFilterRule.objects.prefetch_related("tags")
    serializer_class = FirewallFilterRuleSerializer
    filterset_class = FirewallFilterRuleFilterSet


class FirewallRuleFromSettingViewSet(NetBoxModelViewSet):
    queryset = FirewallRuleFromSetting.objects.all()
    serializer_class = FirewallRuleFromSettingSerializer
    filterset_class = FirewallFilterRuleFromSettingFilterSet


class FirewallRuleThenSettingViewSet(NetBoxModelViewSet):
    queryset = FirewallRuleThenSetting.objects.all()
    serializer_class = FirewallRuleThenSettingSerializer
    filterset_class = FirewallFilterRuleThenSettingFilterSet
