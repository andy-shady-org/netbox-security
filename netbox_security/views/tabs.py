from django.utils.translation import gettext_lazy as _

from dcim.models import Device, VirtualDeviceContext
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
