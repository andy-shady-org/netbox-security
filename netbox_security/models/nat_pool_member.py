from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from netbox.search import SearchIndex, register_search

from netbox.models import PrimaryModel
from ipam.choices import (
    IPAddressStatusChoices,
)

from netbox_security.mixins import PortsMixin

__all__ = (
    "NatPoolMember",
    "NatPoolMemberIndex",
)


class NatPoolMember(PortsMixin, PrimaryModel):
    """ """

    name = models.CharField(max_length=100)
    pool = models.ForeignKey(
        to="netbox_security.NatPool",
        on_delete=models.CASCADE,
        related_name="%(class)s_pools",
    )
    status = models.CharField(
        max_length=50,
        choices=IPAddressStatusChoices,
        default=IPAddressStatusChoices.STATUS_ACTIVE,
        verbose_name=_("Status"),
        help_text=_("The operational status of this NAT Pool Member"),
    )
    address = models.ForeignKey(
        to="ipam.IPAddress",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    prefix = models.ForeignKey(
        to="ipam.Prefix",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    address_range = models.ForeignKey(
        to="ipam.IPRange",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    prerequisite_models = ("netbox_security.NatPool",)

    class Meta:
        verbose_name = _("NAT Pool Member")
        verbose_name_plural = _("NAT Pool Members")
        ordering = ("pool", "name")
        unique_together = ("pool", "name")

    @property
    def network(self):
        return self.prefix

    def __str__(self):
        return f"{self.name}"

    def get_status_color(self):
        return getattr(IPAddressStatusChoices, "colors", {}).get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:natpoolmember", args=[self.pk])

    def _get_status_target(self):
        if self.address is not None:
            return self.address
        if self.prefix is not None:
            return self.prefix
        if self.address_range is not None:
            return self.address_range
        return None

    def _get_status_target_model(self):
        if self.address is not None:
            return self._meta.get_field("address").remote_field.model
        if self.prefix is not None:
            return self._meta.get_field("prefix").remote_field.model
        if self.address_range is not None:
            return self._meta.get_field("address_range").remote_field.model
        return None

    def sync_related_object_status(self, user):
        target_model = self._get_status_target_model()
        target = self._get_status_target()

        if user is None or target_model is None or target is None:
            return False

        queryset = target_model.objects.all()
        restricted_queryset = getattr(queryset, "restrict")(user, "change")
        target = restricted_queryset.filter(pk=target.pk).first()
        if target is None or target.status == self.status:
            return False

        target.status = self.status
        target.save(update_fields=["status"])
        return True

    def clean(self):
        super().clean()
        # make sure that only one field is set
        if self.prefix and self.address and self.address_range:
            raise ValidationError(
                {"prefix": "Cannot set Address, Prefix and Address Range fields"}
            )

        if self.address and self.address_range:
            raise ValidationError(
                {"prefix": "Cannot set Address and Address Range fields"}
            )

        if self.prefix and self.address_range:
            raise ValidationError(
                {"prefix": "Cannot set Prefix and Address Range fields"}
            )

        if self.prefix and self.address:
            raise ValidationError({"prefix": "Cannot set Address and Prefix fields"})

        # at least one field must be set
        if self.prefix is None and self.address is None and self.address_range is None:
            raise ValidationError({"prefix": "Cannot set all fields to Null"})

        if target_model := self._get_status_target_model():
            status_field = target_model._meta.get_field("status")
            try:
                status_field.clean(self.status, self)
            except ValidationError as exc:
                raise ValidationError({"status": exc.messages}) from exc

    def save(self, *args, **kwargs):
        sync_user = getattr(self, "_status_sync_user", None)

        rv = super().save(*args, **kwargs)

        if sync_user is not None:
            self.sync_related_object_status(sync_user)
            self._status_sync_user = None

        return rv


@register_search
class NatPoolMemberIndex(SearchIndex):
    model = NatPoolMember
    fields = (
        ("name", 100),
        ("description", 100),
        ("pool", 300),
        ("address", 300),
        ("prefix", 300),
        ("address_range", 300),
        ("status", 300),
    )
