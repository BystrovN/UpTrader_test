# Generated by Django 4.1.7 on 2023-02-25 17:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0006_alter_item_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="name",
            field=models.CharField(default="default name", max_length=30),
        ),
    ]