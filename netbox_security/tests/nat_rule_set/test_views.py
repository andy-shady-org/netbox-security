from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import NatRuleSet, NatRule
from netbox_security.choices import (
    NatTypeChoices,
    RuleDirectionChoices,
    RuleStatusChoices,
    AddressTypeChoices,
)


class NatRuleSetViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = NatRuleSet

    @classmethod
    def setUpTestData(cls):
        cls.rules = (
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
        NatRuleSet.objects.bulk_create(cls.rules)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "set-4",
            "nat_type": "static",
            "direction": "inbound",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,nat_type,direction",
            "set-5,static,inbound",
            "set-6,static,inbound",
            "set-7,static,inbound",
        )

        cls.csv_update_data = (
            "id,name,nat_type,direction,description",
            f"{cls.rules[0].pk},set-8,static,inbound,test1",
            f"{cls.rules[1].pk},set-9,static,inbound,test2",
            f"{cls.rules[2].pk},set-10,static,inbound,test3",
        )

    maxDiff = None


class NatRuleViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = NatRule

    @classmethod
    def setUpTestData(cls):
        cls.rule_sets = (
            NatRuleSet(
                name="set-1",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-2",
                nat_type=NatTypeChoices.TYPE_STATIC,
                direction=RuleDirectionChoices.DIRECTION_INBOUND,
            ),
            NatRuleSet(
                name="set-3",
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
        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "rule-4",
            "rule_set": cls.rule_sets[0].pk,
            "source_type": AddressTypeChoices.STATIC,
            "destination_type": AddressTypeChoices.STATIC,
            "status": RuleStatusChoices.STATUS_ACTIVE,
            "source_ports": "1,2,3",
            "destination_ports": "1,2,3",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,rule_set,source_type,destination_type,status",
            "rule-5,set-1,static,static,active",
            "rule-6,set-1,static,static,active",
            "rule-7,set-1,static,static,active",
        )

        cls.csv_update_data = (
            "id,name,rule_set,source_type,destination_type,status",
            f"{cls.rules[0].pk},rule-8,set-2,static,static,active",
            f"{cls.rules[1].pk},rule-9,set-2,static,static,active",
            f"{cls.rules[2].pk},rule-10,set-2,static,static,active",
        )

    maxDiff = None
