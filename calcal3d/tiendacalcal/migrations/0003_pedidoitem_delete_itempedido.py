# Generated by Django 5.1.2 on 2024-10-11 03:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendacalcal', '0002_producto_imagen_alter_producto_categoria_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='tiendacalcal.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tiendacalcal.producto')),
            ],
        ),
        migrations.DeleteModel(
            name='ItemPedido',
        ),
    ]
