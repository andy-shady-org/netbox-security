from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import Policer


class PolicerViewTestCase(
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
    model = Policer

    @classmethod
    def setUpTestData(cls):
        cls.policers = (
            Policer(name="policer-1"),
            Policer(name="policer-2"),
            Policer(name="policer-3"),
        )
        Policer.objects.bulk_create(cls.policers)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "policer-4",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name",
            "policer-5",
            "policer-6",
            "policer-7",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.policers[0].pk},policer-8,test1",
            f"{cls.policers[1].pk},policer-9,test2",
            f"{cls.policers[2].pk},policer-10,test3",
        )

    maxDiff = None
