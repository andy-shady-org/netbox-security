from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.tests.mixins import AddressMixin


class AddressViewTestCase(
    AddressMixin,
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
            "name": "address-5",
            "identifier": "xyz",
            "ipam_prefix": cls.prefixes[0].pk,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,identifier,dns_name",
            "address-10,bil,test2.example.com",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.addresses[0].pk},address-12,test1",
            f"{cls.addresses[1].pk},address-13,test2",
            f"{cls.addresses[2].pk},address-14,test3",
        )

    maxDiff = None
