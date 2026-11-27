from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.tests.mixins import AddressMixin


class AddressAPITestCase(
    AddressMixin,
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
    )

    brief_fields = [
        "assigned_object_id",
        "assigned_object_type",
        "description",
        "display",
        "dns_name",
        "id",
        "identifier",
        "name",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Address",
    }
    bulk_update_invalid_data = {
        "dns_name": "invalid_prefix",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.create_data = [
            {
                "name": "address-x",
                "assigned_object_type": "netbox_security.customprefix",
                "assigned_object_id": cls.custom_prefixes[0].pk,
            },
            {
                "name": "address-y",
                "assigned_object_type": "netbox_security.customprefix",
                "assigned_object_id": cls.custom_prefixes[1].pk,
            },
            {
                "name": "address-z",
                "assigned_object_type": "ipam.iprange",
                "assigned_object_id": cls.ranges[0].pk,
            },
            {"name": "address-4", "dns_name": "test.example.com"},
            {"name": "address-5", "dns_name": "*.example.com"},
            {"name": "address-6", "dns_name": "example.com"},
        ]
