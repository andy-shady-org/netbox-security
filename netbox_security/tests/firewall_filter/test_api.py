from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import FirewallFilter
from netbox_security.choices import FamilyChoices


class FirewallFilterAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = FirewallFilter

    brief_fields = ["description", "display", "family", "id", "name", "url"]

    create_data = [
        {"name": "filter-1", "family": FamilyChoices.INET},
        {"name": "filter-2", "family": FamilyChoices.INET},
        {"name": "filter-3", "family": FamilyChoices.INET},
    ]

    bulk_update_data = {
        "description": "Test Firewall Filter",
    }

    @classmethod
    def setUpTestData(cls):
        filters = (
            FirewallFilter(name="filter-4", family=FamilyChoices.INET),
            FirewallFilter(name="filter-5", family=FamilyChoices.INET),
            FirewallFilter(name="filter-6", family=FamilyChoices.INET),
        )
        FirewallFilter.objects.bulk_create(filters)
