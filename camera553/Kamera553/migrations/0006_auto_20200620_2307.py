# Generated by Django 3.0.6 on 2020-06-20 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kamera553', '0005_camera_cam_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='cam_image',
            field=models.BinaryField(verbose_name='Kamera Anlık Feed'),
        ),
    ]
