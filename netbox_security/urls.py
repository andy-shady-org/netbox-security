from django.urls import include, path
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls
from .models import (
    Address,
    SecurityZone,
    SecurityZonePolicy,
    NatPool,
    NatPoolMember,
    NatRuleSet,
    NatRule,
    FirewallFilter,
)

from . import views

urlpatterns = [
    # Addresses
    path('address/', views.AddressView.as_view(), name='address_list'),
    path('address/add/', views.AddressEditView.as_view(), name='address_add'),
    path('address/import/', views.AddressBulkImportView.as_view(), name='address_import'),
    path('address/edit/', views.AddressBulkEditView.as_view(), name='address_bulk_edit'),
    path('address/delete/', views.AddressBulkDeleteView.as_view(), name='address_bulk_delete'),
    path('address/<int:pk>/', views.AddressView.as_view(), name='address'),
    path('address/<int:pk>/edit/', views.AddressEditView.as_view(), name='address_edit'),
    path('address/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
    path('address/<int:pk>/contacts/', views.AddressContactsView.as_view(), name='address_contacts'),
    path('address/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='address_changelog', kwargs={'model': Address}),
    # Security Zones
    path('security-zone/', views.SecurityZoneListView.as_view(), name='securityzone_list'),
    path('security-zone/add/', views.SecurityZoneEditView.as_view(), name='securityzone_add'),
    path('security-zone/import/', views.SecurityZoneBulkImportView.as_view(), name='securityzone_import'),
    path('security-zone/edit/', views.SecurityZoneBulkEditView.as_view(), name='securityzone_bulk_edit'),
    path('security-zone/delete/', views.SecurityZoneBulkDeleteView.as_view(), name='securityzone_bulk_delete'),
    path('security-zone/<int:pk>/', views.SecurityZoneView.as_view(), name='securityzone'),
    path('security-zone/<int:pk>/edit/', views.SecurityZoneEditView.as_view(), name='securityzone_edit'),
    path('security-zone/<int:pk>/delete/', views.SecurityZoneDeleteView.as_view(), name='securityzone_delete'),
    path('security-zone/<int:pk>/contacts/', views.SecurityZoneContactsView.as_view(), name='securityzone_contacts'),
    path('security-zone/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='securityzone_changelog', kwargs={'model': SecurityZone}),
    # Security Zones
    path('security-zone-policy/', views.SecurityZonePolicyListView.as_view(), name='securityzonepolicy_list'),
    path('security-zone-policy/add/', views.SecurityZonePolicyEditView.as_view(), name='securityzonepolicy_add'),
    path('security-zone-policy/import/', views.SecurityZonePolicyBulkImportView.as_view(), name='securityzonepolicy_import'),
    path('security-zone-policy/edit/', views.SecurityZonePolicyBulkEditView.as_view(), name='securityzonepolicy_bulk_edit'),
    path('security-zone-policy/delete/', views.SecurityZonePolicyBulkDeleteView.as_view(), name='securityzonepolicy_bulk_delete'),
    path('security-zone-policy/<int:pk>/', views.SecurityZonePolicyView.as_view(), name='securityzonepolicy'),
    path('security-zone-policy/<int:pk>/edit/', views.SecurityZonePolicyEditView.as_view(), name='securityzonepolicy_edit'),
    path('security-zone-policy/<int:pk>/delete/', views.SecurityZonePolicyDeleteView.as_view(), name='securityzonepolicy_delete'),
    path('security-zone-policy/<int:pk>/contacts/', views.SecurityZonePolicyContactsView.as_view(), name='securityzonepolicy_contacts'),
    path('security-zone-policy/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='securityzonepolicy_changelog', kwargs={'model': SecurityZonePolicy}),
    # Nat Pool
    path('nat-pool/', views.NatPoolListView.as_view(), name='natpool_list'),
    path('nat-pool/add/', views.NatPoolEditView.as_view(), name='natpool_add'),
    path('nat-pool/import/', views.NatPoolBulkImportView.as_view(), name='natpool_import'),
    path('nat-pool/edit/', views.NatPoolBulkEditView.as_view(), name='natpool_bulk_edit'),
    path('nat-pool/delete/', views.NatPoolBulkDeleteView.as_view(), name='natpool_bulk_delete'),
    path('nat-pool/<int:pk>/', views.NatPoolView.as_view(), name='natpool'),
    path('nat-pool/<int:pk>/edit/', views.NatPoolEditView.as_view(), name='natpool_edit'),
    path('nat-pool/<int:pk>/members/', views.NatPoolNatPoolMembersView.as_view(), name='natpool_members'),
    path('nat-pool/<int:pk>/delete/', views.NatPoolDeleteView.as_view(), name='natpool_delete'),
    path('nat-pool/<int:pk>/contacts/', views.NatPoolContactsView.as_view(), name='natpool_contacts'),
    path('nat-pool/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='natpool_changelog', kwargs={'model': NatPool}),
    # Nat Pool Members
    path('pool-member/', views.NatPoolMemberListView.as_view(), name='natpoolmember_list'),
    path('pool-member/add/', views.NatPoolMemberEditView.as_view(), name='natpoolmember_add'),
    path('pool-member/import/', views.NatPoolMemberBulkImportView.as_view(), name='natpoolmember_import'),
    path('pool-member/delete/', views.NatPoolMemberBulkDeleteView.as_view(), name='natpoolmember_bulk_delete'),
    path('pool-member/<int:pk>/', views.NatPoolMemberView.as_view(), name='natpoolmember'),
    path('pool-member/<int:pk>/edit/', views.NatPoolMemberEditView.as_view(), name='natpoolmember_edit'),
    path('pool-member/<int:pk>/delete/', views.NatPoolMemberDeleteView.as_view(), name='natpoolmember_delete'),
    path('pool-member/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='natpoolmember_changelog', kwargs={'model': NatPoolMember}),
    # Nat Rule Sets
    path('rule-set/', views.NatRuleSetListView.as_view(), name='natruleset_list'),
    path('rule-set/add/', views.NatRuleSetEditView.as_view(), name='natruleset_add'),
    path('rule-set/import/', views.NatRuleSetBulkImportView.as_view(), name='natruleset_import'),
    path('rule-set/edit/', views.NatRuleSetBulkEditView.as_view(), name='natruleset_bulk_edit'),
    path('rule-set/delete/', views.NatRuleSetBulkDeleteView.as_view(), name='natruleset_bulk_delete'),
    path('rule-set/<int:pk>/', views.NatRuleSetView.as_view(), name='natruleset'),
    path('rule-set/<int:pk>/edit/', views.NatRuleSetEditView.as_view(), name='natruleset_edit'),
    path('rule-set/<int:pk>/rules/', views.NatRuleSetRulesView.as_view(), name='natruleset_rules'),
    path('rule-set/<int:pk>/delete/', views.NatRuleSetDeleteView.as_view(), name='natruleset_delete'),
    path('rule-set/<int:pk>/contacts/', views.NatRuleSetContactsView.as_view(), name='natruleset_contacts'),
    path('rule-set/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='natruleset_changelog', kwargs={'model': NatRuleSet}),
    # Nat Rules
    path('nat-rule/', views.NatRuleListView.as_view(), name='natrule_list'),
    path('nat-rule/add/', views.NatRuleEditView.as_view(), name='natrule_add'),
    path('nat-rule/import/', views.NatRuleBulkImportView.as_view(), name='natrule_import'),
    path('nat-rule/delete/', views.NatRuleBulkDeleteView.as_view(), name='natrule_bulk_delete'),
    path('nat-rule/<int:pk>/', views.NatRuleView.as_view(), name='natrule'),
    path('nat-rule/<int:pk>/edit/', views.NatRuleEditView.as_view(), name='natrule_edit'),
    path('nat-rule/<int:pk>/delete/', views.NatRuleDeleteView.as_view(), name='natrule_delete'),
    path('nat-rule/<int:pk>/contacts/', views.NatRuleContactsView.as_view(), name='natrule_contacts'),
    path('nat-rule/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='natrule_changelog', kwargs={'model': NatRule}),
    # Firewall Filters
    path('firewall-filter/', views.FirewallFilterView.as_view(), name='firewallfilter_list'),
    path('firewall-filter/add/', views.FirewallFilterEditView.as_view(), name='firewallfilter_add'),
    path('firewall-filter/import/', views.FirewallFilterBulkImportView.as_view(), name='firewallfilter_import'),
    path('firewall-filter/edit/', views.FirewallFilterBulkEditView.as_view(), name='firewallfilter_bulk_edit'),
    path('firewall-filter/delete/', views.FirewallFilterBulkDeleteView.as_view(), name='firewallfilter_bulk_delete'),
    path('firewall-filter/<int:pk>/', views.FirewallFilterView.as_view(), name='firewallfilter'),
    path('firewall-filter/<int:pk>/edit/', views.FirewallFilterEditView.as_view(), name='firewallfilter_edit'),
    path('firewall-filter/<int:pk>/delete/', views.FirewallFilterDeleteView.as_view(), name='firewallfilter_delete'),
    path('firewall-filter/<int:pk>/contacts/', views.FirewallFilterContactsView.as_view(), name='firewallfilter_contacts'),
    path('firewall-filter/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='firewallfilter_changelog', kwargs={'model': FirewallFilter}),
    # Address Assignments
    path('address-assignments/add/', views.AddressAssignmentEditView.as_view(), name='addressassignment_add'),
    path('address-assignments/<int:pk>/', include(get_model_urls('netbox_security', 'addressassignment'))),
    # Security Zone Assignments
    path('security-zone-assignments/add/', views.SecurityZoneAssignmentEditView.as_view(), name='securityzoneassignment_add'),
    path('security-zone-assignments/<int:pk>/', include(get_model_urls('netbox_security', 'securityzoneassignment'))),
    # NAT Pool Assignments
    path('nat-pool-assignments/add/', views.NatPoolAssignmentEditView.as_view(), name='natpoolassignment_add'),
    path('nat-pool-assignments/<int:pk>/', include(get_model_urls('netbox_security', 'natpoolassignment'))),
    # NAT Rule Assignments
    path('nat-rule-assignments/add/', views.NatRuleAssignmentEditView.as_view(), name='natruleassignment_add'),
    path('nat-rule-assignments/<int:pk>/', include(get_model_urls('netbox_security', 'natruleassignment'))),
    # NAT Ruleset Assignments
    path('rule-set-assignments/add/', views.NatRuleSetAssignmentEditView.as_view(), name='natrulesetassignment_add'),
    path('rule-set-assignments/<int:pk>/', include(get_model_urls('netbox_security', 'natrulesetassignment'))),
    # Firewall Filter Assignments
    path('firewall-filter-assignments/add/', views.AddressAssignmentEditView.as_view(), name='addresslistassignment_add'),
    path('firewall-filter-assignments/<int:pk>/', include(get_model_urls('netbox_security', 'addresslistassignment'))),
]
