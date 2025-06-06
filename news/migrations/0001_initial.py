# Generated by Django 5.2.2 on 2025-06-05 16:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('url', models.URLField(max_length=2000, unique=True, verbose_name='記事URL')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='概要')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='発行日時')),
                ('source_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='情報源')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': 'ニュース記事',
                'verbose_name_plural': 'ニュース記事',
                'ordering': ['-published_at', '-created_at'],
            },
        ),
    ]
