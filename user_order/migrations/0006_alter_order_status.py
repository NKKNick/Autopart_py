# Generated by Django 4.2.7 on 2024-02-08 07:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_order", "0005_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("1", "รอผู้ดูแลยืนยันคำสั่งซื้อ"),
                    ("2", "กำลังเตรียมสินค้า"),
                    ("3", "กำลังนำสินค้าไปส่ง"),
                    ("4", "ทำการส่งเรียบร้อย"),
                    ("5", "ผู้ใช้รับสินค้าแล้ว"),
                    ("6", "คำสั่งซื้อถูกยกเลิก"),
                    ("7", "ยังไม่ได้ส่งสลิป"),
                ],
                default=1,
                max_length=20,
            ),
        ),
    ]
