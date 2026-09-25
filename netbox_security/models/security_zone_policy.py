from django.urls import reverse
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from netbox.search import SearchIndex, register_search

from netbox.models import PrimaryModel
from netbox.models.features import ContactsMixin
from netbox_security.choices import ActionChoices
from netbox_security.fields import ChoiceArrayField

__all__ = (
    "SecurityZonePolicy",
    "SecurityZonePolicyIndex",
)


class SecurityZonePolicy(ContactsMixin, PrimaryModel):
    name = models.CharField(
        max_length=100,
    )
    index = models.PositiveIntegerField()
    identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    source_zone = models.ForeignKey(
        to="netbox_security.SecurityZone",
        related_name="source_zone_policies",
        on_delete=models.CASCADE,
    )
    destination_zone = models.ForeignKey(
        to="netbox_security.SecurityZone",
        related_name="destination_zone_policies",
        on_delete=models.CASCADE,
    )
    source_address = models.ManyToManyField(
        to="netbox_security.AddressList",
        related_name="%(class)s_source_address",
    )
    destination_address = models.ManyToManyField(
        to="netbox_security.AddressList",
        related_name="%(class)s_destination_address",
    )
    applications = models.ManyToManyField(
        to="netbox_security.Application",
        blank=True,
        related_name="%(class)s_applications",
    )
    application_sets = models.ManyToManyField(
        to="netbox_security.ApplicationSet",
        blank=True,
        related_name="%(class)s_application_sets",
    )
    policy_actions = ChoiceArrayField(
        base_field=models.CharField(
            max_length=20,
            choices=ActionChoices,
            blank=False,
            null=False,
        ),
        size=4,
        blank=False,
        null=False,
        validators=[MinLengthValidator(1)],
        verbose_name=_("Policy Actions"),
    )
    prerequisite_models = ("netbox_security.SecurityZone",)

    class Meta:
        verbose_name_plural = _("Security Zone Policies")
        ordering = ["index", "name"]
        unique_together = ["name", "identifier", "source_zone", "destination_zone"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:securityzonepolicy", args=[self.pk])

    def clean(self):
        super().clean()

        # Required-field validation handles missing zones.
        if not self.source_zone_id or not self.destination_zone_id:
            return

        if (
            self.source_zone_id == self.destination_zone_id
            and not self.source_zone.allow_intra_zone
        ):
            message = _(
                "Cannot have the same source and destination zone "
                "unless intra-zone traffic is allowed."
            )
            raise ValidationError(
                {
                    "source_zone": [message],
                    "destination_zone": [message],
                }
            )

        self.validate_address_overlap(
            source_addresses=self._effective_addresses("source_address"),
            destination_addresses=self._effective_addresses("destination_address"),
        )

    def _effective_addresses(self, field_name):
        # NetBox supplies pending M2M values before model validation in forms,
        # imports, API serializers, and bulk edits. None preserves the current
        # selection, matching this policy's serializer update semantics.
        pending = getattr(self, "_m2m_values", {})
        if field_name in pending and pending[field_name] is not None:
            return pending[field_name]
        if self._state.adding:
            return ()
        return getattr(self, field_name).all()

    def validate_address_overlap(self, *, source_addresses, destination_addresses):
        """Validate the proposed final selections of AddressList objects."""
        allow_overlap = (
            self.source_zone_id is not None
            and self.source_zone_id == self.destination_zone_id
            and self.source_zone.allow_intra_zone
        )

        if allow_overlap:
            return

        source_ids = {getattr(address, "pk", address) for address in source_addresses}
        destination_ids = {
            getattr(address, "pk", address) for address in destination_addresses
        }

        if source_ids & destination_ids:
            message = _(
                "Source and destination addresses cannot overlap unless "
                "both zones are the same and allow intra-zone traffic."
            )
            raise ValidationError(
                {
                    "source_address": [message],
                    "destination_address": [message],
                }
            )


@register_search
class SecurityZonePolicyIndex(SearchIndex):
    model = SecurityZonePolicy
    fields = (
        ("name", 100),
        ("identifier", 300),
        ("source_zone", 300),
        ("destination_zone", 300),
        ("source_address", 300),
        ("destination_address", 300),
        ("applications", 300),
        ("application_sets", 300),
        ("description", 500),
    )
