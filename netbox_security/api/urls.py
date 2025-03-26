from netbox.api.routers import NetBoxRouter

from .views import (
    NetBoxSecurityRootView,
    AddressViewSet, AddressAssignmentViewSet,
    SecurityZoneViewSet, SecurityZoneAssignmentViewSet,
    SecurityZonePolicyViewSet,
    NatPoolViewSet, NatPoolAssignmentViewSet,
    NatPoolMemberViewSet,
    NatRuleSetViewSet, NatRuleSetAssignmentViewSet,
    NatRuleViewSet, NatRuleAssignmentViewSet,
    FirewallFilterViewSet, FirewallFilterAssignmentViewSet,
    FirewallFilterRuleViewSet, FirewallRuleSettingViewSet
)

app_name = 'netbox_security'

router = NetBoxRouter()
router.APIRootView = NetBoxSecurityRootView
router.register('address', AddressViewSet)
router.register('security-zone', SecurityZoneViewSet)
router.register('security-zone-policy', SecurityZonePolicyViewSet)
router.register('nat-pool', NatPoolViewSet)
router.register('pool-member', NatPoolMemberViewSet)
router.register('rule-set', NatRuleSetViewSet)
router.register('nat-rule', NatRuleViewSet)
router.register('firewall-filter', FirewallFilterViewSet)
router.register('firewall-filter-rule', FirewallFilterRuleViewSet)
router.register('firewall-filter-rule-setting', FirewallRuleSettingViewSet)
router.register('address-assignments', AddressAssignmentViewSet)
router.register('security-zone-assignments', SecurityZoneAssignmentViewSet)
router.register('nat-pool-assignments', NatPoolAssignmentViewSet)
router.register('rule-set-assignments', NatRuleSetAssignmentViewSet)
router.register('nat-rule-assignments', NatRuleAssignmentViewSet)
router.register('firewall-filter-assignments', FirewallFilterAssignmentViewSet)

urlpatterns = router.urls
