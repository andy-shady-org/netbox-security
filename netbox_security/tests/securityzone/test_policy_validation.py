from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import transaction
from django.test import RequestFactory

from netbox_security.forms import (
    SecurityZonePolicyBulkEditForm,
    SecurityZonePolicyForm,
    SecurityZonePolicyImportForm,
)
from netbox_security.models import (
    Address,
    AddressList,
    SecurityZone,
    SecurityZonePolicy,
)
from netbox_security.tests.custom import APITestCase
from netbox_security.views.security_zone_policy import SecurityZonePolicyBulkEditView


class SecurityZonePolicyValidationTestCase(APITestCase):
    model = SecurityZonePolicy
    user_permissions = (
        "netbox_security.view_securityzonepolicy",
        "netbox_security.change_securityzonepolicy",
        "netbox_security.view_securityzone",
        "netbox_security.view_address",
        "netbox_security.view_addresslist",
    )

    @classmethod
    def setUpTestData(cls):
        cls.source_zone = SecurityZone.objects.create(name="validation-source")
        cls.destination_zone = SecurityZone.objects.create(
            name="validation-destination"
        )
        cls.intra_zone = SecurityZone.objects.create(
            name="validation-intra", allow_intra_zone=True
        )
        address_type = ContentType.objects.get_for_model(Address)
        cls.addresses = []
        for index in range(2):
            address = Address.objects.create(
                name=f"validation-address-{index}", dns_name=f"host{index}.example.com"
            )
            cls.addresses.append(
                AddressList.objects.create(
                    name=f"validation-list-{index}",
                    assigned_object_type=address_type,
                    assigned_object_id=address.pk,
                )
            )
        cls.policy = SecurityZonePolicy.objects.create(
            name="validation-policy",
            index=1,
            source_zone=cls.source_zone,
            destination_zone=cls.destination_zone,
            policy_actions=["permit"],
        )
        cls.policy.source_address.set([cls.addresses[0]])
        cls.policy.destination_address.set([cls.addresses[1]])

    def test_new_policy_checks_pending_overlap(self):
        policy = SecurityZonePolicy(
            name="new-policy",
            index=2,
            source_zone=self.source_zone,
            destination_zone=self.destination_zone,
            policy_actions=["permit"],
        )
        policy._m2m_values = {
            "source_address": [self.addresses[0]],
            "destination_address": [self.addresses[0]],
        }
        with self.assertRaises(ValidationError) as error:
            policy.full_clean()
        self.assertIn("source_address", error.exception.message_dict)
        policy.source_zone = policy.destination_zone = self.intra_zone
        policy.full_clean()

    def test_saved_overlap_is_checked_without_pending_values(self):
        self.policy.destination_address.set([self.addresses[0]])
        with self.assertRaises(ValidationError):
            self.policy.full_clean()

    def test_pending_primary_keys_and_explicit_clear(self):
        self.policy._m2m_values = {"source_address": [self.addresses[1].pk]}
        with self.assertRaises(ValidationError):
            self.policy.full_clean()
        self.policy._m2m_values["destination_address"] = []
        self.policy.full_clean()

    def test_edit_form_uses_proposed_zones_and_addresses(self):
        data = {
            "name": self.policy.name,
            "index": self.policy.index,
            "source_zone": self.source_zone.pk,
            "destination_zone": self.destination_zone.pk,
            "source_address": [self.addresses[0].pk],
            "destination_address": [self.addresses[0].pk],
            "policy_actions": ["permit"],
        }
        form = SecurityZonePolicyForm(data=data, instance=self.policy)
        self.assertFalse(form.is_valid())
        self.assertIn("source_address", form.errors)
        data.update(source_zone=self.intra_zone.pk, destination_zone=self.intra_zone.pk)
        form = SecurityZonePolicyForm(data=data, instance=self.policy)
        self.assertTrue(form.is_valid(), form.errors)

    def partial_import(self, data):
        form = SecurityZonePolicyImportForm(data=data, instance=self.policy)
        # Match BulkImportView's treatment of omitted columns on updates.
        for name in list(form.fields):
            if name not in data:
                del form.fields[name]
        return form

    def test_partial_import_checks_omitted_destination(self):
        form = self.partial_import({"source_address": self.addresses[1].name})
        self.assertFalse(form.is_valid())
        self.assertIn("source_address", form.errors)
        self.assertEqual(list(self.policy.source_address.all()), [self.addresses[0]])

    def test_partial_import_preserves_omitted_fields(self):
        form = self.partial_import({"description": "updated"})
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(list(self.policy.source_address.all()), [self.addresses[0]])
        self.assertEqual(
            list(self.policy.destination_address.all()), [self.addresses[1]]
        )

    def test_partial_import_zone_change_checks_saved_overlap(self):
        self.policy.source_zone = self.policy.destination_zone = self.intra_zone
        self.policy.save()
        self.policy.destination_address.set([self.addresses[0]])
        form = self.partial_import({"destination_zone": self.destination_zone.name})
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_patch_checks_omitted_side_and_accepts_explicit_clear(self):
        url = self._get_detail_url(self.policy)
        data = {"source_address": [self.addresses[1].pk]}
        response = self.client.patch(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 400)
        self.assertIn("source_address", response.data)
        self.assertEqual(list(self.policy.source_address.all()), [self.addresses[0]])
        data["destination_address"] = []
        response = self.client.patch(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 200)
        self.assertEqual(list(self.policy.source_address.all()), [self.addresses[1]])
        self.assertFalse(self.policy.destination_address.exists())

    def test_patch_null_preserves_selection(self):
        response = self.client.patch(
            self._get_detail_url(self.policy),
            {"source_address": None},
            format="json",
            **self.header,
        )
        self.assertHttpStatus(response, 200)
        self.assertEqual(list(self.policy.source_address.all()), [self.addresses[0]])
        response = self.client.patch(
            self._get_detail_url(self.policy),
            {"source_address": [self.addresses[1].pk], "destination_address": None},
            format="json",
            **self.header,
        )
        self.assertHttpStatus(response, 400)
        self.assertIn("source_address", response.data)

    def test_bulk_edit_validates_each_policy_and_rolls_back(self):
        other = SecurityZonePolicy.objects.create(
            name="second-policy",
            index=2,
            source_zone=self.source_zone,
            destination_zone=self.destination_zone,
            policy_actions=["permit"],
        )
        other.destination_address.set([self.addresses[0]])
        data = {
            "pk": [self.policy.pk, other.pk],
            "description": "must-roll-back",
            "source_address": [self.addresses[0].pk],
        }
        form = SecurityZonePolicyBulkEditForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        request = RequestFactory().post("/", data)
        view = SecurityZonePolicyBulkEditView()
        # The first policy is valid; the second overlaps its saved destination.
        with self.assertRaises(ValidationError) as error:
            with transaction.atomic():
                view._update_objects(form, request)
        self.assertIn("source_address", error.exception.message_dict)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.description, "")
        self.assertFalse(other.source_address.exists())

    def test_bulk_edit_cannot_fake_clearing_an_address_field(self):
        self.policy.source_zone = self.policy.destination_zone = self.intra_zone
        self.policy.save()
        self.policy.destination_address.set([self.addresses[0]])
        data = {
            "pk": [self.policy.pk],
            "destination_zone": self.destination_zone.pk,
            "_nullify": ["source_address"],
        }
        form = SecurityZonePolicyBulkEditForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        request = RequestFactory().post("/", data)
        with self.assertRaises(ValidationError) as error:
            with transaction.atomic():
                SecurityZonePolicyBulkEditView()._update_objects(form, request)
        self.assertIn("source_address", error.exception.message_dict)
        self.policy.refresh_from_db()
        self.assertEqual(self.policy.destination_zone, self.intra_zone)
