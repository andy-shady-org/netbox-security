from netaddr import IPNetwork
from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import CustomPrefix
from netbox_security.tests.mixins import CustomPrefixMixin


class CustomPrefixAPITestCase(
    APITestCase,
    CustomPrefixMixin,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):

    brief_fields = [
        "description",
        "display",
        "id",
        "prefix",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Address",
    }
    bulk_update_invalid_data = {
        "prefix": "invalid_prefix",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.create_data = [
            {
                "prefix": "1.1.2.1/32",
            },
            {
                "prefix": "1.1.2.2/32",
            },
            {
                "prefix": "1.1.2.3/32",
            },
        ]
