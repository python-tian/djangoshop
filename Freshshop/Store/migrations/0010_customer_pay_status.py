# Generated by Django 2.1.8 on 2019-07-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_auto_20190727_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='pay_status',
            field=models.IntegerField(default=1, verbose_name='支付状态'),
        ),
    ]
