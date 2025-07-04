from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import Address, AddressSet


class AddressSetAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = AddressSet

    brief_fields = [
        "address_sets",
        "addresses",
        "description",
        "display",
        "id",
        "identifier",
        "name",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Address Set",
    }

    @classmethod
    def setUpTestData(cls):
        cls.addresses = (
            Address(name="address-1", address="1.1.1.1/32"),
            Address(name="address-2", address="1.1.1.2/32"),
            Address(name="address-3", address="1.1.1.3/32"),
        )
        Address.objects.bulk_create(cls.addresses)

        cls.create_data = [
            {"name": "address-set-1", "addresses": [cls.addresses[0].pk]},
            {"name": "address-set-2", "addresses": [cls.addresses[1].pk]},
            {"name": "address-set-3"},
        ]

        cls.addresses_sets = (
            AddressSet(name="address-set-5"),
            AddressSet(name="address-set-6"),
            AddressSet(name="address-set-7"),
        )
        AddressSet.objects.bulk_create(cls.addresses_sets)

        cls.address_set = AddressSet.objects.create(name="address-set-8")
        cls.address_set.addresses.add(cls.addresses[0])
        cls.address_set.addresses.set(cls.addresses)

    def test_address_set(self):
        self.assertEqual(set(self.address_set.addresses.all()), set(self.addresses))
