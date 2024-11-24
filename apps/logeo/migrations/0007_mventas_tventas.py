# Generated by Django 4.2.6 on 2024-05-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logeo', '0006_mproductos'),
    ]

    operations = [
        migrations.CreateModel(
            name='mVentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Empleado', models.IntegerField()),
                ('Cliente', models.IntegerField()),
                ('FechaVenta', models.DateField()),
                ('SubTotal', models.FloatField()),
                ('Impuesto', models.FloatField()),
                ('Total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='tVentas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CvVenta', models.IntegerField()),
                ('CvProducto', models.IntegerField()),
                ('PrecioVenta', models.FloatField()),
                ('Cantidad', models.IntegerField()),
                ('SubTot', models.FloatField()),
            ],
        ),
    ]
