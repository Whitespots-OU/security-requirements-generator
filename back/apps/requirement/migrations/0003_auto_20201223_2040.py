# Generated by Django 3.1.4 on 2020-12-23 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("requirement", "0002_auto_20201223_2015"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="name_en",
            field=models.CharField(max_length=128, null=True, verbose_name="Name"),
        ),
        migrations.AddField(
            model_name="category",
            name="name_ru",
            field=models.CharField(max_length=128, null=True, verbose_name="Name"),
        ),
    ]
