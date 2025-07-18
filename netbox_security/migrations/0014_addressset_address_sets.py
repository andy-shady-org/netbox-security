# Generated by Django 5.2 on 2025-07-03 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_security", "0013_address_identifier_addressset_identifier_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="addressset",
            name="address_sets",
            field=models.ManyToManyField(
                related_name="%(class)s_address_sets", to="netbox_security.addressset"
            ),
        ),
    ]
