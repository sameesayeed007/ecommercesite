# Generated by Django 2.2.15 on 2020-12-20 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0022_productimage_is_own'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificationprice',
            name='is_own',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='specificationprice',
            name='mother_specification_id',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
    ]
