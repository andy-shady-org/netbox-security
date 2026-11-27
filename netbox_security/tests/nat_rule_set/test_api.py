from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.choices import (
    NatTypeChoices,
    RuleDirectionChoices,
    RuleStatusChoices,
    AddressTypeChoices,
)
from netbox_security.tests.mixins import NatRuleSetMixin, NatRuleSetRuleMixin


class NatRuleSetAPITestCase(
    NatRuleSetMixin,
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
        "direction",
        "display",
        "id",
        "name",
        "nat_type",
        "rule_count",
        "url",
    ]

    create_data = [
        {
            "name": "set-x",
            "nat_type": NatTypeChoices.TYPE_STATIC,
            "direction": RuleDirectionChoices.DIRECTION_INBOUND,
        },
        {
            "name": "set-y",
            "nat_type": NatTypeChoices.TYPE_STATIC,
            "direction": RuleDirectionChoices.DIRECTION_INBOUND,
        },
        {
            "name": "set-z",
            "nat_type": NatTypeChoices.TYPE_STATIC,
            "direction": RuleDirectionChoices.DIRECTION_INBOUND,
        },
    ]

    bulk_update_data = {
        "description": "Test Nat Rule Set",
    }
    bulk_update_invalid_data = {
        "nat_type": "Test NAT Type",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()


class NatRuleAPITestCase(
    NatRuleSetRuleMixin,
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
        "id",
        "name",
        "rule_set",
        "status",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Nat Rule",
    }
    bulk_update_invalid_data = {
        "status": "invalid status",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.create_data = [
            {
                "name": "rule-3",
                "rule_set": cls.rule_sets[0].pk,
                "source_type": AddressTypeChoices.STATIC,
                "destination_type": AddressTypeChoices.STATIC,
                "status": RuleStatusChoices.STATUS_ACTIVE,
                "source_ports": [1, 2, 3],
                "destination_ports": [1, 2, 3],
            },
            {
                "name": "rule-4",
                "rule_set": cls.rule_sets[1].pk,
                "source_type": AddressTypeChoices.STATIC,
                "destination_type": AddressTypeChoices.STATIC,
                "status": RuleStatusChoices.STATUS_ACTIVE,
                "source_ports": [1, 2, 3],
                "destination_ports": [1, 2, 3],
            },
            {
                "name": "rule-5",
                "rule_set": cls.rule_sets[2].pk,
                "source_type": AddressTypeChoices.STATIC,
                "destination_type": AddressTypeChoices.STATIC,
                "status": RuleStatusChoices.STATUS_ACTIVE,
                "source_ports": [1, 2, 3],
                "destination_ports": [1, 2, 3],
            },
        ]
