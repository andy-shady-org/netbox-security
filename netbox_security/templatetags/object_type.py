from django import template
from ipam.models import Prefix, IPAddress, IPRange
from netbox_security.models import CustomPrefix

register = template.Library()


@register.simple_tag(name="get_related_object_type")
def get_related_object_type(obj):
    if type(obj) is Prefix:
        obj_type = "Prefix"
    elif type(obj) is IPAddress:
        obj_type = "IP Address"
    elif type(obj) is IPRange:
        obj_type = "IP Range"
    elif type(obj) is CustomPrefix:
        obj_type = "Custom Prefix"
    else:
        return None
    return obj_type
