# Generated by Django 4.2.23 on 2025-07-08 14:09

from django.db import migrations, models
import prediction.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=prediction.models.upload_image_path)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('predicted_age', models.IntegerField(blank=True, null=True)),
                ('predicted_gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('age_confidence', models.FloatField(blank=True, null=True)),
                ('gender_confidence', models.FloatField(blank=True, null=True)),
                ('processing_time', models.FloatField(blank=True, null=True)),
                ('is_successful', models.BooleanField(default=False)),
                ('error_message', models.TextField(blank=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
