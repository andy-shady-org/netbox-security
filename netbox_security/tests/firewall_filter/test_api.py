from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import (
    FirewallFilter,
    FirewallFilterRule,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
)
from netbox_security.choices import (
    FamilyChoices,
    FirewallRuleFromSettingChoices,
    FirewallRuleThenSettingChoices,
)


class FirewallFilterAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = FirewallFilter

    brief_fields = [
        "description",
        "display",
        "family",
        "id",
        "name",
        "rule_count",
        "url",
    ]

    create_data = [
        {"name": "filter-1", "family": FamilyChoices.INET},
        {"name": "filter-2", "family": FamilyChoices.INET},
        {"name": "filter-3", "family": FamilyChoices.INET},
    ]

    bulk_update_data = {
        "description": "Test Firewall Filter",
    }

    @classmethod
    def setUpTestData(cls):
        filters = (
            FirewallFilter(name="filter-4", family=FamilyChoices.INET),
            FirewallFilter(name="filter-5", family=FamilyChoices.INET),
            FirewallFilter(name="filter-6", family=FamilyChoices.INET),
        )
        FirewallFilter.objects.bulk_create(filters)


class FirewallFilterRuleAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = FirewallFilterRule

    brief_fields = [
        "description",
        "display",
        "firewall_filter",
        "id",
        "index",
        "name",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Firewall Filter Rule",
    }

    @classmethod
    def setUpTestData(cls):
        cls.filters = (
            FirewallFilter(name="filter-4", family=FamilyChoices.INET),
            FirewallFilter(name="filter-5", family=FamilyChoices.INET),
            FirewallFilter(name="filter-6", family=FamilyChoices.INET),
        )
        FirewallFilter.objects.bulk_create(cls.filters)

        cls.rules = (
            FirewallFilterRule(name="rule-1", firewall_filter=cls.filters[0], index=1),
            FirewallFilterRule(name="rule-2", firewall_filter=cls.filters[1], index=1),
            FirewallFilterRule(name="rule-3", firewall_filter=cls.filters[2], index=1),
        )
        for rule in cls.rules:
            rule.save()

        cls.create_data = [
            {
                "name": "rule-4",
                "index": 1,
                "firewall_filter": cls.filters[0].pk,
            },
            {
                "name": "rule-5",
                "index": 1,
                "firewall_filter": cls.filters[1].pk,
            },
            {
                "name": "rule-6",
                "index": 1,
                "firewall_filter": cls.filters[2].pk,
            },
        ]
