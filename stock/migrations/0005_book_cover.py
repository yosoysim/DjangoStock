# Generated by Django 3.0.4 on 2020-03-09 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, upload_to='covers/'),
        ),
    ]