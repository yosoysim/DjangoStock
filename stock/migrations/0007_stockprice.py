# Generated by Django 3.0.4 on 2020-03-12 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_auto_20200310_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(blank=True, max_length=30, null=True)),
                ('txn_date', models.DateField()),
                ('price_open', models.FloatField(blank=True, null=True)),
                ('price_high', models.FloatField(blank=True, null=True)),
                ('price_low', models.FloatField(blank=True, null=True)),
                ('price_close', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('volume_foreign', models.FloatField(blank=True, null=True)),
                ('volume_org', models.FloatField(blank=True, null=True)),
                ('per', models.FloatField(blank=True, null=True)),
                ('eps', models.FloatField(blank=True, null=True)),
                ('pbr', models.FloatField(blank=True, null=True)),
                ('risefall', models.FloatField(blank=True, null=True)),
                ('risefall_rate', models.FloatField(blank=True, null=True)),
                ('fcst', models.IntegerField(blank=True, null=True)),
                ('residual', models.IntegerField(blank=True, null=True)),
                ('upd_d', models.DateTimeField(blank=True, null=True)),
                ('price_avg', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'stock_price',
                'managed': False,
            },
        ),
    ]
