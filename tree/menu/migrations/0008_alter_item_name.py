# Generated by Django 4.1.7 on 2023-02-25 17:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0007_item_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(blank=True, default="default name", max_length=30),
        ),
    ]