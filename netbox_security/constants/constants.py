"""
Constants for filters
"""

from django.db.models import Q

ADDRESS_LIST_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_security", model="address")
    | Q(app_label="netbox_security", model="addressset")
)

RULESET_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualdevicecontext")
    | Q(app_label="virtualization", model="virtualmachine")
)

POOL_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualdevicecontext")
    | Q(app_label="virtualization", model="virtualmachine")
)

RULE_ASSIGNMENT_MODELS = Q(Q(app_label="dcim", model="interface"))

ZONE_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualdevicecontext")
    | Q(app_label="dcim", model="interface")
)

ADDRESS_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualdevicecontext")
    | Q(app_label="netbox_security", model="securityzone")
)

FILTER_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualdevicecontext")
)

FILTER_SETTING_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_security", model="firewallfilterrule")
)

POLICER_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualdevicecontext")
)

APPLICATION_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device")
    | Q(app_label="dcim", model="virtualdevicecontext")
)
