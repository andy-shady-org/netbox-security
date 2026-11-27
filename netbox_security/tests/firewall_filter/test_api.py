from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.choices import (
    FamilyChoices,
)
from netbox_security.tests.mixins import FirewallFilterMixin, FirewallFilterRuleMixin


class FirewallFilterAPITestCase(
    FirewallFilterMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):

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
        {"name": "filter-x", "family": FamilyChoices.INET},
        {"name": "filter-y", "family": FamilyChoices.INET},
        {"name": "filter-z", "family": FamilyChoices.INET},
    ]

    bulk_update_data = {
        "description": "Test Firewall Filter",
    }
    bulk_update_invalid_data = {
        "family": "Test Family",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()


class FirewallFilterRuleAPITestCase(
    FirewallFilterRuleMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):

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
    bulk_update_invalid_data = {
        "index": "Test Index",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.create_data = [
            {
                "name": "rule-x",
                "index": 1,
                "firewall_filter": cls.filters[0].pk,
            },
            {
                "name": "rule-y",
                "index": 1,
                "firewall_filter": cls.filters[1].pk,
            },
            {
                "name": "rule-z",
                "index": 1,
                "firewall_filter": cls.filters[2].pk,
            },
        ]
