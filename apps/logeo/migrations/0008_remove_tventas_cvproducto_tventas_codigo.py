# Generated by Django 4.2.6 on 2024-05-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logeo', '0007_mventas_tventas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tventas',
            name='CvProducto',
        ),
        migrations.AddField(
            model_name='tventas',
            name='Codigo',
            field=models.CharField(default=0, max_length=13),
            preserve_default=False,
        ),
    ]
