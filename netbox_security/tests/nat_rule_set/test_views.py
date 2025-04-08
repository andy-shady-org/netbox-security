from utilities.testing import ViewTestCases, create_tags
from ipam.choices import IPAddressStatusChoices

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import NatRuleSet
from netbox_security.choices import NatTypeChoices, RuleDirectionChoices


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
