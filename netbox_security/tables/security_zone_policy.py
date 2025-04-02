import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox.tables.columns import TagColumn, ArrayColumn

from netbox_security.models import SecurityZonePolicy

LOOPS = """
{% for p in value.all %}
    <a href="{{ p.get_absolute_url }}">{{ p }}</a>{% if not forloop.last %}<br />{% endif %}
{% empty %}
    &mdash;
{% endfor %}
"""

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
    source_address = tables.TemplateColumn(template_code=LOOPS, orderable=False)
    destination_address = tables.TemplateColumn(template_code=LOOPS, orderable=False)
    application = ArrayColumn()
    actions = tables.TemplateColumn(template_code=ACTIONS, orderable=False)
    tags = TagColumn(url_name="plugins:netbox_security:securityzone_list")

    class Meta(NetBoxTable.Meta):
        model = SecurityZonePolicy
        fields = (
            "pk",
            "index",
            "name",
            "source_zone",
            "destination_zone",
            "source_address",
            "destination_address",
            "application",
            "actions",
            "description",
            "tags",
        )
        default_columns = (
            "pk",
            "index",
            "name",
            "source_zone",
            "destination_zone",
            "source_address",
            "destination_address",
            "application",
            "actions",
        )
