from django.test import TestCase
from netaddr import IPNetwork
from tenancy.models import Tenant, TenantGroup
from utilities.testing import ChangeLoggedFilterSetTestMixin

from netbox_security.models import (
    CustomPrefix,
)

from netbox_security.filtersets import (
    CustomPrefixFilterSet,
)
from netbox_security.tests.mixins import CustomPrefixMixin


class CustomPrefixFiterSetTestCase(
    CustomPrefixMixin, TestCase, ChangeLoggedFilterSetTestMixin
):
    queryset = CustomPrefix.objects.all()
    filterset = CustomPrefixFilterSet

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_prefix(self):
        params = {"prefix": ["1.1.1.1/32", "1.1.1.2/32"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant(self):
        params = {"tenant_id": [self.tenants[0].pk, self.tenants[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"tenant": [self.tenants[0].slug, self.tenants[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_tenant_group(self):
        params = {
            "tenant_group_id": [self.tenant_groups[0].pk, self.tenant_groups[1].pk]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {
            "tenant_group": [self.tenant_groups[0].slug, self.tenant_groups[1].slug]
        }
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
