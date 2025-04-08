from django.test import TestCase
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import NatRuleSet
from netbox_security.filtersets import NatRuleSetFilterSet


class NatRuleSetFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatRuleSet.objects.all()
    filterset = NatRuleSetFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.rules = (
            NatRuleSet(name="set-4"),
            NatRuleSet(name="set-5"),
            NatRuleSet(name="set-6"),
        )
        for item in cls.rules:
            item.save()

    def test_name(self):
        params = {"name": ["set-4", "set-5"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filters(self):
        params = {"natruleset_id": [self.rules[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natruleset_id": [self.rules[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natruleset_id": [self.rules[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
