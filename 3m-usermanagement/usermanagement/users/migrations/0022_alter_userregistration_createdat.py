# Generated by Django 4.1.3 on 2024-02-27 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_analysis_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
