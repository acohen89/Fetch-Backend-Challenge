# Generated by Django 5.1.1 on 2024-09-17 20:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_receipt_purchasedate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
