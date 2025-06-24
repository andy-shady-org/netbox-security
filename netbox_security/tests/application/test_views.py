from utilities.testing import ViewTestCases, create_tags

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import ApplicationItem, Application, ApplicationSet

from netbox_security.choices import ProtocolChoices


class ApplicationItemViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = ApplicationItem

    @classmethod
    def setUpTestData(cls):
        cls.items = (
            ApplicationItem(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-3",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "item-4",
            "destination_port": 1,
            "source_port": 1,
            "index": 1,
            "protocol": ProtocolChoices.TCP,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,index,protocol,destination_port,source_port",
            "item-5,1,tcp,1,2",
            "item-6,2,tcp,2,1",
            "item-7,3,udp,1,2",
        )

        cls.csv_update_data = (
            "id,name,protocol,description",
            f"{cls.items[0].pk},item-8,tcp,test1",
            f"{cls.items[1].pk},item-9,udp,test2",
            f"{cls.items[2].pk},item-10,tcp,test3",
        )


class ApplicationViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = Application

    @classmethod
    def setUpTestData(cls):
        cls.items = (
            ApplicationItem(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-3",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
            ),
            Application(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
            ),
            Application(
                name="item-3",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
            ),
        )
        Application.objects.bulk_create(cls.applications)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "item-4",
            "destination_port": 1,
            "source_port": 1,
            "protocol": ProtocolChoices.TCP,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,application_items,protocol,destination_port,source_port",
            f'item-5,"{cls.items[0].name},{cls.items[1].name}",tcp,1,2',
            "item-6,,tcp,2,1",
            "item-7,,udp,1,2",
        )

        cls.csv_update_data = (
            "id,name,protocol,description",
            f"{cls.applications[0].pk},item-8,tcp,test1",
            f"{cls.applications[1].pk},item-9,udp,test2",
            f"{cls.applications[2].pk},item-10,tcp,test3",
        )


class ApplicationSetViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = ApplicationSet

    @classmethod
    def setUpTestData(cls):
        cls.items = (
            ApplicationItem(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
            ApplicationItem(
                name="item-3",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
                index=1,
            ),
        )
        ApplicationItem.objects.bulk_create(cls.items)

        cls.applications = (
            Application(
                name="item-1",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
            ),
            Application(
                name="item-2",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
            ),
            Application(
                name="item-3",
                protocol=ProtocolChoices.TCP,
                destination_port=1,
                source_port=1,
            ),
        )
        Application.objects.bulk_create(cls.applications)

        cls.application_sets = (
            ApplicationSet(name="item-1"),
            ApplicationSet(
                name="item-2",
            ),
            ApplicationSet(
                name="item-3",
            ),
        )
        ApplicationSet.objects.bulk_create(cls.application_sets)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "item-4",
            "applications": [
                cls.applications[0].pk,
                cls.applications[1].pk,
                cls.applications[2].pk,
            ],
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,applications",
            f'item-5,"{cls.applications[0].name},{cls.applications[1].name}"',
            f'item-6,"{cls.applications[1].name},{cls.applications[2].name}"',
            f'item-7,"{cls.applications[0].name},{cls.applications[2].name}"',
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.application_sets[0].pk},item-8,test1",
            f"{cls.application_sets[1].pk},item-9,test2",
            f"{cls.application_sets[2].pk},item-10,test3",
        )
