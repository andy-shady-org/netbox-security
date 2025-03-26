import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netaddr.core import AddrFormatError
from netaddr import IPNetwork
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter, MultiValueCharFilter, MultiValueNumberFilter
)

from dcim.models import Device, VirtualDeviceContext

from netbox_security.models import (
    Address,
    AddressAssignment,
    SecurityZone,
)


class AddressFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    value = django_filters.CharFilter(
        method='filter_value',
        label=_('Value'),
    )

    class Meta:
        model = Address
        fields = ['id', 'name', 'description']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(name__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)

    def filter_value(self, queryset, name, value):
        if not value.strip():
            return queryset
        try:
            query = str(IPNetwork(value).cidr)
            return queryset.filter(prefix=query)
        except (AddrFormatError, ValueError):
            return queryset.none()


class AddressAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    zone_id = django_filters.ModelMultipleChoiceFilter(
        queryset=SecurityZone.objects.all(),
        label=_('Security Zone (ID)'),
    )
    device = MultiValueCharFilter(
        method='filter_device',
        field_name='name',
        label=_('Device (name)'),
    )
    device_id = MultiValueNumberFilter(
        method='filter_device',
        field_name='pk',
        label=_('Device (ID)'),
    )
    virtualdevicecontext = MultiValueCharFilter(
        method='filter_context',
        field_name='name',
        label=_('Virtual Device Context (name)'),
    )
    virtualdevicecontext_id = MultiValueNumberFilter(
        method='filter_context',
        field_name='pk',
        label=_('Virtual Device Context (ID)'),
    )
    securityzone = MultiValueCharFilter(
        method='filter_securityzone',
        field_name='name',
        label=_('Security Zone (name)'),
    )
    securityzone_id = MultiValueNumberFilter(
        method='filter_securityzone',
        field_name='pk',
        label=_('Security Zone (ID)'),
    )

    class Meta:
        model = AddressAssignment
        fields = ('id', 'zone_id', 'assigned_object_type', 'assigned_object_id')

    def filter_device(self, queryset, name, value):
        devices = Device.objects.filter(**{f'{name}__in': value})
        if not devices.exists():
            return queryset.none()
        device_ids = []
        device_ids.extend(Device.objects.filter(**{f'{name}__in': value}).values_list('id', flat=True))
        return queryset.filter(
            Q(assigned_object_type=ContentType.objects.get_for_model(Device), assigned_object_id__in=device_ids)
        )

    def filter_context(self, queryset, name, value):
        devices = VirtualDeviceContext.objects.filter(**{f'{name}__in': value})
        if not devices.exists():
            return queryset.none()
        device_ids = []
        device_ids.extend(VirtualDeviceContext.objects.filter(**{f'{name}__in': value}).values_list('id', flat=True))
        return queryset.filter(
            Q(assigned_object_type=ContentType.objects.get_for_model(Device), assigned_object_id__in=device_ids)
        )

    def filter_securityzone(self, queryset, name, value):
        zones = SecurityZone.objects.filter(**{f'{name}__in': value})
        if not zones.exists():
            return queryset.none()
        zone_ids = []
        zone_ids.extend(SecurityZone.objects.filter(**{f'{name}__in': value}).values_list('id', flat=True))
        return queryset.filter(
            Q(assigned_object_type=ContentType.objects.get_for_model(SecurityZone), assigned_object_id__in=zone_ids)
        )
