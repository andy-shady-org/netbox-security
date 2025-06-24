from netbox.api.routers import NetBoxRouter

from .views import (
    NetBoxSecurityRootView,
    AddressListViewSet,
    AddressListAssignmentViewSet,
    AddressSetViewSet,
    AddressSetAssignmentViewSet,
    AddressViewSet,
    AddressAssignmentViewSet,
    ApplicationItemViewSet,
    ApplicationViewSet,
    ApplicationSetViewSet,
    ApplicationAssignmentViewSet,
    ApplicationSetAssignmentViewSet,
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
    PolicerViewSet,
    FirewallFilterViewSet,
    FirewallFilterAssignmentViewSet,
    PolicerAssignmentViewSet,
    FirewallFilterRuleViewSet,
    FirewallRuleFromSettingViewSet,
    FirewallRuleThenSettingViewSet,
)

app_name = "netbox_security"

router = NetBoxRouter()
router.APIRootView = NetBoxSecurityRootView
router.register("addresses", AddressViewSet)
router.register("address-sets", AddressSetViewSet)
router.register("address-lists", AddressListViewSet)
router.register("application-items", ApplicationItemViewSet)
router.register("applications", ApplicationViewSet)
router.register("application-sets", ApplicationSetViewSet)
router.register("security-zones", SecurityZoneViewSet)
router.register("security-zone-policies", SecurityZonePolicyViewSet)
router.register("nat-pools", NatPoolViewSet)
router.register("nat-pool-members", NatPoolMemberViewSet)
router.register("nat-rule-sets", NatRuleSetViewSet)
router.register("nat-rules", NatRuleViewSet)
router.register("policers", PolicerViewSet)
router.register("firewall-filters", FirewallFilterViewSet)
router.register("firewall-filter-rules", FirewallFilterRuleViewSet)
router.register("firewall-filter-rule-from-settings", FirewallRuleFromSettingViewSet)
router.register("firewall-filter-rule-then-settings", FirewallRuleThenSettingViewSet)
router.register("address-assignments", AddressAssignmentViewSet)
router.register("address-set-assignments", AddressSetAssignmentViewSet)
router.register("address-list-assignments", AddressListAssignmentViewSet)
router.register("application-assignments", ApplicationAssignmentViewSet)
router.register("application-set-assignments", ApplicationSetAssignmentViewSet)
router.register("security-zone-assignments", SecurityZoneAssignmentViewSet)
router.register("nat-pool-assignments", NatPoolAssignmentViewSet)
router.register("nat-rule-set-assignments", NatRuleSetAssignmentViewSet)
router.register("nat-rule-assignments", NatRuleAssignmentViewSet)
router.register("firewall-filter-assignments", FirewallFilterAssignmentViewSet)
router.register("policer-assignments", PolicerAssignmentViewSet)

urlpatterns = router.urls
