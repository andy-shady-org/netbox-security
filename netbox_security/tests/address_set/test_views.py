from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.tests.mixins import AddressSetMixin


class AddressSetViewTestCase(
    AddressSetMixin,
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

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "address-4",
            "identifier": "xyz",
            "addresses": [cls.addresses[0].pk, cls.addresses[1].pk],
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,identifier",
            "address-set-5,abc",
            "address-set-6,efg",
            "address-set-7,hij",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.address_sets[0].pk},address-set-8,test1",
            f"{cls.address_sets[1].pk},address-set-9,test2",
            f"{cls.address_sets[2].pk},address-set-10,test3",
        )

    maxDiff = None
