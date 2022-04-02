# Generated by Django 4.0.3 on 2022-04-02 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fyp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_detected_card', models.IntegerField(default=0)),
                ('detecte_time', models.CharField(default='', max_length=100)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fyp.video')),
            ],
        ),
    ]
