from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import NatRuleSet, NatRule
from netbox_security.choices import (
    NatTypeChoices,
    RuleDirectionChoices,
    RuleStatusChoices,
    AddressTypeChoices,
)


class NatRuleSetAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = NatRuleSet

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
            "name": "set-1",
            "nat_type": NatTypeChoices.TYPE_STATIC,
            "direction": RuleDirectionChoices.DIRECTION_INBOUND,
        },
        {
            "name": "set-2",
            "nat_type": NatTypeChoices.TYPE_STATIC,
            "direction": RuleDirectionChoices.DIRECTION_INBOUND,
        },
        {
            "name": "set-3",
            "nat_type": NatTypeChoices.TYPE_STATIC,
            "direction": RuleDirectionChoices.DIRECTION_INBOUND,
        },
    ]

    bulk_update_data = {
        "description": "Test Nat Rule Set",
    }

    @classmethod
    def setUpTestData(cls):
        rules = (
            NatRuleSet(
                name="set-4",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-5",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-6",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
        )
        NatRuleSet.objects.bulk_create(rules)


class NatRuleAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = NatRule

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

    @classmethod
    def setUpTestData(cls):
        cls.rule_sets = (
            NatRuleSet(
                name="set-4",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-5",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-6",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
        )
        NatRuleSet.objects.bulk_create(cls.rule_sets)

        cls.rules = (
            NatRule(
                name="rule-1",
                rule_set=cls.rule_sets[0],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
            NatRule(
                name="rule-2",
                rule_set=cls.rule_sets[1],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
            NatRule(
                name="rule-3",
                rule_set=cls.rule_sets[2],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatRule.objects.bulk_create(cls.rules)

        cls.create_data = [
            {
                "name": "rule-3",
                "rule_set": cls.rule_sets[0].pk,
                "source_type": AddressTypeChoices.STATIC,
                "destination_type": AddressTypeChoices.STATIC,
                "status": RuleStatusChoices.STATUS_ACTIVE,
                "source_ports": [1,2,3],
                "destination_ports": [1,2,3],
            },
            {
                "name": "rule-4",
                "rule_set": cls.rule_sets[1].pk,
                "source_type": AddressTypeChoices.STATIC,
                "destination_type": AddressTypeChoices.STATIC,
                "status": RuleStatusChoices.STATUS_ACTIVE,
                "source_ports": [1,2,3],
                "destination_ports": [1,2,3],
            },
            {
                "name": "rule-5",
                "rule_set": cls.rule_sets[2].pk,
                "source_type": AddressTypeChoices.STATIC,
                "destination_type": AddressTypeChoices.STATIC,
                "status": RuleStatusChoices.STATUS_ACTIVE,
                "source_ports": [1,2,3],
                "destination_ports": [1,2,3],
            },
        ]
