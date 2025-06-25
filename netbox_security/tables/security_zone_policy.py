import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ManyToManyColumn, ChoicesColumn

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
        linkify_item=True,
    )
    destination_address = ManyToManyColumn(
        linkify_item=True,
    )
    applications = ManyToManyColumn(
        linkify_item=True,
    )
    application_sets = ManyToManyColumn(linkify_item=True)
    policy_actions = ChoicesColumn(template_code=ACTIONS, orderable=False)
    tags = TagColumn(url_name="plugins:netbox_security:securityzone_list")

    class Meta(NetBoxTable.Meta):
        model = SecurityZonePolicy
        fields = (
            "id",
            "index",
            "name",
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
            "source_zone",
            "destination_zone",
            "source_address",
            "destination_address",
            "applications",
            "application_sets",
            "policy_actions",
        )
