# Generated by Django 2.2.15 on 2020-12-19 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0021_productimage_mother_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='is_own',
            field=models.BooleanField(default=True),
        ),
    ]
