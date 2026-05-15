from django.utils.translation import gettext_lazy as _

from ipam.models import IPAddress, IPRange, Prefix
from dcim.models import Device, VirtualDeviceContext
from virtualization.models import VirtualMachine
from netbox.views import generic
from utilities.views import register_model_view, ViewTab


@register_model_view(Device, name="security")
class DeviceSecurityView(generic.ObjectView):
    queryset = Device.objects.all()
    template_name = "netbox_security/device/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(VirtualDeviceContext, name="security")
class VirtualDeviceContextSecurityView(generic.ObjectView):
    queryset = VirtualDeviceContext.objects.all()
    template_name = "netbox_security/virtual_device_context/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(VirtualMachine, name="security")
class VirtualMachineSecurityView(generic.ObjectView):
    queryset = VirtualMachine.objects.all()
    template_name = "netbox_security/virtualmachine/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(IPAddress, name="security")
class IPAddressSecurityView(generic.ObjectView):
    queryset = IPAddress.objects.all()
    template_name = "netbox_security/ipaddress/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(Prefix, name="security")
class PrefixSecurityView(generic.ObjectView):
    queryset = Prefix.objects.all()
    template_name = "netbox_security/prefix/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )


@register_model_view(IPRange, name="security")
class IPRangeSecurityView(generic.ObjectView):
    queryset = IPRange.objects.all()
    template_name = "netbox_security/iprange/security.html"
    tab = ViewTab(
        label=_("Security"),
        hide_if_empty=True,
    )
