from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import NatRuleSet
from netbox_security.choices import NatTypeChoices, RuleDirectionChoices


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
