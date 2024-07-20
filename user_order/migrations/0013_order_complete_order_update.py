# Generated by Django 4.2.7 on 2024-07-16 09:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_order", "0012_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="complete",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="update",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
