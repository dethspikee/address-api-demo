# Generated by Django 3.2.6 on 2021-08-17 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0007_remove_address_user_uuid'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('street', 'postcode', 'town', 'country')},
        ),
    ]