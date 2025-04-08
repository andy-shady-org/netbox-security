from django.test import TestCase
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import NatPool
from netbox_security.filtersets import NatPoolFilterSet


class NatPoolFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatPool.objects.all()
    filterset = NatPoolFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.pools = (
            NatPool(name="pool-4"),
            NatPool(name="pool-5"),
            NatPool(name="pool-6"),
        )
        for item in cls.pools:
            item.save()

    def test_name(self):
        params = {"name": ["pool-4", "pool-5"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filters(self):
        params = {"natpool_id": [self.pools[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natpool_id": [self.pools[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natpool_id": [self.pools[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
