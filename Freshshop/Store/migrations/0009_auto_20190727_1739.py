# Generated by Django 2.1.8 on 2019-07-27 09:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_auto_20190727_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='下单时间'),
        ),
    ]
