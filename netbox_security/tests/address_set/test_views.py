from netaddr import IPNetwork
from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import Address, AddressSet


class AddressSetViewTestCase(
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
    model = AddressSet

    @classmethod
    def setUpTestData(cls):
        cls.addresses = (
            Address(name="address-1", address=IPNetwork("1.1.1.1/32")),
            Address(name="address-2", address=IPNetwork("1.1.1.2/32")),
            Address(name="address-3", address=IPNetwork("1.1.1.3/32")),
        )
        Address.objects.bulk_create(cls.addresses)

        cls.addresses_sets = (
            AddressSet(name="address-set-1"),
            AddressSet(name="address-set-2"),
            AddressSet(name="address-set-3"),
        )
        AddressSet.objects.bulk_create(cls.addresses_sets)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "address-4",
            "addresses": [cls.addresses[0].pk, cls.addresses[1].pk],
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name",
            "address-set-5",
            "address-set-6",
            "address-set-7",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.addresses_sets[0].pk},address-set-8,test1",
            f"{cls.addresses_sets[1].pk},address-set-9,test2",
            f"{cls.addresses_sets[2].pk},address-set-10,test3",
        )

    maxDiff = None
