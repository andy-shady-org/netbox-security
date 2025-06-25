from django.urls import include, path
from utilities.urls import get_model_urls

# +
# Import views so the register_model_view is run. This is required for the
# URLs to be set up properly with get_model_urls().
# -
from .views import *  # noqa: F401

app_name = "netbox_security"

urlpatterns = [
    # Addresses
    path(
        "address/",
        include(get_model_urls("netbox_security", "address", detail=False)),
    ),
    path(
        "address/<int:pk>/",
        include(get_model_urls("netbox_security", "address")),
    ),
    # Address Sets
    path(
        "address-set/",
        include(get_model_urls("netbox_security", "addressset", detail=False)),
    ),
    path(
        "address-set/<int:pk>/",
        include(get_model_urls("netbox_security", "addressset")),
    ),
    # Address Lists
    path(
        "address-list/",
        include(get_model_urls("netbox_security", "addresslist", detail=False)),
    ),
    path(
        "address-list/<int:pk>/",
        include(get_model_urls("netbox_security", "addresslist")),
    ),
    # Application Items
    path(
        "application-item/",
        include(get_model_urls("netbox_security", "applicationitem", detail=False)),
    ),
    path(
        "application-item/<int:pk>/",
        include(get_model_urls("netbox_security", "applicationitem")),
    ),
    # Applications
    path(
        "application/",
        include(get_model_urls("netbox_security", "application", detail=False)),
    ),
    path(
        "application/<int:pk>/",
        include(get_model_urls("netbox_security", "application")),
    ),
    # Application Sets
    path(
        "application-set/",
        include(get_model_urls("netbox_security", "applicationset", detail=False)),
    ),
    path(
        "application-set/<int:pk>/",
        include(get_model_urls("netbox_security", "applicationset")),
    ),
    # Security Zones
    path(
        "security-zone/",
        include(get_model_urls("netbox_security", "securityzone", detail=False)),
    ),
    path(
        "security-zone/<int:pk>/",
        include(get_model_urls("netbox_security", "securityzone")),
    ),
    # Security Zone Policies
    path(
        "security-zone-policy/",
        include(get_model_urls("netbox_security", "securityzonepolicy", detail=False)),
    ),
    path(
        "security-zone-policy/<int:pk>/",
        include(get_model_urls("netbox_security", "securityzonepolicy")),
    ),
    # Nat Pools
    path(
        "nat-pool/",
        include(get_model_urls("netbox_security", "natpool", detail=False)),
    ),
    path(
        "nat-pool/<int:pk>/",
        include(get_model_urls("netbox_security", "natpool")),
    ),
    # Nat Pool Members
    path(
        "nat-pool-member/",
        include(get_model_urls("netbox_security", "natpoolmember", detail=False)),
    ),
    path(
        "nat-pool-member/<int:pk>/",
        include(get_model_urls("netbox_security", "natpoolmember")),
    ),
    # Nat Rule Sets
    path(
        "nat-rule-set/",
        include(get_model_urls("netbox_security", "natruleset", detail=False)),
    ),
    path(
        "nat-rule-set/<int:pk>/",
        include(get_model_urls("netbox_security", "natruleset")),
    ),
    # Nat Rules
    path(
        "nat-rule/",
        include(get_model_urls("netbox_security", "natrule", detail=False)),
    ),
    path(
        "nat-rule/<int:pk>/",
        include(get_model_urls("netbox_security", "natrule")),
    ),
    # Firewall Filters
    path(
        "firewall-filter/",
        include(get_model_urls("netbox_security", "firewallfilter", detail=False)),
    ),
    path(
        "firewall-filter/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallfilter")),
    ),
    # Policers
    path(
        "policer/",
        include(get_model_urls("netbox_security", "policer", detail=False)),
    ),
    path(
        "policer/<int:pk>/",
        include(get_model_urls("netbox_security", "policer")),
    ),
    # Firewall Filter Rules
    path(
        "firewall-filter-rule/",
        include(get_model_urls("netbox_security", "firewallfilterrule", detail=False)),
    ),
    path(
        "firewall-filter-rule/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallfilterrule")),
    ),
    # Firewall Filter Rule From Settings
    path(
        "firewall-filter-rule-from-setting/",
        include(
            get_model_urls("netbox_security", "firewallrulefromsetting", detail=False)
        ),
    ),
    path(
        "firewall-filter-rule-from-setting/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallrulefromsetting")),
    ),
    # Firewall Filter Rule Then Settings
    path(
        "firewall-filter-rule-then-setting/",
        include(
            get_model_urls("netbox_security", "firewallrulethensetting", detail=False)
        ),
    ),
    path(
        "firewall-filter-rule-then-setting/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallrulethensetting")),
    ),
    # Address List Assignments
    path(
        "address-list-assignments/",
        include(
            get_model_urls("netbox_security", "addresslistassignment", detail=False)
        ),
    ),
    path(
        "address-list-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "addresslistassignment")),
    ),
    # Address Set Assignments
    path(
        "address-set-assignments/",
        include(
            get_model_urls("netbox_security", "addresssetassignment", detail=False)
        ),
    ),
    path(
        "address-set-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "addresssetassignment")),
    ),
    # Address Assignments
    path(
        "address-assignments/",
        include(get_model_urls("netbox_security", "addressassignment", detail=False)),
    ),
    path(
        "address-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "addressassignment")),
    ),
    # Application Assignments
    path(
        "application-assignments/",
        include(
            get_model_urls("netbox_security", "applicationassignment", detail=False)
        ),
    ),
    path(
        "application-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "applicationassignment")),
    ),
    # Application Set Assignments
    path(
        "applicationset-assignments/",
        include(
            get_model_urls("netbox_security", "applicationsetassignment", detail=False)
        ),
    ),
    path(
        "applicationset-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "applicationsetassignment")),
    ),
    # Security Zone Assignments
    path(
        "security-zone-assignments/",
        include(
            get_model_urls("netbox_security", "securityzoneassignment", detail=False)
        ),
    ),
    path(
        "security-zone-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "securityzoneassignment")),
    ),
    # NAT Pool Assignments
    path(
        "nat-pool-assignments/",
        include(get_model_urls("netbox_security", "natpoolassignment", detail=False)),
    ),
    path(
        "nat-pool-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "natpoolassignment")),
    ),
    # NAT Rule Assignments
    path(
        "nat-rule-assignments/",
        include(get_model_urls("netbox_security", "natruleassignment", detail=False)),
    ),
    path(
        "nat-rule-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "natruleassignment")),
    ),
    # NAT Ruleset Assignments
    path(
        "nat-rule-set-assignments/",
        include(
            get_model_urls("netbox_security", "natrulesetassignment", detail=False)
        ),
    ),
    path(
        "nat-rule-set-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "natrulesetassignment")),
    ),
    # Firewall Filter Assignments
    path(
        "firewall-filter-assignments/",
        include(
            get_model_urls("netbox_security", "firewallfilterassignment", detail=False)
        ),
    ),
    path(
        "firewall-filter-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "firewallfilterassignment")),
    ),
    # Policer Assignments
    path(
        "policer-assignments/",
        include(get_model_urls("netbox_security", "policerassignment", detail=False)),
    ),
    path(
        "policer-assignments/<int:pk>/",
        include(get_model_urls("netbox_security", "policerassignment")),
    ),
]
