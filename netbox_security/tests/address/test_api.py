from utilities.testing import APIViewTestCases
from ipam.models import IPRange
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

    brief_fields = [
        "address",
        "description",
        "display",
        "dns_name",
        "id",
        "identifier",
        "ip_range",
        "name",
        "url",
    ]

    create_data = [
        {"name": "address-1", "address": "1.1.1.1/32"},
        {"name": "address-2", "address": "1.1.1.2/32"},
        {"name": "address-3", "address": "1.1.1.3/32"},
        {"name": "address-4", "dns_name": "test.example.com"},
        {"name": "address-5", "dns_name": "*.example.com"},
        {"name": "address-6", "dns_name": "example.com"},
    ]

    bulk_update_data = {
        "description": "Test Address",
    }

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

        addresses = (
            Address(name="address-7", address="1.1.1.4/32"),
            Address(name="address-8", address="1.1.1.5/32"),
            Address(name="address-9", address="1.1.1.6/32"),
            Address(name="address-11", dns_name="test1.example.com"),
            Address(name="address-12", ip_range=cls.ranges[0]),
            Address(name="address-13", ip_range=cls.ranges[1]),
            Address(name="address-14", dns_name="test2.example.com"),
        )
        Address.objects.bulk_create(addresses)
