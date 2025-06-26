from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import ApplicationItem, Application, ApplicationSet
from netbox_security.choices import ProtocolChoices


class ApplicationItemAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = ApplicationItem

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
            "name": "item-1",
            "destination_ports": [1],
            "source_ports": [1],
            "index": 1,
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-2",
            "destination_ports": [2],
            "source_ports": [2],
            "index": 2,
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-3",
            "destination_ports": [3],
            "source_ports": [3],
            "index": 4,
            "protocol": [ProtocolChoices.TCP],
        },
    ]

    bulk_update_data = {
        "description": "Test Item",
    }

    @classmethod
    def setUpTestData(cls):
        items = (
            ApplicationItem(
                name="item-7",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-8",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-9",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(items)


class ApplicationAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Application

    brief_fields = [
        "application_items",
        "description",
        "destination_ports",
        "display",
        "id",
        "name",
        "protocol",
        "source_ports",
        "url",
    ]

    create_data = [
        {
            "name": "item-1",
            "destination_ports": [1],
            "source_ports": [1],
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-2",
            "destination_ports": [1],
            "source_ports": [1],
            "protocol": [ProtocolChoices.TCP],
        },
        {
            "name": "item-3",
            "destination_ports": [1],
            "source_ports": [1],
            "protocol": [ProtocolChoices.TCP],
        },
    ]

    bulk_update_data = {
        "description": "Test Item",
    }

    @classmethod
    def setUpTestData(cls):
        cls.items = (
            ApplicationItem(
                name="item-7",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-8",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-9",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-7",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
            ),
            Application(
                name="item-8",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
            ),
            Application(name="item-9"),
        )
        Application.objects.bulk_create(cls.applications)
        cls.applications[2].application_items.set([cls.items[0], cls.items[1]])


class ApplicationSetAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = ApplicationSet

    brief_fields = [
        "applications",
        "description",
        "display",
        "id",
        "name",
        "url",
    ]

    bulk_update_data = {
        "description": "Test Item",
    }

    @classmethod
    def setUpTestData(cls):
        cls.create_data = [
            {
                "name": "app-1",
            },
            {
                "name": "app-2",
            },
            {
                "name": "app-3",
            },
        ]

        cls.items = (
            ApplicationItem(
                name="item-7",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-8",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
            ApplicationItem(
                name="item-9",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-7",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
            ),
            Application(
                name="item-8",
                protocol=[ProtocolChoices.TCP],
                destination_ports=[1],
                source_ports=[1],
            ),
            Application(name="item-9"),
        )
        Application.objects.bulk_create(cls.applications)
        cls.applications[1].application_items.set([cls.items[0]])
        cls.applications[2].application_items.set([cls.items[1], cls.items[2]])
        cls.sets = (
            ApplicationSet(
                name="item-7",
            ),
            ApplicationSet(
                name="item-8",
            ),
            ApplicationSet(
                name="item-9",
            ),
        )
        ApplicationSet.objects.bulk_create(cls.sets)
        cls.sets[0].applications.set(
            [
                cls.applications[0],
            ]
        )
        cls.sets[1].applications.set(
            [
                cls.applications[0],
                cls.applications[1],
            ]
        )
        cls.sets[2].applications.set(
            [
                cls.applications[1],
                cls.applications[2],
            ]
        )
