from netaddr import IPNetwork
from django.contrib.contenttypes.models import ContentType
from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import Address, AddressSet, CustomPrefix


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
        cls.custom_prefixes = (
            CustomPrefix(prefix=IPNetwork("1.1.1.1/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.2/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.3/32")),
        )
        CustomPrefix.objects.bulk_create(cls.custom_prefixes)
        cls.addresses = (
            Address(
                name="address-7",
                assigned_object_id=cls.custom_prefixes[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
            ),
            Address(
                name="address-8",
                assigned_object_id=cls.custom_prefixes[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
            ),
            Address(
                name="address-9",
                assigned_object_id=cls.custom_prefixes[2].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
            ),
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
            f"{cls.addresses_sets[0].pk},address-set-8,test1",
            f"{cls.addresses_sets[1].pk},address-set-9,test2",
            f"{cls.addresses_sets[2].pk},address-set-10,test3",
        )

    maxDiff = None
