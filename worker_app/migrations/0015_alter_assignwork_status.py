# Generated by Django 4.2.7 on 2024-05-05 16:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("worker_app", "0014_workrequest_note"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignwork",
            name="status",
            field=models.CharField(
                choices=[("1", "กำลังดำเนินการ"), ("2", "เสร็จสิ้น")],
                default=1,
                max_length=20,
            ),
        ),
    ]
