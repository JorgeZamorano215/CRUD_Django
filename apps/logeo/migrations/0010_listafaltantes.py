# Generated by Django 4.2.6 on 2024-06-01 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logeo', '0009_mpedidos_tpedidos'),
    ]

    operations = [
        migrations.CreateModel(
            name='listaFaltantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Codigo', models.CharField(max_length=13)),
                ('FechaAlerta', models.DateField()),
                ('Pedido', models.BooleanField()),
            ],
        ),
    ]