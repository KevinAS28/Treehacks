# Generated by Django 3.1.1 on 2021-02-13 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_patientprofile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprofile',
            name='user',
        ),
    ]
