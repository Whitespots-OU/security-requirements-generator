# Generated by Django 3.1.4 on 2021-01-02 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_auto_20201225_2050"),
    ]

    operations = [
        migrations.AlterField(
            model_name="config",
            name="export_company_name",
            field=models.CharField(default="Company name", max_length=256, verbose_name="Company name"),
        ),
    ]
