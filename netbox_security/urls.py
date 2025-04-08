from django.urls import include, path
from utilities.urls import get_model_urls

from . import views

app_name = "netbox_security"

urlpatterns = [
    # Addresses
    path("address/", views.AddressListView.as_view(), name="address_list"),
    path("address/add", views.AddressEditView.as_view(), name="address_add"),
    path(
        "address/delete",
        views.AddressBulkDeleteView.as_view(),
        name="address_bulk_delete",
    ),
    path("address/edit", views.AddressBulkEditView.as_view(), name="address_bulk_edit"),
    path(
        "address/import", views.AddressBulkImportView.as_view(), name="address_import"
    ),
    path("address/<int:pk>/", views.AddressView.as_view(), name="address"),
    path(
        "address/<int:pk>/edit/", views.AddressEditView.as_view(), name="address_edit"
    ),
    path(
        "address/<int:pk>/delete/",
        views.AddressDeleteView.as_view(),
        name="address_delete",
    ),
    path(
        "address/<int:pk>/",
        include(get_model_urls("netbox_security", "address")),
    ),
    # Address Sets
    path("address-set/", views.AddressSetListView.as_view(), name="addressset_list"),
    path("address-set/add", views.AddressSetEditView.as_view(), name="addressset_add"),
    path(
        "address-set/delete",
        views.AddressSetBulkDeleteView.as_view(),
        name="addressset_bulk_delete",
    ),
    path(
        "address-set/edit",
        views.AddressSetBulkEditView.as_view(),
        name="addressset_bulk_edit",
    ),
    path(
        "address-set/import",
        views.AddressSetBulkImportView.as_view(),
        name="addressset_import",
    ),
    path("address-set/<int:pk>/", views.AddressSetView.as_view(), name="addressset"),
    path(
        "address-set/<int:pk>/edit/",
        views.AddressSetEditView.as_view(),
        name="addressset_edit",
    ),
    path(
        "address-set/<int:pk>/delete/",
        views.AddressSetDeleteView.as_view(),
        name="addressset_delete",
    ),
    path(
        "address-set/<int:pk>/",
        include(get_model_urls("netbox_security", "addressset")),
    ),
    # Address Lists
    path(
        "address-list/",
        include(get_model_urls("netbox_security", "addresslist")),
    ),
    path(
        "address-list/<int:pk>/",
        include(get_model_urls("netbox_security", "addresslist")),
    ),
    # Security Zones
    path(
        "security-zone/", views.SecurityZoneListView.as_view(), name="securityzone_list"
    ),
    path(
        "security-zone/add",
        views.SecurityZoneEditView.as_view(),
        name="securityzone_add",
    ),
    path(
        "security-zone/delete",
        views.SecurityZoneBulkDeleteView.as_view(),
        name="securityzone_bulk_delete",
    ),
    path(
        "security-zone/edit",
        views.SecurityZoneBulkEditView.as_view(),
        name="securityzone_bulk_edit",
    ),
    path(
        "security-zone/import",
        views.SecurityZoneBulkImportView.as_view(),
        name="securityzone_import",
    ),
    path(
        "security-zone/<int:pk>/", views.SecurityZoneView.as_view(), name="securityzone"
    ),
    path(
        "security-zone/<int:pk>/edit/",
        views.SecurityZoneEditView.as_view(),
        name="securityzone_edit",
    ),
    path(
        "security-zone/<int:pk>/delete/",
        views.SecurityZoneDeleteView.as_view(),
        name="securityzone_delete",
    ),
    path(
        "security-zone/<int:pk>/",
        include(get_model_urls("netbox_security", "securityzone")),
    ),
    # Security Zone Policies
    path(
        "security-zone-policy/",
        views.SecurityZonePolicyListView.as_view(),
        name="securityzonepolicy_list",
    ),
    path(
        "security-zone-policy/add",
        views.SecurityZonePolicyEditView.as_view(),
        name="securityzonepolicy_add",
    ),
    path(
        "security-zone-policy/delete",
        views.SecurityZonePolicyBulkDeleteView.as_view(),
        name="securityzonepolicy_bulk_delete",
    ),
    path(
        "security-zone-policy/edit",
        views.SecurityZonePolicyBulkEditView.as_view(),
        name="securityzonepolicy_bulk_edit",
    ),
    path(
        "security-zone-policy/import",
        views.SecurityZonePolicyBulkImportView.as_view(),
        name="securityzonepolicy_import",
    ),
    path(
        "security-zone-policy/<int:pk>/",
        views.SecurityZonePolicyView.as_view(),
        name="securityzonepolicy",
    ),
    path(
        "security-zone-policy/<int:pk>/edit/",
        views.SecurityZonePolicyEditView.as_view(),
        name="securityzonepolicy_edit",
    ),
    path(
        "security-zone-policy/<int:pk>/delete/",
        views.SecurityZonePolicyDeleteView.as_view(),
        name="securityzonepolicy_delete",
    ),
    path(
        "security-zone-policy/<int:pk>/",
        include(get_model_urls("netbox_security", "securityzonepolicy")),
    ),
    # Nat Pools
    path("nat-pool/", views.NatPoolListView.as_view(), name="natpool_list"),
    path("nat-pool/add", views.NatPoolEditView.as_view(), name="natpool_add"),
    path(
        "nat-pool/delete",
        views.NatPoolBulkDeleteView.as_view(),
        name="natpool_bulk_delete",
    ),
    path(
        "nat-pool/edit", views.NatPoolBulkEditView.as_view(), name="natpool_bulk_edit"
    ),
    path(
        "nat-pool/import", views.NatPoolBulkImportView.as_view(), name="natpool_import"
    ),
    path("nat-pool/<int:pk>/", views.NatPoolView.as_view(), name="natpool"),
    path(
        "nat-pool/<int:pk>/edit/", views.NatPoolEditView.as_view(), name="natpool_edit"
    ),
    path(
        "nat-pool/<int:pk>/delete/",
        views.NatPoolDeleteView.as_view(),
        name="natpool_delete",
    ),
    path(
        "nat-pool/<int:pk>/",
        include(get_model_urls("netbox_security", "natpool")),
    ),
    # Nat Pool Members
    path(
        "nat-pool-member/",
        views.NatPoolMemberListView.as_view(),
        name="natpoolmember_list",
    ),
    path(
        "nat-pool-member/add",
        views.NatPoolMemberEditView.as_view(),
        name="natpoolmember_add",
    ),
    path(
        "nat-pool-member/delete",
        views.NatPoolMemberBulkDeleteView.as_view(),
        name="natpoolmember_bulk_delete",
    ),
    path(
        "nat-pool-member/edit",
        views.NatPoolMemberBulkEditView.as_view(),
        name="natpoolmember_bulk_edit",
    ),
    path(
        "nat-pool-member/import",
        views.NatPoolMemberBulkImportView.as_view(),
        name="natpoolmember_import",
    ),
    path(
        "nat-pool-member/<int:pk>/",
        views.NatPoolMemberView.as_view(),
        name="natpoolmember",
    ),
    path(
        "nat-pool-member/<int:pk>/edit/",
        views.NatPoolMemberEditView.as_view(),
        name="natpoolmember_edit",
    ),
    path(
        "nat-pool-member/<int:pk>/delete/",
        views.NatPoolMemberDeleteView.as_view(),
        name="natpoolmember_delete",
    ),
    path(
        "nat-pool-member/<int:pk>/",
        include(get_model_urls("netbox_security", "natpoolmember")),
    ),
    # Nat Rule Sets
    path("nat-rule-set/", views.NatRuleSetListView.as_view(), name="natruleset_list"),
    path("nat-rule-set/add", views.NatRuleSetEditView.as_view(), name="natruleset_add"),
    path(
        "nat-rule-set/delete",
        views.NatRuleSetBulkDeleteView.as_view(),
        name="natruleset_bulk_delete",
    ),
    path(
        "nat-rule-set/edit",
        views.NatRuleSetBulkEditView.as_view(),
        name="natruleset_bulk_edit",
    ),
    path(
        "nat-rule-set/import",
        views.NatRuleSetBulkImportView.as_view(),
        name="natruleset_import",
    ),
    path("nat-rule-set/<int:pk>/", views.NatRuleSetView.as_view(), name="natruleset"),
    path(
        "nat-rule-set/<int:pk>/edit/",
        views.NatRuleSetEditView.as_view(),
        name="natruleset_edit",
    ),
    path(
        "nat-rule-set/<int:pk>/delete/",
        views.NatRuleSetDeleteView.as_view(),
        name="natruleset_delete",
    ),
    path(
        "nat-rule-set/<int:pk>/",
        include(get_model_urls("netbox_security", "natruleset")),
    ),
    # Nat Rules
    path("nat-rule/", views.NatRuleListView.as_view(), name="natrule_list"),
    path("nat-rule/add", views.NatRuleEditView.as_view(), name="natrule_add"),
    path(
        "nat-rule/delete",
        views.NatRuleBulkDeleteView.as_view(),
        name="natrule_bulk_delete",
    ),
    path(
        "nat-rule/edit", views.NatRuleBulkEditView.as_view(), name="natrule_bulk_edit"
    ),
    path(
        "nat-rule/import", views.NatRuleBulkImportView.as_view(), name="natrule_import"
    ),
    path("nat-rule/<int:pk>/", views.NatRuleView.as_view(), name="natrule"),
    path(
        "nat-rule/<int:pk>/edit/", views.NatRuleEditView.as_view(), name="natrule_edit"
    ),
    path(
        "nat-rule/<int:pk>/delete/",
        views.NatRuleDeleteView.as_view(),
        name="natrule_delete",
    ),
    path(
        "nat-rule/<int:pk>/",
        include(get_model_urls("netbox_security", "natrule")),
    ),
    # Firewall Filters
    path(
        "firewall-filter/",
        views.FirewallFilterListView.as_view(),
        name="firewallfilter_list",
    ),
    path(
        "firewall-filter/add",
        views.FirewallFilterEditView.as_view(),
        name="firewallfilter_add",
    ),
    path(
        "firewall-filter/delete",
        views.FirewallFilterBulkDeleteView.as_view(),
        name="firewallfilter_bulk_delete",
    ),
    path(
        "firewall-filter/edit",
        views.FirewallFilterBulkEditView.as_view(),
        name="firewallfilter_bulk_edit",
    ),
    path(
        "firewall-filter/import",
        views.FirewallFilterBulkImportView.as_view(),
        name="firewallfilter_import",
    ),
    path(
        "firewall-filter/<int:pk>/",
        views.FirewallFilterView.as_view(),
        name="firewallfilter",
    ),
    path(
        "firewall-filter/<int:pk>/edit/",
        views.FirewallFilterEditView.as_view(),
        name="firewallfilter_edit",
    ),
    path(
        "firewall-filter/<int:pk>/delete/",
        views.FirewallFilterDeleteView.as_view(),
        name="firewallfilter_delete",
    ),
    path(
        "firewall-filter/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallfilter")),
    ),
    # Firewall Filter Rules
    path(
        "firewall-filter-rule/",
        views.FirewallFilterRuleListView.as_view(),
        name="firewallfilterrule_list",
    ),
    path(
        "firewall-filter-rule/add",
        views.FirewallFilterRuleEditView.as_view(),
        name="firewallfilterrule_add",
    ),
    path(
        "firewall-filter-rule/delete",
        views.FirewallFilterRuleBulkDeleteView.as_view(),
        name="firewallfilterrule_bulk_delete",
    ),
    path(
        "firewall-filter-rule/<int:pk>/",
        views.FirewallFilterRuleView.as_view(),
        name="firewallfilterrule",
    ),
    path(
        "firewall-filter-rule/<int:pk>/edit/",
        views.FirewallFilterRuleEditView.as_view(),
        name="firewallfilterrule_edit",
    ),
    path(
        "firewall-filter-rule/<int:pk>/delete/",
        views.FirewallFilterRuleDeleteView.as_view(),
        name="firewallfilterrule_delete",
    ),
    path(
        "firewall-filter-rule/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallfilterrule")),
    ),
    # Firewall Filter Rule From Settings
    path(
        "firewall-filter-rule-from-setting/",
        include(get_model_urls("netbox_security", "firewallrulefromsetting")),
    ),
    path(
        "firewall-filter-rule-from-setting/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallrulefromsetting")),
    ),
    # Firewall Filter Rule Then Settings
    path(
        "firewall-filter-rule-then-setting/",
        include(get_model_urls("netbox_security", "firewallrulethensetting")),
    ),
    path(
        "firewall-filter-rule-then-setting/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallrulethensetting")),
    ),
    # Address List Assignments
    path(
        "address-list-assignments/",
        include(get_model_urls("netbox_security", "addresslistassignment")),
    ),
    path(
        "address-list-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "addresslistassignment")),
    ),
    # Address Set Assignments
    path(
        "address-set-assignments/",
        include(get_model_urls("netbox_security", "addresssetassignment")),
    ),
    path(
        "address-set-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "addresssetassignment")),
    ),
    # Address Assignments
    path(
        "address-assignments/",
        include(get_model_urls("netbox_security", "addressassignment")),
    ),
    path(
        "address-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "addressassignment")),
    ),
    # Security Zone Assignments
    path(
        "security-zone-assignments/",
        include(get_model_urls("netbox_security", "securityzoneassignment")),
    ),
    path(
        "security-zone-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "securityzoneassignment")),
    ),
    # NAT Pool Assignments
    path(
        "nat-pool-assignments/",
        include(get_model_urls("netbox_security", "natpoolassignment")),
    ),
    path(
        "nat-pool-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "natpoolassignment")),
    ),
    # NAT Rule Assignments
    path(
        "nat-rule-assignments/",
        include(get_model_urls("netbox_security", "natruleassignment")),
    ),
    path(
        "nat-rule-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "natruleassignment")),
    ),
    # NAT Ruleset Assignments
    path(
        "nat-rule-set-assignments/",
        include(get_model_urls("netbox_security", "natrulesetassignment")),
    ),
    path(
        "nat-rule-set-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "natrulesetassignment")),
    ),
    # Firewall Filter Assignments
    path(
        "firewall-filter-assignments/",
        include(get_model_urls("netbox_security", "firewallfilterassignment")),
    ),
    path(
        "firewall-filter-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallfilterassignment")),
    ),
]
