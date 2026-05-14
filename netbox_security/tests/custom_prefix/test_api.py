from netaddr import IPNetwork
from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import CustomPrefix


class CustomPrefixAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = CustomPrefix

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

    @classmethod
    def setUpTestData(cls):
        cls.custom_prefixes = (
            CustomPrefix(prefix=IPNetwork("1.1.1.1/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.2/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.3/32")),
        )
        CustomPrefix.objects.bulk_create(cls.custom_prefixes)

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
