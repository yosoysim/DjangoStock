# Generated by Django 3.0.4 on 2020-03-10 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_book_cover'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('special_status', 'Can read all books')]},
        ),
    ]
