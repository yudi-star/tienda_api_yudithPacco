# Generated by Django 5.2 on 2025-05-06 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre del producto', max_length=100, unique=True)),
                ('precio', models.DecimalField(decimal_places=2, help_text='Precio del producto', max_digits=10)),
                ('stock', models.PositiveIntegerField(default=0, help_text='Cantidad disponible del producto')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Fecha de creación del producto')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Fecha de última actualización')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True, help_text='Fecha en que se realizó el pedido')),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('EN_PROCESO', 'En Proceso'), ('COMPLETADO', 'Completado'), ('CANCELADO', 'Cancelado')], default='PENDIENTE', help_text='Estado actual del pedido', max_length=20)),
                ('usuario', models.ForeignKey(help_text='Usuario que realiza el pedido', on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-fecha_pedido'],
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(help_text='Cantidad del producto')),
                ('precio_unitario', models.DecimalField(decimal_places=2, help_text='Precio del producto al momento de la compra', max_digits=10)),
                ('pedido', models.ForeignKey(help_text='Pedido al que pertenece este detalle', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='productos.pedido')),
                ('producto', models.ForeignKey(help_text='Producto incluido en el pedido', on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
            options={
                'verbose_name': 'Detalle de Pedido',
                'verbose_name_plural': 'Detalles de Pedidos',
            },
        ),
        migrations.AddField(
            model_name='pedido',
            name='productos',
            field=models.ManyToManyField(help_text='Productos incluidos en el pedido', through='productos.DetallePedido', to='productos.producto'),
        ),
    ]
