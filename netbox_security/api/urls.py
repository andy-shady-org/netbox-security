from netbox.api.routers import NetBoxRouter

from .views import (
    NetBoxSecurityRootView,
    AddressListViewSet,
    AddressListAssignmentViewSet,
    AddressSetViewSet,
    AddressSetAssignmentViewSet,
    AddressViewSet,
    AddressAssignmentViewSet,
    SecurityZoneViewSet,
    SecurityZoneAssignmentViewSet,
    SecurityZonePolicyViewSet,
    NatPoolViewSet,
    NatPoolAssignmentViewSet,
    NatPoolMemberViewSet,
    NatRuleSetViewSet,
    NatRuleSetAssignmentViewSet,
    NatRuleViewSet,
    NatRuleAssignmentViewSet,
    FirewallFilterViewSet,
    FirewallFilterAssignmentViewSet,
    FirewallFilterRuleViewSet,
    FirewallRuleFromSettingViewSet,
    FirewallRuleThenSettingViewSet,
)

app_name = "netbox_security"

router = NetBoxRouter()
router.APIRootView = NetBoxSecurityRootView
router.register("address", AddressViewSet)
router.register("address-set", AddressSetViewSet)
router.register("address-list", AddressListViewSet)
router.register("security-zone", SecurityZoneViewSet)
router.register("security-zone-policy", SecurityZonePolicyViewSet)
router.register("nat-pool", NatPoolViewSet)
router.register("nat-pool-member", NatPoolMemberViewSet)
router.register("nat-rule-set", NatRuleSetViewSet)
router.register("nat-rule", NatRuleViewSet)
router.register("firewall-filter", FirewallFilterViewSet)
router.register("firewall-filter-rule", FirewallFilterRuleViewSet)
router.register("firewall-filter-rule-from-setting", FirewallRuleFromSettingViewSet)
router.register("firewall-filter-rule-then-setting", FirewallRuleThenSettingViewSet)
router.register("address-assignments", AddressAssignmentViewSet)
router.register("address-set-assignments", AddressSetAssignmentViewSet)
router.register("address-list-assignments", AddressListAssignmentViewSet)
router.register("security-zone-assignments", SecurityZoneAssignmentViewSet)
router.register("nat-pool-assignments", NatPoolAssignmentViewSet)
router.register("nat-rule-set-assignments", NatRuleSetAssignmentViewSet)
router.register("nat-rule-assignments", NatRuleAssignmentViewSet)
router.register("firewall-filter-assignments", FirewallFilterAssignmentViewSet)

urlpatterns = router.urls
