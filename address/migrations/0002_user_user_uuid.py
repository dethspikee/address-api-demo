# Generated by Django 3.2.6 on 2021-08-24 19:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
