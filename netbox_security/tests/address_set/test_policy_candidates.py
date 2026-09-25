from types import SimpleNamespace
from unittest import TestCase

from netbox_security.utils.policy_candidates import classify_match, _path_scope


class PolicyCandidateClassificationTestCase(TestCase):
    def test_match_classification(self):
        for members, scope, expected in (
            ({1}, True, "zone_confirmed"),
            ({2}, True, "zone_mismatch"),
            (None, True, "unconfirmed"),
            ({1}, None, "unconfirmed"),
            ({1}, False, "scope_mismatch"),
            (None, False, "scope_mismatch"),
        ):
            with self.subTest(members=members, scope=scope):
                self.assertEqual(classify_match(1, members, scope), expected)

    def test_address_book_scopes(self):
        obj = SimpleNamespace(pk=1, _meta=SimpleNamespace(model_name="address"))
        for assignments, zone, device, expected in (
            ([], 1, None, True),
            (None, 1, None, None),
            ([("netbox_security", "securityzone", 1)], 1, None, True),
            ([("netbox_security", "securityzone", 1)], 2, None, False),
            ([("dcim", "device", 4)], 1, 4, True),
            ([("dcim", "device", 4)], 1, 5, False),
            ([("dcim", "device", 4)], 1, None, None),
        ):
            with self.subTest(assignments=assignments, zone=zone, device=device):
                allowed, _ = _path_scope(
                    [obj], {("address", 1): assignments}, zone, device
                )
                self.assertIs(allowed, expected)

    def test_global_wrapper_preserves_child_scope(self):
        wrapper = SimpleNamespace(pk=2, _meta=SimpleNamespace(model_name="addresslist"))
        child = SimpleNamespace(pk=1, _meta=SimpleNamespace(model_name="address"))
        scopes = {
            ("addresslist", 2): [],
            ("address", 1): [("netbox_security", "securityzone", 8)],
        }
        self.assertIs(_path_scope([wrapper, child], scopes, 9, None)[0], False)
        self.assertIs(_path_scope([wrapper, child], scopes, 8, None)[0], True)
