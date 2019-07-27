# Generated by Django 2.1.8 on 2019-07-27 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_customer_address_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='goods_id',
        ),
        migrations.AddField(
            model_name='customer',
            name='goods_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Store.Goods', verbose_name='商品id'),
            preserve_default=False,
        ),
    ]
