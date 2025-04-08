from netaddr import IPNetwork
from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import Address


class AddressViewTestCase(
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
    model = Address

    @classmethod
    def setUpTestData(cls):
        cls.addresses = (
            Address(name="address-1", value=IPNetwork("1.1.1.1/32")),
            Address(name="address-2", value=IPNetwork("1.1.1.2/32")),
            Address(name="address-3", value=IPNetwork("1.1.1.3/32")),
        )
        Address.objects.bulk_create(cls.addresses)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "address-4", "value": IPNetwork("1.1.1.4/32"),
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,value",
            "address-5,1.1.1.5/32",
            "address-6,1.1.1.6/32",
            "address-7,1.1.1.7/32",
        )

        cls.csv_update_data = (
            "id,name,value,description",
            f"{cls.addresses[0].pk},address-8,1.1.1.8/32,test1",
            f"{cls.addresses[1].pk},address-9,1.1.1.9/32,test2",
            f"{cls.addresses[2].pk},address-10,1.1.1.10/32,test3",
        )

    maxDiff = None
