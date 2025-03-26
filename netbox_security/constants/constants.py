"""
Constants for filters
"""
from django.db.models import Q

RULESET_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device"),
    Q(app_label="dcim", model="virtualdevicecontext"),
)

POOL_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device"),
    Q(app_label="dcim", model="virtualdevicecontext"),
)

RULE_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="interface")
)

ZONE_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device"),
    Q(app_label="dcim", model="virtualdevicecontext"),
    Q(app_label="dcim", model="interface"),
)

ADDRESSLIST_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device"),
    Q(app_label="dcim", model="virtualdevicecontext"),
    Q(app_label="netbox_security", model="SecurityZone"),
)

FILTER_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="device"),
    Q(app_label="dcim", model="virtualdevicecontext"),
)
