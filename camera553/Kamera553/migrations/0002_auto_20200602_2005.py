# Generated by Django 3.0.6 on 2020-06-02 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kamera553', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='owner_id',
            field=models.IntegerField(default=-1, verbose_name='Kullanıcı ID si'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='cam_name',
            field=models.CharField(max_length=64, verbose_name='Kamera Adı'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='cam_url',
            field=models.CharField(max_length=256, verbose_name='Kamera Url Adresi'),
        ),
    ]
