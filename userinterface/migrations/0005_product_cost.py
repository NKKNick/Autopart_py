# Generated by Django 4.2.7 on 2024-05-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userinterface", "0004_remove_orders_customer_delete_orderdetail_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="cost",
            field=models.IntegerField(default=200),
        ),
    ]
