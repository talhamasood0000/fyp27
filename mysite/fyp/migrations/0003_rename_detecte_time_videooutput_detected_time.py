# Generated by Django 4.0.3 on 2022-04-02 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fyp', '0002_videooutput'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videooutput',
            old_name='detecte_time',
            new_name='detected_time',
        ),
    ]
