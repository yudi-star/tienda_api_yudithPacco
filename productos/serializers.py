# productos/serializers.py

from rest_framework import serializers
from .models import Producto, Pedido, DetallePedido
from django.contrib.auth.models import User

class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Producto.
    Permite la conversión de Productos a JSON y viceversa.
    """
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # Estos campos no se pueden modificar

    def validate_stock(self, value):
        """
        Validación personalizada para el stock.
        Asegura que el stock no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def validate_precio(self, value):
        """
        Validación personalizada para el precio.
        Asegura que el precio sea mayor a cero.
        """
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        return value

class DetallePedidoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo DetallePedido.
    Se usa para mostrar y crear detalles de pedidos.
    """
    nombre_producto = serializers.CharField(source='producto.nombre', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'nombre_producto', 'cantidad',
                 'precio_unitario', 'subtotal']
        read_only_fields = ['precio_unitario']  # Se establecerá automáticamente

    def validate_cantidad(self, value):
        """
        Validación personalizada para la cantidad.
        Asegura que la cantidad sea mayor a cero.
        """
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value

class PedidoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Pedido.
    Se usa para mostrar los pedidos existentes.
    """
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    usuario = serializers.StringRelatedField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'fecha_pedido', 'estado', 'detalles', 'total']
        read_only_fields = ['fecha_pedido']

class CrearPedidoSerializer(serializers.ModelSerializer):
    """
    Serializer especial para crear nuevos pedidos.
    Permite enviar una lista de productos y sus cantidades.
    """
    detalles = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        write_only=True
    )

    class Meta:
        model = Pedido
        fields = ['detalles']

    def validate_detalles(self, detalles):
        """
        Validación de los detalles del pedido.
        Verifica que haya stock suficiente.
        """
        for detalle in detalles:
            try:
                producto = Producto.objects.get(id=detalle['producto_id'])
                if producto.stock < detalle['cantidad']:
                    raise serializers.ValidationError(
                        f"Stock insuficiente para {producto.nombre}. "
                        f"Disponible: {producto.stock}"
                    )
            except Producto.DoesNotExist:
                raise serializers.ValidationError(
                    f"El producto con ID {detalle['producto_id']} no existe."
                )
        return detalles

    def create(self, validated_data):
        """
        Crea un nuevo pedido con sus detalles.
        También actualiza el stock de los productos.
        """
        detalles_data = validated_data.pop('detalles')
        usuario = self.context['request'].user

        # Crear el pedido
        pedido = Pedido.objects.create(usuario=usuario)

        # Crear los detalles del pedido
        for detalle in detalles_data:
            producto = Producto.objects.get(id=detalle['producto_id'])
            cantidad = detalle['cantidad']

            # Crear el detalle
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )

            # Actualizar el stock
            producto.stock -= cantidad
            producto.save()

        return pedido