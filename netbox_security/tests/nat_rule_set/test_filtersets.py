from django.test import TestCase
from utilities.testing import ChangeLoggedFilterSetTests

from netbox_security.models import NatRuleSet, NatRule
from netbox_security.filtersets import NatRuleSetFilterSet, NatRuleFilterSet
from netbox_security.choices import (
    RuleStatusChoices,
    AddressTypeChoices,
)


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


class NatRuleFiterSetTestCase(TestCase, ChangeLoggedFilterSetTests):
    queryset = NatRule.objects.all()
    filterset = NatRuleFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.rule_sets = (
            NatRuleSet(name="set-4"),
            NatRuleSet(name="set-5"),
            NatRuleSet(name="set-6"),
        )
        NatRuleSet.objects.bulk_create(cls.rule_sets)

        cls.rules = (
            NatRule(
                name="rule-1",
                rule_set=cls.rule_sets[0],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
            NatRule(
                name="rule-2",
                rule_set=cls.rule_sets[1],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
            NatRule(
                name="rule-3",
                rule_set=cls.rule_sets[2],
                source_type=AddressTypeChoices.STATIC,
                destination_type=AddressTypeChoices.STATIC,
                status=RuleStatusChoices.STATUS_ACTIVE,
            ),
        )
        NatRule.objects.bulk_create(cls.rules)

    def test_name(self):
        params = {"name": ["rule-1", "rule-2"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_filters(self):
        params = {"natrule_id": [self.rules[0].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natrule_id": [self.rules[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"natrule_id": [self.rules[2].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
