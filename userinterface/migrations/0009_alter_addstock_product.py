# Generated by Django 5.0.7 on 2024-08-02 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userinterface", "0008_addstock_name_alter_addstock_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addstock",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="userinterface.product"
            ),
        ),
    ]
