from utilities.testing import ViewTestCases, create_tags
from ipam.choices import IPAddressStatusChoices

from netbox_security.tests.custom import ModelViewTestCase
from netbox_security.models import NatPool
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
            NatPool(name="pool-1", pool_type=PoolTypeChoices.ADDRESS, status=IPAddressStatusChoices.STATUS_ACTIVE),
            NatPool(name="pool-2", pool_type=PoolTypeChoices.ADDRESS, status=IPAddressStatusChoices.STATUS_ACTIVE),
            NatPool(name="pool-3", pool_type=PoolTypeChoices.ADDRESS, status=IPAddressStatusChoices.STATUS_ACTIVE),
        )
        NatPool.objects.bulk_create(cls.pools)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "pool-4", "pool_type": "address", "status": "active",
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
