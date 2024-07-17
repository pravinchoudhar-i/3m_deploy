# Generated by Django 4.1.3 on 2023-01-11 10:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_delete_analysis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='analytics-images')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('predictionType', models.CharField(max_length=100)),
                ('predictionColor', models.CharField(max_length=100)),
                ('feedbackType', models.CharField(max_length=100)),
                ('feedbackColor', models.CharField(max_length=100)),
                ('createdAt', models.DateTimeField(default=datetime.datetime(2023, 1, 11, 10, 55, 1, 1221))),
                ('updatedAt', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=1)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='create', to='users.userregistration')),
                ('updatedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='update', to='users.userregistration')),
            ],
        ),
    ]
