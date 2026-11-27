from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import ApplicationItem, Application, ApplicationSet
from netbox_security.choices import ProtocolChoices
from netbox_security.tests.mixins import (
    ApplicationItemMixin,
    ApplicationMixin,
    ApplicationSetMixin,
)


class ApplicationItemAPITestCase(
    ApplicationItemMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    # TODO: Remove this override once NetBox fixes enum-backed ArrayLookup
    # auto-filter rendering in utilities.testing.api (_emit_array_lookup_filter_tests).
    graphql_auto_filter_exclude = ("protocol",)

    brief_fields = [
        "description",
        "destination_ports",
        "display",
        "id",
        "index",
        "name",
        "protocol",
        "source_ports",
        "url",
    ]

    create_data = [
        {
            "name": "item-x",
            "destination_ports": [1],
            "source_ports": [1],
            "index": 1,
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-y",
            "destination_ports": [2],
            "source_ports": [2],
            "index": 2,
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-z",
            "destination_ports": [3],
            "source_ports": [3],
            "index": 4,
            "protocol": [ProtocolChoices.TCP],
        },
    ]

    bulk_update_data = {
        "description": "Test Item",
    }
    bulk_update_invalid_data = {"protocol": ["ABC"]}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()


class ApplicationAPITestCase(
    ApplicationMixin,
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    # TODO: Remove this override once NetBox fixes enum-backed ArrayLookup
    # auto-filter rendering in utilities.testing.api (_emit_array_lookup_filter_tests).
    graphql_auto_filter_exclude = ("protocol",)

    user_permissions = (
        "netbox_security.view_applicationitem",
    )

    brief_fields = [
        "application_items",
        "description",
        "destination_ports",
        "display",
        "id",
        "identifier",
        "name",
        "protocol",
        "source_ports",
        "url",
    ]

    create_data = [
        {
            "name": "item-x",
            "destination_ports": [1],
            "source_ports": [1],
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-y",
            "destination_ports": [1],
            "source_ports": [1],
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-z",
            "destination_ports": [1],
            "source_ports": [1],
            "protocol": [ProtocolChoices.TCP],
        },
    ]

    bulk_update_data = {
        "description": "Test Item",
    }
    bulk_update_invalid_data = {"protocol": ["ABC"]}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.applications[2].application_items.set([cls.items[0], cls.items[1]])


class ApplicationSetAPITestCase(
    ApplicationSetMixin,
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
        "netbox_security.view_applicationitem",
        "netbox_security.view_application",
    )

    brief_fields = [
        "application_sets",
        "applications",
        "description",
        "display",
        "id",
        "identifier",
        "name",
        "url",
    ]

    create_data = [
        {
            "name": "app-x",
        },
        {
            "name": "app-y",
        },
        {
            "name": "app-z",
        },
    ]

    bulk_update_data = {
        "description": "Test Item",
    }
    bulk_update_invalid_data = {"applications": ["ABC"]}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.applications[1].application_items.set([cls.items[0]])
        cls.applications[2].application_items.set([cls.items[1], cls.items[2]])
        cls.application_sets[0].applications.set(
            [
                cls.applications[0],
            ]
        )
        cls.application_sets[1].applications.set(
            [
                cls.applications[0],
                cls.applications[1],
            ]
        )
        cls.application_sets[2].applications.set(
            [
                cls.applications[1],
                cls.applications[2],
            ]
        )
