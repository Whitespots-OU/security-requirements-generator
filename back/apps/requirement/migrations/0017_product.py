# Generated by Django 3.1.4 on 2022-07-30 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requirement', '0016_auto_20210701_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('categories', models.ManyToManyField(to='requirement.Category', verbose_name='Category', blank=True)),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]