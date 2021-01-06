# Generated by Django 2.2.15 on 2020-12-30 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0031_bkashpaymentinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='is_own',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='mother_admin_status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Cancelled', 'Cancelled')], default='Pending', max_length=155),
        ),
    ]