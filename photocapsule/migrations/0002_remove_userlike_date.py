# Generated by Django 2.2.28 on 2024-03-17 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photocapsule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlike',
            name='date',
        ),
    ]