# Generated by Django 5.1.7 on 2025-03-26 07:11
# Django가 모델을 기반으로 자동 생성한 최초 마이그레이션 스크립트

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StandardDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_type', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=255)),
                ('contents', models.TextField()),
            ],
        ),
    ]
