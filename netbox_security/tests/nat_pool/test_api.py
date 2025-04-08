from utilities.testing import APIViewTestCases
from netbox_security.tests.custom import APITestCase, NetBoxSecurityGraphQLMixin
from netbox_security.models import NatPool
from ipam.choices import IPAddressStatusChoices
from netbox_security.choices import (
    PoolTypeChoices,
)


class NatPoolAPITestCase(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
    NetBoxSecurityGraphQLMixin,
    APIViewTestCases.GraphQLTestCase,
):
    model = NatPool

    brief_fields = [
        "description",
        "display",
        "id",
        "member_count",
        "name",
        "pool_type",
        "status",
        "url",
    ]

    create_data = [
        {
            "name": "pool-1",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
        {
            "name": "pool-2",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
        {
            "name": "pool-3",
            "pool_type": PoolTypeChoices.ADDRESS,
            "status": IPAddressStatusChoices.STATUS_ACTIVE,
        },
    ]

    bulk_update_data = {
        "description": "Test Nat Pool",
    }

    @classmethod
    def setUpTestData(cls):
        filters = (
            NatPool(
                name="pool-4",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-5",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
            NatPool(
                name="pool-6",
                pool_type=PoolTypeChoices.ADDRESS,
                status=IPAddressStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatPool.objects.bulk_create(filters)
