import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ManyToManyColumn

from netbox_security.models import SecurityZonePolicy

ACTIONS = """
{% for action in value %}
    <span class="badge text-bg-{% if action == 'permit' %}green
    {% elif action == 'deny' %}red
    {% elif action == 'log' %}orange
    {% elif action == 'count' %}blue
    {% elif action == 'reject' %}red
    {% endif %}"
    >{{ action }}</span>
{% endfor %}
"""


__all__ = ("SecurityZonePolicyTable",)


class SecurityZonePolicyTable(NetBoxTable):
    name = tables.LinkColumn()
    source_zone = tables.LinkColumn()
    destination_zone = tables.LinkColumn()
    source_address = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Source Address")
    )
    destination_address = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Destination Address")
    )
    applications = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Applications")
    )
    application_sets = ManyToManyColumn(
        orderable=False, linkify=True, verbose_name=_("Application Sets")
    )
    policy_actions = tables.TemplateColumn(template_code=ACTIONS, orderable=False)
    tags = TagColumn(url_name="plugins:netbox_security:securityzone_list")

    class Meta(NetBoxTable.Meta):
        model = SecurityZonePolicy
        fields = (
            "id",
            "index",
            "name",
            "identifier",
            "source_zone",
            "destination_zone",
            "source_address",
            "destination_address",
            "applications",
            "application_sets",
            "policy_actions",
            "description",
            "tags",
        )
        default_columns = (
            "index",
            "name",
            "identifier",
            "source_zone",
            "destination_zone",
            "source_address",
            "destination_address",
            "applications",
            "application_sets",
            "policy_actions",
        )
