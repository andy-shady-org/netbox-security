from rest_framework.routers import APIRootView
from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import Count

from .serializers import (
    AddressListSerializer, AddressListAssignmentSerializer,
    SecurityZoneSerializer, SecurityZoneAssignmentSerializer,
    NatPoolSerializer, NatPoolAssignmentSerializer,
    NatPoolMemberSerializer,
    NatRuleSetSerializer, NatRuleSetAssignmentSerializer,
    NatRuleSerializer, NatRuleAssignmentSerializer,
)

from netbox_security.models import (
    AddressList, AddressListAssignment,
    SecurityZone, SecurityZoneAssignment,
    NatPool, NatPoolAssignment,
    NatPoolMember,
    NatRuleSet, NatRuleSetAssignment,
    NatRule, NatRuleAssignment,
)

from netbox_security.filtersets import (
    AddressListFilterSet, AddressListAssignmentFilterSet,
    SecurityZoneFilterSet, SecurityZoneAssignmentFilterSet,
    NatPoolFilterSet, NatPoolAssignmentFilterSet,
    NatPoolMemberFilterSet,
    NatRuleSetFilterSet, NatRuleSetAssignmentFilterSet,
    NatRuleFilterSet, NatRuleAssignmentFilterSet,
)


class NetBoxSecurityRootView(APIRootView):
    def get_view_name(self):
        return "NetBoxSecurity"


class AddressListViewSet(NetBoxModelViewSet):
    queryset = AddressList.objects.prefetch_related('tenant', 'tags')
    serializer_class = AddressListSerializer
    filterset_class = AddressListFilterSet


class AddressListAssignmentViewSet(NetBoxModelViewSet):
    queryset = AddressListAssignment.objects.all()
    serializer_class = AddressListAssignmentSerializer
    filterset_class = AddressListAssignmentFilterSet


class SecurityZoneViewSet(NetBoxModelViewSet):
    queryset = SecurityZone.objects.prefetch_related('tenant', 'tags')
    serializer_class = SecurityZoneSerializer
    filterset_class = SecurityZoneFilterSet


class SecurityZoneAssignmentViewSet(NetBoxModelViewSet):
    queryset = SecurityZoneAssignment.objects.all()
    serializer_class = SecurityZoneAssignmentSerializer
    filterset_class = SecurityZoneAssignmentFilterSet


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
