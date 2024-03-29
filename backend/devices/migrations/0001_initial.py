# Generated by Django 5.0 on 2023-12-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=255)),
                ('mac_address', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('building', models.CharField(max_length=255)),
                ('floor', models.CharField(max_length=255)),
                ('is_online', models.BooleanField(default=False)),
            ],
        ),
    ]
