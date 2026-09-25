from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.test import override_settings
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from users.models import ObjectPermission

from dcim.models import Device, DeviceRole, DeviceType, Interface, Manufacturer, Site
from extras.events import serialize_for_event
from ipam.models import Prefix
from netbox.api.fields import ContentTypeField
from netbox_security.api.urls import router
from netbox_security.api.serializers import AddressSerializer
from netbox_security.models import (
    Address,
    AddressAssignment,
    AddressList,
    AddressListAssignment,
    AddressSet,
    AddressSetAssignment,
    Application,
    ApplicationAssignment,
    ApplicationSet,
    ApplicationSetAssignment,
    CustomPrefix,
    FirewallFilter,
    FirewallFilterAssignment,
    FirewallFilterRule,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
    NatPool,
    NatPoolAssignment,
    NatRule,
    NatRuleAssignment,
    NatRuleSet,
    NatRuleSetAssignment,
    Policer,
    PolicerAssignment,
    SecurityZone,
    SecurityZoneAssignment,
)
from netbox_security.tests.custom import APITestCase


@override_settings(EXEMPT_VIEW_PERMISSIONS=[])
class GenericAssignmentPermissionTestCase(APITestCase):
    model = Address
    user_permissions = (
        "netbox_security.view_address",
        "netbox_security.add_address",
        "netbox_security.change_address",
        "netbox_security.view_addressassignment",
        "netbox_security.add_addressassignment",
        "netbox_security.change_addressassignment",
        "netbox_security.view_addresslist",
        "netbox_security.view_securityzone",
    )

    @classmethod
    def setUpTestData(cls):
        cls.visible_prefix = Prefix.objects.create(prefix="192.0.2.0/25")
        cls.hidden_prefix = Prefix.objects.create(prefix="192.0.2.128/25")
        cls.prefix_type = ContentType.objects.get_for_model(Prefix)
        cls.visible_address = Address.objects.create(
            name="visible-address",
            assigned_object_type=cls.prefix_type,
            assigned_object_id=cls.visible_prefix.pk,
        )
        cls.hidden_address = Address.objects.create(
            name="hidden-address",
            assigned_object_type=cls.prefix_type,
            assigned_object_id=cls.hidden_prefix.pk,
        )
        cls.dns_address = Address.objects.create(
            name="dns-address", dns_name="example.com"
        )
        cls.zone = SecurityZone.objects.create(name="target-zone")
        cls.zone_type = ContentType.objects.get_for_model(SecurityZone)

    def setUp(self):
        super().setUp()
        permission = ObjectPermission.objects.create(
            name="visible-prefix-only",
            actions=["view"],
            constraints={"pk": self.visible_prefix.pk},
        )
        permission.object_types.add(self.prefix_type)
        permission.users.add(self.user)

    def test_list_and_brief_hide_inaccessible_targets_and_counts(self):
        for brief in (0, 1):
            with self.subTest(brief=brief):
                response = self.client.get(
                    self._get_list_url(), {"brief": brief}, **self.header
                )
                self.assertHttpStatus(response, 200)
                self.assertEqual(response.data["count"], 2)
                self.assertEqual(
                    {row["id"] for row in response.data["results"]},
                    {self.visible_address.pk, self.dns_address.pk},
                )

    def test_hidden_target_detail_is_not_found(self):
        response = self.client.get(
            self._get_detail_url(self.hidden_address), **self.header
        )
        self.assertHttpStatus(response, 404)

    def test_missing_and_hidden_targets_have_same_write_error(self):
        errors = []
        for target_id in (self.hidden_prefix.pk, self.hidden_prefix.pk + 100000):
            response = self.client.post(
                self._get_list_url(),
                {
                    "name": "new-address",
                    "assigned_object_type": "ipam.prefix",
                    "assigned_object_id": target_id,
                },
                format="json",
                **self.header,
            )
            self.assertHttpStatus(response, 400)
            errors.append(response.data)
        self.assertEqual(errors[0], errors[1])

    def test_patch_checks_effective_target(self):
        response = self.client.patch(
            self._get_detail_url(self.visible_address),
            {
                "assigned_object_id": self.hidden_prefix.pk,
            },
            format="json",
            **self.header,
        )
        self.assertHttpStatus(response, 400)
        self.visible_address.refresh_from_db()
        self.assertEqual(
            self.visible_address.assigned_object_id, self.visible_prefix.pk
        )

    def test_assignment_requires_target_change_permission(self):
        url = reverse("plugins-api:netbox_security-api:addressassignment-list")
        data = {
            "address": {"id": self.visible_address.pk},
            "assigned_object_type": "netbox_security.securityzone",
            "assigned_object_id": self.zone.pk,
        }
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 400)
        self.assertIn("assigned_object_id", response.data)
        self.add_permissions("netbox_security.change_securityzone")
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 201)

    def test_partial_assignment_update_requires_target_change_permission(self):
        assignment = AddressAssignment.objects.create(
            address=self.dns_address,
            assigned_object_type=self.zone_type,
            assigned_object_id=self.zone.pk,
        )
        url = reverse(
            "plugins-api:netbox_security-api:addressassignment-detail",
            args=[assignment.pk],
        )
        response = self.client.patch(
            url, {"address": self.visible_address.pk}, format="json", **self.header
        )
        self.assertHttpStatus(response, 400)
        self.assertIn("assigned_object_id", response.data)

    def test_address_list_cannot_reveal_hidden_target_chain(self):
        address_type = ContentType.objects.get_for_model(Address)
        AddressList.objects.create(
            name="hidden-chain",
            assigned_object_type=address_type,
            assigned_object_id=self.hidden_address.pk,
        )
        visible = AddressList.objects.create(
            name="visible-chain",
            assigned_object_type=address_type,
            assigned_object_id=self.visible_address.pk,
        )
        response = self.client.get(
            reverse("plugins-api:netbox_security-api:addresslist-list"), **self.header
        )
        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], visible.pk)

    def test_nested_address_fails_before_rendering_hidden_target(self):
        from types import SimpleNamespace

        serializer = AddressSerializer(
            self.hidden_address,
            nested=True,
            context={"request": SimpleNamespace(user=self.user)},
        )
        with self.assertRaises(PermissionDenied):
            serializer.data

    def test_missing_request_context_still_rejects_serialization(self):
        with self.assertRaises(PermissionDenied):
            AddressSerializer(self.hidden_address).data

    def test_event_context_does_not_bypass_write_permissions(self):
        serializer = AddressSerializer(
            data={
                "name": "event-context-write",
                "assigned_object_type": "ipam.prefix",
                "assigned_object_id": self.hidden_prefix.pk,
            },
            context={"request": None},
        )
        with self.assertRaises(PermissionDenied):
            serializer.is_valid(raise_exception=True)

    def test_patch_type_only_checks_existing_id_against_new_model(self):
        target = CustomPrefix.objects.create(
            pk=self.visible_prefix.pk, prefix="198.51.100.0/24"
        )
        url = self._get_detail_url(self.visible_address)
        data = {"assigned_object_type": "netbox_security.customprefix"}
        response = self.client.patch(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 400)
        self.visible_address.refresh_from_db()
        self.assertEqual(
            self.visible_address.assigned_object_type_id, self.prefix_type.pk
        )
        self.assertEqual(
            self.visible_address.assigned_object_id, self.visible_prefix.pk
        )

        self.add_permissions("netbox_security.view_customprefix")
        response = self.client.patch(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 200)
        self.visible_address.refresh_from_db()
        self.assertEqual(self.visible_address.assigned_object, target)

    def test_creates_dns_only_address(self):
        response = self.client.post(
            self._get_list_url(),
            {"name": "new-dns-address", "dns_name": "allowed.example.com"},
            format="json",
            **self.header,
        )
        self.assertHttpStatus(response, 201)
        address = Address.objects.get(pk=response.data["id"])
        self.assertEqual(address.dns_name, "allowed.example.com")
        self.assertIsNone(address.assigned_object_type_id)
        self.assertIsNone(address.assigned_object_id)

    def test_rejects_incomplete_target_pairs(self):
        for assignment in (
            {"assigned_object_type": "ipam.prefix"},
            {"assigned_object_id": self.visible_prefix.pk},
        ):
            with self.subTest(assignment=assignment):
                response = self.client.post(
                    self._get_list_url(),
                    {"name": "incomplete", **assignment},
                    format="json",
                    **self.header,
                )
                self.assertHttpStatus(response, 400)
                self.assertIn("assigned_object_type", response.data)
                self.assertIn("assigned_object_id", response.data)
        self.assertFalse(Address.objects.filter(name="incomplete").exists())

    def test_existing_assignment_becomes_inaccessible_after_revocation(self):
        assignment = AddressAssignment.objects.create(
            address=self.dns_address,
            assigned_object_type=self.zone_type,
            assigned_object_id=self.zone.pk,
        )
        detail_url = reverse(
            "plugins-api:netbox_security-api:addressassignment-detail",
            args=[assignment.pk],
        )
        list_url = reverse("plugins-api:netbox_security-api:addressassignment-list")
        self.assertHttpStatus(self.client.get(detail_url, **self.header), 200)
        self.remove_permissions("netbox_security.view_securityzone")
        self.assertHttpStatus(self.client.get(detail_url, **self.header), 404)
        for brief in (0, 1):
            response = self.client.get(list_url, {"brief": brief}, **self.header)
            self.assertHttpStatus(response, 200)
            self.assertEqual(response.data["count"], 0)
            self.assertEqual(response.data["results"], [])
            self.assertNotIn(self.zone.name, response.content.decode())
        # The record remains; only its visibility has changed.
        self.assertTrue(AddressAssignment.objects.filter(pk=assignment.pk).exists())

    def test_change_permission_is_constrained_to_the_selected_target(self):
        other_zone = SecurityZone.objects.create(name="unchangeable-zone")
        permission = ObjectPermission.objects.create(
            name="change-one-zone", actions=["change"], constraints={"pk": self.zone.pk}
        )
        permission.object_types.add(self.zone_type)
        permission.users.add(self.user)
        url = reverse("plugins-api:netbox_security-api:addressassignment-list")
        data = {
            "address": self.dns_address.pk,
            "assigned_object_type": "netbox_security.securityzone",
            "assigned_object_id": other_zone.pk,
        }
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 400)
        self.assertIn("assigned_object_id", response.data)
        self.assertFalse(AddressAssignment.objects.exists())

        data["assigned_object_id"] = self.zone.pk
        response = self.client.post(url, data, format="json", **self.header)
        self.assertHttpStatus(response, 201)
        assignment = AddressAssignment.objects.get(pk=response.data["id"])
        detail_url = reverse(
            "plugins-api:netbox_security-api:addressassignment-detail",
            args=[assignment.pk],
        )
        response = self.client.patch(
            detail_url,
            {"assigned_object_id": other_zone.pk},
            format="json",
            **self.header,
        )
        self.assertHttpStatus(response, 400)
        assignment.refresh_from_db()
        self.assertEqual(assignment.assigned_object_id, self.zone.pk)


