# Generated by Django 3.2.6 on 2021-08-13 21:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_auto_20210812_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
