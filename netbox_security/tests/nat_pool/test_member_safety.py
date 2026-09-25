from types import SimpleNamespace

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from netaddr import IPNetwork
from ipam.models import IPAddress, IPRange, Prefix, VRF
from tenancy.models import Tenant
from users.models import ObjectPermission
from utilities.forms import restrict_form_fields
from virtualization.models import VirtualMachine, VMInterface

from netbox_security.api.serializers_.nat_pool_member import NatPoolMemberSerializer
from netbox_security.forms import NatPoolMemberImportForm
from netbox_security.models import NatPool, NatPoolMember


class NatPoolMemberSafetyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username="nat-reference")
        cls.pool = NatPool.objects.create(name="portable-pool")
        cls.vrf = VRF.objects.create(name="customer", rd="65000:1")
        cls.tenant = Tenant.objects.create(name="customer", slug="customer")
        cls.global_ip = IPAddress.objects.create(
            address=IPNetwork("192.0.2.1/24"), status="reserved"
        )
        cls.scoped_ip = IPAddress.objects.create(
            address=IPNetwork("192.0.2.1/24"),
            vrf=cls.vrf,
            tenant=cls.tenant,
            status="reserved",
        )
        cls.prefix = Prefix.objects.create(
            prefix=IPNetwork("192.0.2.0/24"), status="reserved"
        )
        cls.ip_range = IPRange.objects.create(
            start_address=IPNetwork("192.0.2.2/24"),
            end_address=IPNetwork("192.0.2.10/24"),
            status="reserved",
        )
        cls.vm = VirtualMachine.objects.create(name="nat-safety")
        cls.interface = VMInterface.objects.create(virtual_machine=cls.vm, name="eth0")
        cls.global_ip.assigned_object = cls.interface
        cls.global_ip.save()
        cls.vm.primary_ip4 = cls.global_ip
        cls.vm.save()
        permission = ObjectPermission.objects.create(
            name="reference-view", actions=["view"]
        )
        permission.object_types.set(
            ContentType.objects.get_for_models(
                IPAddress, Prefix, IPRange, VRF, Tenant, NatPool
            ).values()
        )
        permission.users.add(cls.user)

    def import_form(self, **values):
        form = NatPoolMemberImportForm(
            data={
                "name": "member",
                "pool": self.pool.name,
                "status": "active",
                **values,
            }
        )
        restrict_form_fields(form, self.user)
        return form

    def grant_change_permission(self):
        permission = ObjectPermission.objects.create(
            name="reference-change", actions=["change"]
        )
        permission.object_types.set(
            ContentType.objects.get_for_models(IPAddress, Prefix, IPRange).values()
        )
        permission.users.add(self.user)

    def test_text_import_selects_global_or_named_scope(self):
        for context, expected in (
            ({}, self.global_ip),
            ({"vrf": "customer", "tenant": "customer"}, self.scoped_ip),
        ):
            with self.subTest(context=context):
                form = self.import_form(address="192.0.2.1/24", **context)
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["address"], expected)

    def test_ambiguous_missing_and_invalid_scope_are_rejected(self):
        IPAddress.objects.create(address=IPNetwork("192.0.2.1/24"))
        for values in (
            {"address": "192.0.2.1/24"},
            {"address": "198.51.100.1/24"},
            {"address": "192.0.2.1/24", "vrf": "missing"},
        ):
            with self.subTest(values=values):
                self.assertFalse(self.import_form(**values).is_valid())

    def test_range_end_disambiguates_text(self):
        IPRange.objects.create(
            start_address=IPNetwork("192.0.2.2/24"),
            end_address=IPNetwork("192.0.2.20/24"),
        )
        self.assertFalse(self.import_form(address_range="192.0.2.2/24").is_valid())
        form = self.import_form(
            address_range="192.0.2.2/24", address_range_end="192.0.2.10/24"
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["address_range"], self.ip_range)

    def test_inaccessible_target_is_rejected(self):
        self.user = get_user_model().objects.create(username="no-ipam-view")
        form = self.import_form(address="192.0.2.1/24")
        self.assertFalse(form.is_valid())
        self.assertIn("address", form.errors)

    def test_api_validation_create_and_edit_preserve_ipam(self):
        for field, obj in (
            ("address", self.global_ip),
            ("prefix", self.prefix),
            ("address_range", self.ip_range),
        ):
            with self.subTest(field=field):
                before = type(obj).objects.filter(pk=obj.pk).values().get()
                serializer = NatPoolMemberSerializer(
                    data={
                        "name": field,
                        "pool": self.pool.pk,
                        field: obj.pk,
                    },
                    context={"request": SimpleNamespace(user=self.user)},
                )
                self.assertTrue(serializer.is_valid(), serializer.errors)
                self.assertEqual(
                    type(obj).objects.filter(pk=obj.pk).values().get(), before
                )
                member = serializer.save()
                serializer = NatPoolMemberSerializer(
                    member,
                    data={"description": "edited"},
                    partial=True,
                    context={"request": SimpleNamespace(user=self.user)},
                )
                self.assertTrue(serializer.is_valid(), serializer.errors)
                serializer.save()
                self.assertEqual(
                    type(obj).objects.filter(pk=obj.pk).values().get(), before
                )
        self.vm.refresh_from_db()
        self.assertEqual(self.vm.primary_ip4_id, self.global_ip.pk)

    def test_import_save_preserves_assignment(self):
        form = self.import_form(address="192.0.2.1/24")
        self.assertTrue(form.is_valid(), form.errors)
        member = form.save()
        self.global_ip.refresh_from_db()
        self.assertEqual(member.address_id, self.global_ip.pk)
        self.assertEqual(self.global_ip.assigned_object, self.interface)
        self.assertEqual(self.global_ip.status, "reserved")
        self.assertEqual(NatPoolMember.objects.count(), 1)

    def test_import_save_updates_status_when_user_can_change_target(self):
        self.grant_change_permission()
        form = self.import_form(address="192.0.2.1/24", status="deprecated")
        form.request_user = self.user
        self.assertTrue(form.is_valid(), form.errors)

        member = form.save()

        self.global_ip.refresh_from_db()
        self.assertEqual(member.status, "deprecated")
        self.assertEqual(self.global_ip.status, "deprecated")
        self.assertEqual(self.global_ip.assigned_object, self.interface)

    def test_tenant_disambiguates_and_prefix_text_is_supported(self):
        IPAddress.objects.create(address=IPNetwork("192.0.2.1/24"), vrf=self.vrf)
        self.assertFalse(
            self.import_form(address="192.0.2.1/24", vrf="customer").is_valid()
        )
        form = self.import_form(
            address="192.0.2.1/24", vrf="customer", tenant="customer"
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["address"], self.scoped_ip)
        form = self.import_form(prefix="192.0.2.0/24")
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["prefix"], self.prefix)

    def test_scoped_prefix_and_range_text_resolution(self):
        scoped_prefix = Prefix.objects.create(
            prefix=IPNetwork("198.51.100.0/24"), vrf=self.vrf, tenant=self.tenant
        )
        scoped_range = IPRange.objects.create(
            start_address=IPNetwork("198.51.100.10/24"),
            end_address=IPNetwork("198.51.100.20/24"),
            vrf=self.vrf,
            tenant=self.tenant,
        )

        form = self.import_form(
            prefix="198.51.100.0/24",
            vrf="customer",
            tenant="customer",
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["prefix"], scoped_prefix)

        form = self.import_form(
            address_range="198.51.100.10/24",
            address_range_end="198.51.100.20/24",
            vrf="customer",
            tenant="customer",
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["address_range"], scoped_range)

    def test_api_validation_updates_ipam_status_when_user_can_change_target(self):
        self.grant_change_permission()

        for field, obj in (
            ("address", self.global_ip),
            ("prefix", self.prefix),
            ("address_range", self.ip_range),
        ):
            with self.subTest(field=field):
                serializer = NatPoolMemberSerializer(
                    data={
                        "name": f"{field}-sync",
                        "pool": self.pool.pk,
                        "status": "deprecated",
                        field: obj.pk,
                    },
                    context={"request": SimpleNamespace(user=self.user)},
                )
                self.assertTrue(serializer.is_valid(), serializer.errors)

                member = serializer.save()
                obj.refresh_from_db()
                self.assertEqual(member.status, "deprecated")
                self.assertEqual(obj.status, "deprecated")

                serializer = NatPoolMemberSerializer(
                    member,
                    data={"status": "active"},
                    partial=True,
                    context={"request": SimpleNamespace(user=self.user)},
                )
                self.assertTrue(serializer.is_valid(), serializer.errors)
                serializer.save()

                obj.refresh_from_db()
                self.assertEqual(obj.status, "active")

        self.global_ip.refresh_from_db()
        self.assertEqual(self.global_ip.assigned_object, self.interface)

    def test_invalid_range_end_is_a_form_error(self):
        form = self.import_form(
            address_range="192.0.2.2/24", address_range_end="invalid"
        )
        self.assertFalse(form.is_valid())
        self.assertIn("address_range_end", form.errors)

    def test_prefix_and_range_reject_ipaddress_only_statuses(self):
        for values in (
            {"name": "prefix-invalid", "pool": self.pool.pk, "prefix": self.prefix.pk},
            {
                "name": "range-invalid",
                "pool": self.pool.pk,
                "address_range": self.ip_range.pk,
            },
        ):
            with self.subTest(values=values):
                serializer = NatPoolMemberSerializer(
                    data={**values, "status": "dhcp"},
                    context={"request": SimpleNamespace(user=self.user)},
                )
                self.assertFalse(serializer.is_valid())
                self.assertIn("status", serializer.errors)

