from netaddr import IPNetwork
from utilities.testing import ViewTestCases, create_tags


from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import CustomPrefix


class CustomPrefixViewTestCase(
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
    model = CustomPrefix

    @classmethod
    def setUpTestData(cls):
        cls.custom_prefixes = (
            CustomPrefix(prefix=IPNetwork("1.1.1.1/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.2/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.3/32")),
        )
        CustomPrefix.objects.bulk_create(cls.custom_prefixes)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "prefix": IPNetwork("1.1.1.4/32"),
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "prefix,description",
            "1.1.1.5/32,test prefix",
        )

        cls.csv_update_data = (
            "id,prefix,description",
            f"{cls.custom_prefixes[0].pk},1.1.1.6/32,test1",
            f"{cls.custom_prefixes[1].pk},1.1.1.7/32,test2",
            f"{cls.custom_prefixes[2].pk},1.1.1.8/32,test3",
        )

    maxDiff = None
