# Generated by Django 4.0 on 2022-01-28 21:46

import ckeditor.fields
import datetime
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=200)),
                ('titulo', models.CharField(max_length=200)),
                ('autor', models.CharField(max_length=200)),
                ('fecha', models.CharField(blank=True, default=datetime.datetime(2022, 1, 28, 18, 46, 32, 798746), max_length=100, null=True)),
                ('texto', ckeditor.fields.RichTextField(max_length=10000)),
                ('portada', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='AppProyectoFinal/static/AppProyectoFinal/img'), upload_to='')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Foro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(blank=True, default='anonimo', max_length=100, null=True)),
                ('mensaje', ckeditor.fields.RichTextField()),
                ('fecha', models.CharField(blank=True, default=datetime.datetime(2022, 1, 28, 18, 46, 32, 797766), max_length=100, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
