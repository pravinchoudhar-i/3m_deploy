# Generated by Django 4.1.3 on 2024-02-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_customuser_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
    ]
