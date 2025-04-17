from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import FirewallFilter, FirewallFilterRule
from netbox_security.choices import FamilyChoices


class FirewallFilterViewTestCase(
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
    model = FirewallFilter

    @classmethod
    def setUpTestData(cls):
        cls.filters = (
            FirewallFilter(name="filter-1", family=FamilyChoices.INET),
            FirewallFilter(name="filter-2", family=FamilyChoices.INET),
            FirewallFilter(name="filter-3", family=FamilyChoices.INET),
        )
        FirewallFilter.objects.bulk_create(cls.filters)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "filter-4",
            "family": "inet",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,family",
            "filter-5,inet",
            "filter-6,inet",
            "filter-7,inet",
        )

        cls.csv_update_data = (
            "id,name,family,description",
            f"{cls.filters[0].pk},filter-8,inet,test1",
            f"{cls.filters[1].pk},filter-9,inet,test2",
            f"{cls.filters[2].pk},filter-10,inet,test3",
        )

    maxDiff = None


class FirewallFilterRuleViewTestCase(
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
    model = FirewallFilterRule

    @classmethod
    def setUpTestData(cls):
        cls.filters = (
            FirewallFilter(name="filter-1", family=FamilyChoices.INET),
            FirewallFilter(name="filter-2", family=FamilyChoices.INET),
            FirewallFilter(name="filter-3", family=FamilyChoices.INET),
        )
        FirewallFilter.objects.bulk_create(cls.filters)

        cls.rules = (
            FirewallFilterRule(name="rule-1", firewall_filter=cls.filters[0], index=1),
            FirewallFilterRule(name="rule-2", firewall_filter=cls.filters[1], index=1),
            FirewallFilterRule(name="rule-3", firewall_filter=cls.filters[2], index=1),
        )
        FirewallFilterRule.objects.bulk_create(cls.rules)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "rule-4",
            "index": 1,
            "firewall_filter": cls.filters[0].pk,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,index,firewall_filter",
            f"rule-5,1,{cls.filters[0].name}",
            f"rule-6,1,{cls.filters[1].name}",
            f"rule-7,1,{cls.filters[2].name}",
        )

        cls.csv_update_data = (
            "id,name,index,firewall_filter,description",
            f"{cls.rules[0].pk},rule-8,1,{cls.filters[0].name},test1",
            f"{cls.rules[1].pk},rule-9,2,{cls.filters[1].name},test2",
            f"{cls.rules[2].pk},rule-10,3,{cls.filters[2].name},test3",
        )

    maxDiff = None
