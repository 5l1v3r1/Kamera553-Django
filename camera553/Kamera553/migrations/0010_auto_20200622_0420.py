# Generated by Django 3.0.6 on 2020-06-22 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kamera553', '0009_auto_20200621_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='r_camid',
            field=models.IntegerField(default=-1, verbose_name='Kamera Id si'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='cam_status',
            field=models.BooleanField(default=False, verbose_name='Kamerda Durumu'),
        ),
    ]
