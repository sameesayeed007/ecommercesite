# Generated by Django 2.2.15 on 2020-12-19 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0019_product_child_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='child_product_id',
        ),
    ]