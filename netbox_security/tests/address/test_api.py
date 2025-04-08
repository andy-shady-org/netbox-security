from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import Address


class AddressAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Address

    brief_fields = ["description", "display", "id", "name", "url", "value"]

    create_data = [
        {"name": "address-1", "value": "1.1.1.1/32"},
        {"name": "address-2", "value": "1.1.1.2/32"},
        {"name": "address-3", "value": "1.1.1.3/32"},
    ]

    bulk_update_data = {
        "description": "Test Address",
    }

    @classmethod
    def setUpTestData(cls):
        addresses = (
            Address(name="address-4", value="1.1.1.4/32"),
            Address(name="address-5", value="1.1.1.5/32"),
            Address(name="address-6", value="1.1.1.6/32"),
        )
        Address.objects.bulk_create(addresses)
