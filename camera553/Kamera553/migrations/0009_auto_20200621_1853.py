# Generated by Django 3.0.6 on 2020-06-21 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kamera553', '0008_auto_20200621_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='cam_alarmstatus',
            field=models.BooleanField(default=False, verbose_name='Alarm Durumu'),
        ),
        migrations.AddField(
            model_name='camera',
            name='cam_status',
            field=models.BooleanField(default=True, verbose_name='Kamerda Durumu'),
        ),
    ]
