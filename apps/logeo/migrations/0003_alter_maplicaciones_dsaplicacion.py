# Generated by Django 4.2.6 on 2024-04-27 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logeo', '0002_maplicaciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maplicaciones',
            name='DsAplicacion',
            field=models.CharField(max_length=50),
        ),
    ]
