# Generated by Django 3.1.6 on 2021-02-13 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0007_auto_20210213_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprofile',
            name='email',
        ),
    ]
