# Generated by Django 4.2.7 on 2024-06-05 14:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("worker_app", "0020_alter_assignwork_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="workrequest",
            old_name="customer",
            new_name="admin",
        ),
    ]
