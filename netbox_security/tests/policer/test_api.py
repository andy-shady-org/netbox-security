from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import Policer


class PolicerAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Policer

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
        {"name": "policer-1"},
        {"name": "policer-2"},
        {"name": "policer-3"},
    ]

    bulk_update_data = {
        "description": "Test Policers",
    }

    @classmethod
    def setUpTestData(cls):
        policers = (
            Policer(name="policer-4"),
            Policer(name="policer-5"),
            Policer(name="policer-6"),
        )
        Policer.objects.bulk_create(policers)
