# Generated by Django 4.2.7 on 2023-12-20 12:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("userinterface", "0003_rename_cart_orderdetail_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orders",
            name="customer",
        ),
        migrations.DeleteModel(
            name="orderDetail",
        ),
        migrations.DeleteModel(
            name="orders",
        ),
    ]
