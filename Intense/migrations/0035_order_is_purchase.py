# Generated by Django 2.2.15 on 2021-01-02 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0034_auto_20210102_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_purchase',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
