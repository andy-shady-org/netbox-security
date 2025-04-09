from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import FirewallFilter
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
