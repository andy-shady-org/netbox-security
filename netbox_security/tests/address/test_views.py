from netaddr import IPNetwork
from utilities.testing import ViewTestCases, create_tags
from ipam.models import IPRange

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
        cls.ranges = (
            IPRange(
                start_address="1.1.1.2/24",
                end_address="1.1.1.5/24",
                status="active",
                size=4,
            ),
            IPRange(
                start_address="1.1.2.2/24",
                end_address="1.1.2.5/24",
                status="active",
                size=4,
            ),
            IPRange(
                start_address="1.1.3.2/24",
                end_address="1.1.3.5/24",
                status="active",
                size=4,
            ),
        )
        IPRange.objects.bulk_create(cls.ranges)

        cls.addresses = (
            Address(name="address-1", address=IPNetwork("1.1.1.1/32")),
            Address(name="address-2", address=IPNetwork("1.1.1.2/32")),
            Address(name="address-3", address=IPNetwork("1.1.1.3/32")),
            Address(name="address-4", dns_name="test.example.com"),
            Address(name="address-5", ip_range=cls.ranges[0]),
            Address(name="address-6", ip_range=cls.ranges[0]),
        )
        Address.objects.bulk_create(cls.addresses)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "address-5",
            "identifier": "xyz",
            "address": IPNetwork("1.1.1.4/32"),
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,identifier,address,dns_name,ip_range",
            "address-7,abc,1.1.1.5/32,,",
            "address-8,efg,1.1.1.6/32,,",
            "address-9,dad,1.1.1.7/32,,",
            "address-10,bil,,test2.example.com,",
            "address-11,poo,,,1.1.3.2/24",
        )

        cls.csv_update_data = (
            "id,name,address,description",
            f"{cls.addresses[0].pk},address-12,1.1.1.8/32,test1",
            f"{cls.addresses[1].pk},address-13,1.1.1.9/32,test2",
            f"{cls.addresses[2].pk},address-14,1.1.1.10/32,test3",
        )

    maxDiff = None
