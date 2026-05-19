from django.urls import reverse
from django.db import models
from taggit.managers import TaggableManager
from extras.managers import NetBoxTaggableManager
from netbox.models import PrimaryModel
from netbox.models.features import ContactsMixin
from ipam.fields import IPNetworkField
from netbox.search import SearchIndex, register_search

__all__ = (
    "CustomPrefix",
    "CustomPrefixIndex",
)


class CustomPrefix(ContactsMixin, PrimaryModel):
    prefix = IPNetworkField(help_text="IPv4 or IPv6 network with mask")
    tags = TaggableManager(
        through='extras.TaggedItem',
        ordering=('weight', 'name'),
        manager=NetBoxTaggableManager,
        related_name='netbox_security_customprefix_set',
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.SET_NULL,
        related_name="%(class)s_related",
        blank=True,
        null=True,
    )

    clone_fields = ("prefix",)
    prerequisite_models = ()

    class Meta:
        default_related_name = "%(app_label)s_%(model_name)s_set"
        ordering = [
            "prefix",
        ]
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "prefix",
                    "tenant",
                ),
                name="%(app_label)s_%(class)s_unique_prefix",
                violation_error_message="Prefix must be unique or unique within a tenant.",
            ),
        )

    def __str__(self):
        return f"{self.prefix}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_security:customprefix", args=[self.pk])


@register_search
class CustomPrefixIndex(SearchIndex):
    model = CustomPrefix
    fields = (("prefix", 100),)
