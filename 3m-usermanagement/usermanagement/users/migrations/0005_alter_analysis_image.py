# Generated by Django 4.1.3 on 2022-12-12 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_analysis_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='image',
            field=models.FileField(upload_to='analytics-images'),
        ),
    ]
