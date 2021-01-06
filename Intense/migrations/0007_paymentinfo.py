# Generated by Django 2.2.15 on 2020-12-08 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Intense', '0006_specificationprice_specification_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(blank=True, default=-1, null=True)),
                ('transaction_id', models.CharField(blank=True, default='', max_length=255)),
                ('payment_method', models.CharField(blank=True, default='', max_length=255)),
                ('merchant_id', models.IntegerField(blank=True, default=-1, null=True)),
                ('payment_reference_id', models.CharField(blank=True, default='', max_length=255)),
                ('amount', models.CharField(blank=True, default='', max_length=255)),
                ('client_mobile_number', models.CharField(blank=True, default='', max_length=255)),
                ('order_datetime', models.CharField(blank=True, default='', max_length=255)),
                ('issuer_payment_datetime', models.CharField(blank=True, default='', max_length=255)),
                ('issuer_payment_ref_no', models.CharField(blank=True, default='', max_length=255)),
                ('additional_merchant_info', models.CharField(blank=True, default='', max_length=255)),
                ('status', models.CharField(blank=True, default='', max_length=255)),
                ('status_code', models.CharField(blank=True, default='', max_length=255)),
                ('cancelissuer_datetime', models.CharField(blank=True, default='', max_length=255)),
                ('cancelissuer_ref_no', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
    ]
