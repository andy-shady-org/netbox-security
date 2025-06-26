import django_filters
from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from utilities.data import array_to_string
from ipam.constants import SERVICE_PORT_MIN, SERVICE_PORT_MAX
from utilities.forms.fields import (
    NumericArrayField,
)
from utilities.filters import NumericArrayFilter

__all__ = (
    "PortsMixin",
    "PortsForm",
    "PortsFilterSet",
)


class PortsMixin(models.Model):
    """
    Enables the assignments of source and destination port variables.
    """

    source_ports = ArrayField(
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(SERVICE_PORT_MIN),
                MaxValueValidator(SERVICE_PORT_MAX),
            ]
        ),
        null=True,
        blank=True,
        verbose_name=_("Source Port numbers"),
    )
    destination_ports = ArrayField(
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(SERVICE_PORT_MIN),
                MaxValueValidator(SERVICE_PORT_MAX),
            ]
        ),
        null=True,
        blank=True,
        verbose_name=_("Destination Port numbers"),
    )

    class Meta:
        abstract = True

    @property
    def source_port_list(self):
        return array_to_string(self.source_ports)

    @property
    def destination_port_list(self):
        return array_to_string(self.destination_ports)


class PortsForm(forms.Form):
    source_ports = NumericArrayField(
        base_field=forms.IntegerField(
            min_value=SERVICE_PORT_MIN, max_value=SERVICE_PORT_MAX
        ),
        help_text="Comma-separated list of one or more port numbers. A range may be specified using a hyphen.",
        required=False,
    )
    destination_ports = NumericArrayField(
        base_field=forms.IntegerField(
            min_value=SERVICE_PORT_MIN, max_value=SERVICE_PORT_MAX
        ),
        help_text="Comma-separated list of one or more port numbers. A range may be specified using a hyphen.",
        required=False,
    )


class PortsFilterSet(django_filters.FilterSet):
    source_ports = NumericArrayFilter(field_name="source_ports", lookup_expr="contains")
    destination_ports = NumericArrayFilter(
        field_name="destination_ports", lookup_expr="contains"
    )
