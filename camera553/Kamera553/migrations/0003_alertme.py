# Generated by Django 3.0.6 on 2020-06-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kamera553', '0002_auto_20200602_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='alertme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_start', models.CharField(max_length=5, verbose_name='Başlangıç Saati')),
                ('a_end', models.CharField(max_length=5, verbose_name='Başlangıç Saati')),
            ],
        ),
    ]
