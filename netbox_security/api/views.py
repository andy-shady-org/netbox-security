from rest_framework.routers import APIRootView
from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import Count

from .serializers import (
    AddressSerializer, AddressAssignmentSerializer,
    SecurityZoneSerializer, SecurityZoneAssignmentSerializer,
    SecurityZonePolicySerializer,
    NatPoolSerializer, NatPoolAssignmentSerializer,
    NatPoolMemberSerializer,
    NatRuleSetSerializer, NatRuleSetAssignmentSerializer,
    NatRuleSerializer, NatRuleAssignmentSerializer,
    FirewallFilterSerializer, FirewallFilterAssignmentSerializer,
    FirewallFilterRuleSerializer, FirewallRuleSettingSerializer,
)

from netbox_security.models import (
    Address, AddressAssignment,
    SecurityZone, SecurityZoneAssignment,
    SecurityZonePolicy,
    NatPool, NatPoolAssignment,
    NatPoolMember,
    NatRuleSet, NatRuleSetAssignment,
    NatRule, NatRuleAssignment,
    FirewallFilter, FirewallFilterAssignment,
    FirewallFilterRule, FirewallRuleSetting,
)

from netbox_security.filtersets import (
    AddressFilterSet, AddressAssignmentFilterSet,
    SecurityZoneFilterSet, SecurityZoneAssignmentFilterSet,
    SecurityZonePolicyFilterSet,
    NatPoolFilterSet, NatPoolAssignmentFilterSet,
    NatPoolMemberFilterSet,
    NatRuleSetFilterSet, NatRuleSetAssignmentFilterSet,
    NatRuleFilterSet, NatRuleAssignmentFilterSet,
    FirewallFilterFilterSet, FirewallFilterAssignmentFilterSet,
    FirewallFilterRuleFilterSet, FirewallFilterRuleSettingFilterSet,
)


class NetBoxSecurityRootView(APIRootView):
    def get_view_name(self):
        return "NetBoxSecurity"


class AddressViewSet(NetBoxModelViewSet):
    queryset = Address.objects.prefetch_related('tenant', 'tags')
    serializer_class = AddressSerializer
    filterset_class = AddressFilterSet


class AddressAssignmentViewSet(NetBoxModelViewSet):
    queryset = AddressAssignment.objects.all()
    serializer_class = AddressAssignmentSerializer
    filterset_class = AddressAssignmentFilterSet


class SecurityZoneViewSet(NetBoxModelViewSet):
    queryset = SecurityZone.objects.prefetch_related('tenant', 'tags')
    serializer_class = SecurityZoneSerializer
    filterset_class = SecurityZoneFilterSet


class SecurityZoneAssignmentViewSet(NetBoxModelViewSet):
    queryset = SecurityZoneAssignment.objects.all()
    serializer_class = SecurityZoneAssignmentSerializer
    filterset_class = SecurityZoneAssignmentFilterSet


class SecurityZonePolicyViewSet(NetBoxModelViewSet):
    queryset = SecurityZonePolicy.objects.prefetch_related(
        'source_zone', 'destination_zone', 'source_address',
        'destination_address', 'tenant', 'tags'
    )
    serializer_class = SecurityZonePolicySerializer
    filterset_class = SecurityZonePolicyFilterSet


class NatPoolViewSet(NetBoxModelViewSet):
    queryset = NatPool.objects.prefetch_related('tags').annotate(
        member_count=Count('natpoolmember_pools')
    )
    serializer_class = NatPoolSerializer
    filterset_class = NatPoolFilterSet


class NatPoolAssignmentViewSet(NetBoxModelViewSet):
    queryset = NatPoolAssignment.objects.all()
    serializer_class = NatPoolAssignmentSerializer
    filterset_class = NatPoolAssignmentFilterSet


class NatPoolMemberViewSet(NetBoxModelViewSet):
    queryset = NatPoolMember.objects.prefetch_related(
        'pool', 'address', 'prefix', 'address_range', 'tags'
    )
    serializer_class = NatPoolMemberSerializer
    filterset_class = NatPoolMemberFilterSet


class NatRuleSetViewSet(NetBoxModelViewSet):
    queryset = NatRuleSet.objects.prefetch_related('tags').annotate(
        rule_count=Count('natrule_rules')
    )
    serializer_class = NatRuleSetSerializer
    filterset_class = NatRuleSetFilterSet


class NatRuleSetAssignmentViewSet(NetBoxModelViewSet):
    queryset = NatRuleSetAssignment.objects.all()
    serializer_class = NatRuleSetAssignmentSerializer
    filterset_class = NatRuleSetAssignmentFilterSet


class NatRuleViewSet(NetBoxModelViewSet):
    queryset = NatRule.objects.prefetch_related(
        'source_addresses', 'destination_addresses', 'source_prefixes', 'destination_prefixes', 'source_ranges',
        'destination_ranges', 'source_pool', 'destination_pool', 'pool', 'tags'
    )
    serializer_class = NatRuleSerializer
    filterset_class = NatRuleFilterSet


class NatRuleAssignmentViewSet(NetBoxModelViewSet):
    queryset = NatRuleAssignment.objects.all()
    serializer_class = NatRuleAssignmentSerializer
    filterset_class = NatRuleAssignmentFilterSet


class FirewallFilterViewSet(NetBoxModelViewSet):
    queryset = FirewallFilter.objects.prefetch_related('tenant', 'tags')
    serializer_class = FirewallFilterSerializer
    filterset_class = FirewallFilterFilterSet


class FirewallFilterAssignmentViewSet(NetBoxModelViewSet):
    queryset = FirewallFilterAssignment.objects.all()
    serializer_class = FirewallFilterAssignmentSerializer
    filterset_class = FirewallFilterAssignmentFilterSet


class FirewallFilterRuleViewSet(NetBoxModelViewSet):
    queryset = FirewallFilterRule.objects.prefetch_related('tags')
    serializer_class = FirewallFilterRuleSerializer
    filterset_class = FirewallFilterRuleFilterSet


class FirewallRuleSettingViewSet(NetBoxModelViewSet):
    queryset = FirewallRuleSetting.objects.all()
    serializer_class = FirewallRuleSettingSerializer
    filterset_class = FirewallFilterRuleSettingFilterSet
