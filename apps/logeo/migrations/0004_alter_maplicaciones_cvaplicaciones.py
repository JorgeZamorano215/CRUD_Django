# Generated by Django 4.2.6 on 2024-04-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logeo', '0003_alter_maplicaciones_dsaplicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maplicaciones',
            name='CvAplicaciones',
            field=models.CharField(max_length=6),
        ),
    ]