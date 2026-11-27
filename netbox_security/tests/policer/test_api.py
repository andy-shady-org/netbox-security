from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.tests.mixins import PolicerMixin


class PolicerAPITestCase(
    PolicerMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):

    brief_fields = [
        "bandwidth_limit",
        "bandwidth_percent",
        "burst_size_limit",
        "description",
        "discard",
        "display",
        "forwarding_class",
        "id",
        "logical_interface_policer",
        "loss_priority",
        "name",
        "out_of_profile",
        "physical_interface_policer",
        "url",
    ]

    create_data = [
        {"name": "policer-x"},
        {"name": "policer-y"},
        {"name": "policer-z"},
    ]

    bulk_update_data = {
        "description": "Test Policers",
    }
    bulk_update_invalid_data = {
        "bandwidth_limit": "Test Bandwidth Limit",
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
