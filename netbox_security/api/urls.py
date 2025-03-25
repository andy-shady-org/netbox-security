from netbox.api.routers import NetBoxRouter

from .views import (
    NetBoxSecurityRootView,
    AddressListViewSet, AddressListAssignmentViewSet,
    SecurityZoneViewSet, SecurityZoneAssignmentViewSet,
    NatPoolViewSet, NatPoolAssignmentViewSet,
    NatPoolMemberViewSet,
    NatRuleSetViewSet, NatRuleSetAssignmentViewSet,
    NatRuleViewSet, NatRuleAssignmentViewSet,
)

app_name = 'netbox_security'

router = NetBoxRouter()
router.APIRootView = NetBoxSecurityRootView
router.register('address-list', AddressListViewSet)
router.register('security-zone', SecurityZoneViewSet)
router.register('nat-pool', NatPoolViewSet)
router.register('pool-member', NatPoolMemberViewSet)
router.register('rule-set', NatRuleSetViewSet)
router.register('nat-rule', NatRuleViewSet)
router.register('address-list-assignments', AddressListAssignmentViewSet)
router.register('security-zone-assignments', SecurityZoneAssignmentViewSet)
router.register('nat-pool-assignments', NatPoolAssignmentViewSet)
router.register('rule-set-assignments', NatRuleSetAssignmentViewSet)
router.register('nat-rule-assignments', NatRuleAssignmentViewSet)

urlpatterns = router.urls
