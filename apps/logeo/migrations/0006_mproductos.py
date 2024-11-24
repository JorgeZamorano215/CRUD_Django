# Generated by Django 4.2.6 on 2024-05-18 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logeo', '0005_maccesos'),
    ]

    operations = [
        migrations.CreateModel(
            name='mProductos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Codigo', models.CharField(max_length=13)),
                ('Producto', models.CharField(max_length=50)),
                ('PreCompra', models.FloatField()),
                ('PreVenta', models.FloatField()),
                ('Utilidad', models.FloatField()),
                ('Stock', models.IntegerField()),
                ('MinStock', models.IntegerField()),
                ('Proveedor', models.IntegerField()),
            ],
        ),
    ]