@override_settings(EXEMPT_VIEW_PERMISSIONS=[])
class GenericAssignmentEndpointPermissionTestCase(APITestCase):
    """Exercise every generic-assignment route with object-constrained permissions."""

    model = Address

    @classmethod
    def setUpTestData(cls):
        site = Site.objects.create(name="assignment-site", slug="assignment-site")
        manufacturer = Manufacturer.objects.create(
            name="assignment-maker", slug="assignment-maker"
        )
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer, model="assignment-type", slug="assignment-type"
        )
        role = DeviceRole.objects.create(name="assignment-role", slug="assignment-role")
        devices = [
            Device.objects.create(
                name=f"{visibility}-assignment-device",
                site=site,
                device_type=device_type,
                role=role,
            )
            for visibility in ("visible", "hidden")
        ]
        interfaces = [
            Interface.objects.create(
                name=f"{visibility}-assignment-interface",
                device=device,
                type="virtual",
            )
            for visibility, device in zip(("visible", "hidden"), devices)
        ]
        prefixes = [
            Prefix.objects.create(prefix=prefix)
            for prefix in ("203.0.113.0/25", "203.0.113.128/25")
        ]
        address_sets = [
            AddressSet.objects.create(name=f"{visibility}-target-set")
            for visibility in ("visible", "hidden")
        ]
        firewall_filter = FirewallFilter.objects.create(name="assignment-filter")
        rules = [
            FirewallFilterRule.objects.create(
                name=f"{visibility}-target-rule",
                index=index,
                firewall_filter=firewall_filter,
            )
            for index, visibility in enumerate(("visible", "hidden"))
        ]
        source_address = Address.objects.create(
            name="source-dns", dns_name="source.example.com"
        )
        source_list = AddressList.objects.create(
            name="source-list",
            assigned_object_type=ContentType.objects.get_for_model(Address),
            assigned_object_id=source_address.pk,
        )
        source_set = AddressSet.objects.create(name="source-set")
        source_zone = SecurityZone.objects.create(name="source-zone")
        application = Application.objects.create(name="source-application")
        application_set = ApplicationSet.objects.create(name="source-application-set")
        pool = NatPool.objects.create(name="source-pool")
        ruleset = NatRuleSet.objects.create(name="source-ruleset")
        nat_rule = NatRule.objects.create(name="source-nat-rule")
        policer = Policer.objects.create(name="source-policer")
        cls.sources = [
            source_address,
            source_list,
            source_set,
            source_zone,
            application,
            application_set,
            pool,
            ruleset,
            nat_rule,
            policer,
            firewall_filter,
        ]
        # model, required non-target values, targets, required target action
        definitions = [
            (Address, {"name": "endpoint-address"}, prefixes, "view"),
            (AddressList, {"name": "endpoint-list"}, address_sets, "view"),
            (AddressAssignment, {"address": source_address}, devices, "change"),
            (AddressListAssignment, {"address_list": source_list}, devices, "change"),
            (AddressSetAssignment, {"address_set": source_set}, devices, "change"),
            (ApplicationAssignment, {"application": application}, devices, "change"),
            (
                ApplicationSetAssignment,
                {"application_set": application_set},
                devices,
                "change",
            ),
            (SecurityZoneAssignment, {"zone": source_zone}, devices, "change"),
            (NatPoolAssignment, {"pool": pool}, devices, "change"),
            (NatRuleSetAssignment, {"ruleset": ruleset}, devices, "change"),
            (NatRuleAssignment, {"rule": nat_rule}, interfaces, "change"),
            (PolicerAssignment, {"policer": policer}, devices, "change"),
            (
                FirewallFilterAssignment,
                {"firewall_filter": firewall_filter},
                devices,
                "change",
            ),
        ]
        for setting_model in (FirewallRuleFromSetting, FirewallRuleThenSetting):
            key = next(
                value
                for value, _ in setting_model._meta.get_field("key").flatchoices
                if value
            )
            definitions.append(
                (setting_model, {"key": key, "value": "1"}, rules, "change")
            )
        cls.cases = []
        for model, values, targets, action in definitions:
            content_type = ContentType.objects.get_for_model(targets[0])
            records = [
                model.objects.create(
                    **values,
                    assigned_object_type=content_type,
                    assigned_object_id=target.pk,
                )
                for target in targets
            ]
            cls.cases.append((model, values, targets, action, records))

    def setUp(self):
        super().setUp()
        permitted = defaultdict(set)
        for source in self.sources:
            permitted[type(source)].add(source.pk)
        for model, _, targets, _, records in self.cases:
            # The user may view both assignments but only one of their targets.
            permitted[model].update(record.pk for record in records)
            permitted[type(targets[0])].add(targets[0].pk)
            self.add_permissions(f"netbox_security.add_{model._meta.model_name}")
        for model, ids in permitted.items():
            permission = ObjectPermission.objects.create(
                name=f"view-fixtures-{model._meta.label_lower}",
                actions=["view"],
                constraints={"pk__in": list(ids)},
            )
            permission.object_types.add(ContentType.objects.get_for_model(model))
            permission.users.add(self.user)

    def test_event_snapshots_include_targets_without_request_permissions(self):
        for model, _, targets, _, records in self.cases:
            for target, record in zip(targets, records):
                with self.subTest(model=model._meta.label, target=target.pk):
                    data = serialize_for_event(record)
                    self.assertEqual(data["id"], record.pk)
                    self.assertEqual(data["assigned_object_id"], target.pk)
                    self.assertEqual(data["assigned_object"]["id"], target.pk)

    def test_every_generic_endpoint_is_exercised(self):
        registered = {
            view.queryset.model
            for _, view, _ in router.registry
            if "assigned_object"
            in {field.name for field in view.queryset.model._meta.private_fields}
        }
        self.assertEqual({model for model, *_ in self.cases}, registered)

    def test_list_brief_and_detail_exclude_hidden_targets(self):
        for model, _, targets, _, records in self.cases:
            visible, hidden = records
            list_url = reverse(
                f"plugins-api:netbox_security-api:{model._meta.model_name}-list"
            )
            hidden_url = reverse(
                f"plugins-api:netbox_security-api:{model._meta.model_name}-detail",
                args=[hidden.pk],
            )
            visible_url = reverse(
                f"plugins-api:netbox_security-api:{model._meta.model_name}-detail",
                args=[visible.pk],
            )
            for brief in (0, 1):
                with self.subTest(model=model._meta.label, brief=brief):
                    response = self.client.get(
                        list_url, {"brief": brief}, **self.header
                    )
                    self.assertHttpStatus(response, 200)
                    self.assertEqual(response.data["count"], model.objects.count() - 1)
                    ids = {row["id"] for row in response.data["results"]}
                    self.assertIn(visible.pk, ids)
                    self.assertNotIn(hidden.pk, ids)
                    self.assertNotIn(str(targets[1]), response.content.decode())
                    self.assertHttpStatus(
                        self.client.get(hidden_url, {"brief": brief}, **self.header),
                        404,
                    )
                    detail = self.client.get(
                        visible_url, {"brief": brief}, **self.header
                    )
                    self.assertHttpStatus(detail, 200)
                    self.assertEqual(detail.data["id"], visible.pk)

    def test_create_checks_target_permissions_on_every_endpoint(self):
        for model, values, targets, action, records in self.cases:
            with self.subTest(model=model._meta.label):
                content_type = ContentType.objects.get_for_model(targets[0])
                view = next(
                    view
                    for _, view, _ in router.registry
                    if view.queryset.model is model
                )
                type_field = view.serializer_class().fields["assigned_object_type"]
                type_value = (
                    f"{content_type.app_label}.{content_type.model}"
                    if isinstance(type_field, ContentTypeField)
                    else content_type.pk
                )
                payload = {
                    name: value.pk if hasattr(value, "pk") else value
                    for name, value in values.items()
                }
                payload.update(
                    assigned_object_type=type_value, assigned_object_id=targets[1].pk
                )
                list_url = reverse(
                    f"plugins-api:netbox_security-api:{model._meta.model_name}-list"
                )
                # Remove the fixtures to avoid uniqueness errors masking validation.
                for record in records:
                    record.delete()
                before = model.objects.count()
                errors = []
                for target_id in (targets[1].pk, targets[1].pk + 100000):
                    payload["assigned_object_id"] = target_id
                    response = self.client.post(
                        list_url, payload, format="json", **self.header
                    )
                    self.assertHttpStatus(response, 400)
                    self.assertIn("assigned_object_id", response.data)
                    errors.append(response.data)
                self.assertEqual(errors[0], errors[1])
                self.assertEqual(model.objects.count(), before)
                payload["assigned_object_id"] = targets[0].pk
                permission = None
                if action == "change":
                    response = self.client.post(
                        list_url, payload, format="json", **self.header
                    )
                    self.assertHttpStatus(response, 400)
                    self.assertIn("assigned_object_id", response.data)
                    permission = ObjectPermission.objects.create(
                        name=f"change-target-{model._meta.model_name}",
                        actions=["change"],
                        constraints={"pk": targets[0].pk},
                    )
                    permission.object_types.add(content_type)
                    permission.users.add(self.user)
                try:
                    response = self.client.post(
                        list_url, payload, format="json", **self.header
                    )
                    self.assertHttpStatus(response, 201)
                    self.assertEqual(model.objects.count(), before + 1)
                finally:
                    if permission is not None:
                        permission.delete()
