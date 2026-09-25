from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from netaddr import IPNetwork
from ipam.models import IPAddress, IPRange, Prefix, VRF
from users.models import ObjectPermission

from netbox_security.models import Address, CustomPrefix
from netbox_security.utils.address_set_hierarchy import get_address_set_hierarchy


class RoutingContextTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="routing-context", is_superuser=True
        )
        cls.vrf_a = VRF.objects.create(name="A", rd="65000:1")
        cls.vrf_b = VRF.objects.create(name="B", rd="65000:2")
        cls.target = CustomPrefix.objects.create(prefix="192.0.2.1/32")
        cls.parent = CustomPrefix.objects.create(prefix="192.0.2.0/24")
        cls.direct = cls.make_address("direct", cls.target)
        cls.definition = cls.make_address("definition", cls.parent)
        cls.scoped_ids = {}
        cls.hosts = {}
        for vrf in (None, cls.vrf_a, cls.vrf_b):
            key = vrf.pk if vrf else None
            objects = [
                Prefix.objects.create(prefix="192.0.2.0/24", vrf=vrf),
                IPAddress.objects.create(address="192.0.2.1/32", vrf=vrf),
                IPRange.objects.create(
                    start_address=IPNetwork("192.0.2.1/32"),
                    end_address=IPNetwork("192.0.2.10/32"),
                    vrf=vrf,
                ),
            ]
            cls.hosts[key] = objects[1]
            cls.scoped_ids[key] = {
                cls.make_address(f"{key}-{obj._meta.model_name}", obj).pk
                for obj in objects
            }

    @staticmethod
    def make_address(name, obj):
        return Address.objects.create(
            name=name,
            assigned_object_type=ContentType.objects.get_for_model(obj),
            assigned_object_id=obj.pk,
        )

    def context(self, obj=None, **kwargs):
        obj = obj or self.target
        return get_address_set_hierarchy(
            user=self.user,
            app_label=obj._meta.app_label,
            model=obj._meta.model_name,
            object_id=obj.pk,
            **kwargs,
        )

    def test_explicit_context_isolates_all_ipam_models(self):
        for vrf_id, expected in self.scoped_ids.items():
            with self.subTest(vrf_id=vrf_id):
                result = self.context(routing_vrf_id=vrf_id)
                self.assertEqual(
                    set(result["inherited_address_ids"]),
                    expected | {self.definition.pk},
                )
                self.assertTrue(result["routing_context_known"])
                self.assertEqual(result["routing_vrf_id"], vrf_id)

    def test_unknown_context_retains_address_book_only(self):
        result = self.context()
        self.assertEqual(result["address_ids"], [self.direct.pk])
        self.assertEqual(result["inherited_address_ids"], [self.definition.pk])
        self.assertFalse(result["routing_context_known"])
        self.assertIsNone(result["routing_vrf_id"])

    def test_ipam_context_is_authoritative_and_definitions_are_reusable(self):
        for vrf_id, host in self.hosts.items():
            with self.subTest(vrf_id=vrf_id):
                result = self.context(host, routing_vrf_id=self.vrf_b.pk)
                self.assertEqual(result["routing_vrf_id"], vrf_id)
                self.assertTrue(result["routing_context_known"])
                inherited = set(result["inherited_address_ids"])
                self.assertIn(self.definition.pk, inherited)
                self.assertTrue(inherited & self.scoped_ids[vrf_id])
                for other_vrf, ids in self.scoped_ids.items():
                    if other_vrf != vrf_id:
                        self.assertFalse(inherited & ids)

    def test_hidden_ipam_targets_are_excluded(self):
        self.user = get_user_model().objects.create_user(username="restricted-routing")
        permission = ObjectPermission.objects.create(
            name="address-book-only", actions=["view"]
        )
        permission.object_types.set(
            ContentType.objects.get_for_models(Address, CustomPrefix).values()
        )
        permission.users.add(self.user)
        result = self.context(routing_vrf_id=self.vrf_a.pk)
        self.assertEqual(result["inherited_address_ids"], [self.definition.pk])

    def test_empty_and_missing_targets_report_context(self):
        empty = CustomPrefix.objects.create(prefix="203.0.113.0/24")
        result = self.context(empty, routing_vrf_id=None)
        self.assertTrue(result["routing_context_known"])
        self.assertEqual(result["inherited_address_ids"], [])
        result = get_address_set_hierarchy(
            user=self.user,
            app_label="netbox_security",
            model="customprefix",
            object_id=0,
            routing_vrf_id=self.vrf_a.pk,
        )
        self.assertFalse(result["routing_context_known"])
        self.assertIsNone(result["routing_vrf_id"])
