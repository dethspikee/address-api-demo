# Generated by Django 3.2.6 on 2021-08-24 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_user_user_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_uuid',
        ),
    ]
