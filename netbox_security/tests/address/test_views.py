from netaddr import IPNetwork
from utilities.testing import ViewTestCases, create_tags
from ipam.models import IPRange, Prefix, IPAddress
from tenancy.models import Tenant, TenantGroup
from django.contrib.contenttypes.models import ContentType

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import Address, CustomPrefix


class AddressViewTestCase(
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
    model = Address

    @classmethod
    def setUpTestData(cls):
        cls.tenant_groups = (
            TenantGroup(name="Tenant group 1", slug="tenant-group-1"),
            TenantGroup(name="Tenant group 2", slug="tenant-group-2"),
            TenantGroup(name="Tenant group 3", slug="tenant-group-3"),
        )
        for tenantgroup in cls.tenant_groups:
            tenantgroup.save()

        cls.tenants = (
            Tenant(name="Tenant 1", slug="tenant-1", group=cls.tenant_groups[0]),
            Tenant(name="Tenant 2", slug="tenant-2", group=cls.tenant_groups[1]),
            Tenant(name="Tenant 3", slug="tenant-3", group=cls.tenant_groups[2]),
        )
        Tenant.objects.bulk_create(cls.tenants)

        cls.custom_prefixes = (
            CustomPrefix(prefix=IPNetwork("1.1.1.1/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.2/32")),
            CustomPrefix(prefix=IPNetwork("1.1.1.3/32")),
        )
        CustomPrefix.objects.bulk_create(cls.custom_prefixes)
        cls.prefixes = (
            Prefix(
                prefix="1.1.1.0/24",
                status="active",
            ),
            Prefix(
                prefix="1.1.2.0/24",
                status="active",
            ),
            Prefix(
                prefix="1.1.3.0/24",
                status="active",
            ),
        )
        Prefix.objects.bulk_create(cls.prefixes)

        cls.ip_addresses = (
            IPAddress(
                address="1.1.1.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.2.1/24",
                status="active",
            ),
            IPAddress(
                address="1.1.3.1/24",
                status="active",
            ),
        )
        IPAddress.objects.bulk_create(cls.ip_addresses)
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

        cls.addresses = (
            Address(
                name="address-1",
                assigned_object_id=cls.custom_prefixes[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
                tenant=cls.tenants[0],
            ),
            Address(
                name="address-2",
                assigned_object_id=cls.custom_prefixes[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
                tenant=cls.tenants[1],
            ),
            Address(
                name="address-3",
                assigned_object_id=cls.custom_prefixes[2].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="netbox_security", model="customprefix"
                ),
                tenant=cls.tenants[2],
            ),
            Address(
                name="address-4",
                assigned_object_id=cls.ranges[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="iprange"
                ),
                tenant=cls.tenants[2],
            ),
            Address(
                name="address-5",
                assigned_object_id=cls.ranges[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="iprange"
                ),
                tenant=cls.tenants[2],
            ),
            Address(
                name="address-6",
                assigned_object_id=cls.prefixes[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="prefix"
                ),
                tenant=cls.tenants[2],
            ),
            Address(
                name="address-7",
                assigned_object_id=cls.prefixes[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="prefix"
                ),
                tenant=cls.tenants[2],
            ),
            Address(
                name="address-8",
                assigned_object_id=cls.ip_addresses[0].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="ipaddress"
                ),
                tenant=cls.tenants[2],
            ),
            Address(
                name="address-9",
                assigned_object_id=cls.ip_addresses[1].pk,
                assigned_object_type=ContentType.objects.get(
                    app_label="ipam", model="ipaddress"
                ),
                tenant=cls.tenants[2],
            ),
            Address(
                name="address-10", dns_name="test.example.com", tenant=cls.tenants[2]
            ),
        )
        for address in cls.addresses:
            address.save()

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "address-5",
            "identifier": "xyz",
            "ipam_prefix": cls.prefixes[0].pk,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,identifier,dns_name",
            "address-10,bil,test2.example.com",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.addresses[0].pk},address-12,test1",
            f"{cls.addresses[1].pk},address-13,test2",
            f"{cls.addresses[2].pk},address-14,test3",
        )

    maxDiff = None
