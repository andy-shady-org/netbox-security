from utilities.testing import ViewTestCases, create_tags
from netbox_security.tests.custom import ModelViewTestCase

from ipam.models import IPAddress, Prefix, IPRange
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import NatPool, NatPoolMember
from netbox_security.choices import PoolTypeChoices


class NatPoolViewTestCase(
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
    model = NatPool

    @classmethod
    def setUpTestData(cls):
        cls.pools = (
            NatPool(
                name="pool-1",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-2",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-3",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatPool.objects.bulk_create(cls.pools)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "pool-4",
            "pool_type": "address",
            "status": "active",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "description": "New Description",
        }

        cls.csv_data = (
            "name,pool_type,status",
            "pool-5,address,active",
            "pool-6,address,active",
            "pool-7,address,active",
        )

        cls.csv_update_data = (
            "id,name,pool_type,status,description",
            f"{cls.pools[0].pk},pool-8,address,active,test1",
            f"{cls.pools[1].pk},pool-9,address,active,test2",
            f"{cls.pools[2].pk},pool-10,address,active,test3",
        )

    maxDiff = None


class NatPoolMemberViewTestCase(
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
    model = NatPoolMember

    @classmethod
    def setUpTestData(cls):
        cls.pools = (
            NatPool(
                name="pool-1",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-2",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-3",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatPool.objects.bulk_create(cls.pools)

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

        cls.addresses = (
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
        IPAddress.objects.bulk_create(cls.addresses)

        cls.ranges = (
            IPRange(
                start_address="1.1.1.2/24",
                end_address="1.1.1.5/24",
                status="active",
                size=4
            ),
            IPRange(
                start_address="1.1.2.2/24",
                end_address="1.1.2.5/24",
                status="active",
                size=4
            ),
            IPRange(
                start_address="1.1.3.2/24",
                end_address="1.1.3.5/24",
                status="active",
                size=4
            ),
        )
        IPRange.objects.bulk_create(cls.ranges)

        cls.members = (
            NatPoolMember(
                name="member-1",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                prefix=cls.prefixes[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            NatPoolMember(
                name="member-2",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                address=cls.addresses[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
            NatPoolMember(
                name="member-3",
                pool=cls.pools[0],
                status=IPAddressStatusChoices.STATUS_ACTIVE,
                address_range=cls.ranges[0],
                source_ports=[1, 2, 3],
                destination_ports=[4, 5, 6],
            ),
        )
        NatPoolMember.objects.bulk_create(cls.members)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "member-4",
            "pool": cls.pools[0].pk,
            "status": "active",
            "address": cls.addresses[0].pk,
            "source_ports": "1,2,3",
            "destination_ports": "4,5,6",
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "status": IPAddressStatusChoices.STATUS_RESERVED
        }

        cls.csv_data = (
            "name,pool,status,address,prefix,address_range,source_ports,destination_ports",
            'member-5,pool-1,active,1.1.1.1/24,,,"1,2,3","4,5,6"',
            'member-6,pool-2,active,,1.1.2.0/24,,"4,5,6","7,8,9"',
            'member-7,pool-3,active,,,1.1.3.2/24,"5,6,7","8,9,10"',
        )

        cls.csv_update_data = (
            "id,status",
            f"{cls.members[0].pk},active",
            f"{cls.members[1].pk},active",
            f"{cls.members[2].pk},active",
        )

    maxDiff = None
