# Generated by Django 5.1.2 on 2025-04-22 08:28

import projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=100)),
                ('funding_goal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('detailed_description', models.TextField()),
                ('probem_statement', models.TextField()),
                ('funds_use', models.TextField()),
                ('campaign_cover', models.ImageField(blank=True, null=True, upload_to=projects.models.upload_cover)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('campaign_gallery', models.ImageField(blank=True, null=True, upload_to=projects.models.upload_gallery)),
                ('reward_title', models.CharField(max_length=255)),
                ('reward_description', models.TextField()),
                ('delivery', models.DateField()),
                ('agreements', models.TextField()),
            ],
        ),
    ]
