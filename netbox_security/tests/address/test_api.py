from netaddr import IPNetwork
from utilities.testing import APIViewTestCases
from django.contrib.contenttypes.models import ContentType
from ipam.models import IPRange
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import Address, CustomPrefix


class AddressAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = Address

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

    @classmethod
    def setUpTestData(cls):
        cls.custom_prefixes = (
            CustomPrefix(prefix=IPNetwork("1.1.1.1/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.2/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.3/32")),
        )
        CustomPrefix.objects.bulk_create(cls.custom_prefixes)
        cls.ranges = (
            IPRange(
                start_address=IPNetwork("1.1.1.2/24"),
                end_address=IPNetwork("1.1.1.5/24"),
                status="active",
                size=4,
            ),
            IPRange(
                start_address=IPNetwork("1.1.2.2/24"),
                end_address=IPNetwork("1.1.2.5/24"),
                status="active",
                size=4,
            ),
            IPRange(
                start_address=IPNetwork("1.1.3.2/24"),
                end_address=IPNetwork("1.1.3.5/24"),
                status="active",
                size=4,
            ),
        )
        IPRange.objects.bulk_create(cls.ranges)

        addresses = (
            Address(
                name="address-7",
                assigned_object_id=cls.custom_prefixes[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
            ),
            Address(
                name="address-8",
                assigned_object_id=cls.custom_prefixes[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
            ),
            Address(
                name="address-9",
                assigned_object_id=cls.custom_prefixes[2].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
            ),
            Address(
                name="address-10",
                assigned_object_id=cls.ranges[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="iprange"
                ),
            ),
            Address(
                name="address-11",
                assigned_object_id=cls.ranges[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="iprange"
                ),
            ),
            Address(name="address-12", dns_name="test1.example.com"),
            Address(name="address-13", dns_name="test2.example.com"),
        )
        Address.objects.bulk_create(addresses)

        cls.create_data = [
            {
                "name": "address-1",
                "assigned_object_type": "netbox_security.customprefix",
                "assigned_object_id": cls.custom_prefixes[0].pk,
            },
            {
                "name": "address-2",
                "assigned_object_type": "netbox_security.customprefix",
                "assigned_object_id": cls.custom_prefixes[1].pk,
            },
            {
                "name": "address-3",
                "assigned_object_type": "ipam.iprange",
                "assigned_object_id": cls.ranges[0].pk,
            },
            {"name": "address-4", "dns_name": "test.example.com"},
            {"name": "address-5", "dns_name": "*.example.com"},
            {"name": "address-6", "dns_name": "example.com"},
        ]
