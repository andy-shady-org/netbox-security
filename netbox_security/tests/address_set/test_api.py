from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.tests.mixins import AddressSetMixin


class AddressSetAPITestCase(
    AddressSetMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):

    user_permissions = (
        "ipam.view_iprange",
        "ipam.view_prefix",
        "ipam.view_ipaddress",
        "tenancy.view_tenantgroup",
        "tenancy.view_tenant",
        "netbox_security.view_customprefix",
        "netbox_security.view_address"
    )

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
    bulk_update_invalid_data = {
        "addresses": "invalid_prefix",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.address_sets[0].addresses.add(cls.addresses[0])
        cls.address_sets[0].addresses.set(cls.addresses)

        cls.create_data = [
            {"name": "address-set-x", "addresses": [cls.addresses[0].pk]},
            {"name": "address-set-y", "addresses": [cls.addresses[1].pk]},
            {"name": "address-set-z"},
        ]

    def test_address_set(self):
        self.assertEqual(set(self.address_sets[0].addresses.all()), set(self.addresses))
