# Generated by Django 5.0.4 on 2024-05-12 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0013_remove_customer_groups_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="is_staff_property",
            new_name="_is_staff",
        ),
    ]
