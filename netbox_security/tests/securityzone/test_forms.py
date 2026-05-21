from django.test import TestCase

from netbox_security.forms import SecurityZoneForm
from netbox_security.models import SecurityZone, SecurityZonePolicy


class SecurityZoneFormTestCase(TestCase):
    def test_disallow_intra_zone_rejected_with_same_zone_policies(self):
        zone = SecurityZone.objects.create(name="INTRA-ZONE", allow_intra_zone=True)
        SecurityZonePolicy.objects.create(
            name="intra-zone-policy",
            index=999,
            source_zone=zone,
            destination_zone=zone,
            policy_actions=["permit"],
        )

        form = SecurityZoneForm(
            data={
                "name": zone.name,
                "identifier": zone.identifier or "",
                "description": zone.description or "",
                "allow_intra_zone": False,
            },
            instance=zone,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("allow_intra_zone", form.errors)
