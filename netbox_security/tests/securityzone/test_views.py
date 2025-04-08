from utilities.testing import ViewTestCases, create_tags
from django.contrib.contenttypes.models import ContentType

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import SecurityZone, SecurityZonePolicy, Address, AddressList


class SecurityZoneViewTestCase(
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
    model = SecurityZone

    @classmethod
    def setUpTestData(cls):
        cls.zones = (
            SecurityZone(name="DMZ"),
            SecurityZone(name="INTERNAL"),
            SecurityZone(name="PUBLIC"),
        )
        SecurityZone.objects.bulk_create(cls.zones)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "TEST-ZONE1",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name",
            "TEST-ZONE2",
            "TEST-ZONE3",
            "TEST-ZONE4",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.zones[0].pk},TEST-ZONE5,test1",
            f"{cls.zones[1].pk},TEST-ZONE6,test2",
            f"{cls.zones[2].pk},TEST-ZONE7,test3",
        )

    maxDiff = None


class SecurityZonePolicyViewTestCase(
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
    model = SecurityZonePolicy

    @classmethod
    def setUpTestData(cls):
        cls.zones = (
            SecurityZone(name="DMZ"),
            SecurityZone(name="INTERNAL"),
            SecurityZone(name="PUBLIC"),
        )
        SecurityZone.objects.bulk_create(cls.zones)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.addresses = (
            Address(name="address-1", value="1.1.1.1/32"),
            Address(name="address-2", value="1.1.1.2/32"),
            Address(name="address-3", value="1.1.1.3/32"),
            Address(name="address-4", value="1.1.1.4/32"),
        )
        Address.objects.bulk_create(cls.addresses)

        cls.source_addresses = (
            AddressList(name="address-list-1", assigned_object_id=cls.addresses[0].pk, assigned_object_type=ContentType.objects.get(app_label='netbox_security', model='address')),
            AddressList(name="address-list-2", assigned_object_id=cls.addresses[1].pk, assigned_object_type=ContentType.objects.get(app_label='netbox_security', model='address'))
        )
        AddressList.objects.bulk_create(cls.source_addresses)

        cls.destination_addresses = (
            AddressList(name="address-list-3", assigned_object_id=cls.addresses[2].pk, assigned_object_type=ContentType.objects.get(app_label='netbox_security', model='address')),
            AddressList(name="address-list-4", assigned_object_id=cls.addresses[3].pk, assigned_object_type=ContentType.objects.get(app_label='netbox_security', model='address')),
        )
        AddressList.objects.bulk_create(cls.destination_addresses)

        cls.policies = (
            SecurityZonePolicy(name="policy-1", index=5,
                               source_zone=cls.zones[0],
                               destination_zone=cls.zones[1],
                               actions=["permit", "count", "log"],
                               application=['test-1', 'test-2']),
            SecurityZonePolicy(name="policy-2", index=6,
                               source_zone=cls.zones[0],
                               destination_zone=cls.zones[1],
                               actions=["permit", "count", "log"],
                               application=['test-1', 'test-2']),
            SecurityZonePolicy(name="policy-3", index=7,
                               source_zone=cls.zones[0],
                               destination_zone=cls.zones[1],
                               actions=["permit", "count", "log"],
                               application=['test-1', 'test-2']),
        )
        SecurityZonePolicy.objects.bulk_create(cls.policies)
        for policy in cls.policies:
            policy.source_address.set(cls.source_addresses)
            policy.destination_address.set(cls.destination_addresses)

        cls.form_data = {
            "name": "TEST-POLICY1",
            "index": 10,
            "source_zone": cls.zones[0].pk,
            "destination_zone": cls.zones[1].pk,
            "source_address": [cls.source_addresses[0].pk, cls.source_addresses[1].pk],
            "destination_address": [cls.destination_addresses[0].pk, cls.destination_addresses[1].pk],
            "actions": ["permit", "count", "log"],
            "application": "test-1,test-2",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,index,source_zone,destination_zone,actions,application",
            f'TEST-POLICY4,1,{cls.zones[0].name},{cls.zones[1].name},"permit,count","test-1,test-2"',
            f'TEST-POLICY5,2,{cls.zones[0].name},{cls.zones[1].name},"permit,count","test-1,test-2"',
            f'TEST-POLICY6,3,{cls.zones[0].name},{cls.zones[1].name},"permit,count","test-1,test-2"',
        )

        cls.csv_update_data = (
            "id,description",
            f"{cls.policies[0].pk},test1",
            f"{cls.policies[1].pk},test2",
            f"{cls.policies[2].pk},test3",
        )

    maxDiff = None
