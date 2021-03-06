# Generated by Django 3.0.6 on 2020-06-23 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kamera553', '0013_camera_cam_ownermail'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertme',
            name='alert_image',
            field=models.BinaryField(null=True, verbose_name='Kamera Alarm Görüntüsü/'),
        ),
        migrations.AddField(
            model_name='reports',
            name='r_yakinsay',
            field=models.IntegerField(default=55, verbose_name='Yakın Duran İnsan Sayısı'),
            preserve_default=False,
        ),
    ]
