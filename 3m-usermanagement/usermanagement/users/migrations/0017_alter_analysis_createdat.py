# Generated by Django 4.1.3 on 2023-01-11 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_analysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='createdAt',
            field=models.DateTimeField(),
        ),
    ]
