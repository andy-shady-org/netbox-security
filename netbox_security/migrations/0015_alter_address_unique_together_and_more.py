# Generated by Django 5.2 on 2025-07-04 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ipam", "0081_remove_service_device_virtual_machine_add_parent_gfk_index"),
        ("netbox_security", "0014_addressset_address_sets"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="address",
            unique_together={("name", "identifier", "address", "dns_name", "ip_range")},
        ),
        migrations.AlterUniqueTogether(
            name="addressset",
            unique_together={("name", "identifier")},
        ),
        migrations.AlterUniqueTogether(
            name="application",
            unique_together={("name", "identifier")},
        ),
        migrations.AlterUniqueTogether(
            name="applicationset",
            unique_together={("name", "identifier")},
        ),
        migrations.AlterUniqueTogether(
            name="securityzone",
            unique_together={("name", "identifier")},
        ),
        migrations.AlterUniqueTogether(
            name="securityzonepolicy",
            unique_together={("name", "identifier", "source_zone", "destination_zone")},
        ),
    ]
