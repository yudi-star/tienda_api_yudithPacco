from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    """
    Modelo que representa un producto en la tienda.
    Almacena la información básica de cada producto.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,  # Evita productos duplicados
        help_text="Nombre del producto"
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio del producto"
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Cantidad disponible del producto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del producto"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de última actualización"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']  # Ordenar por fecha de creación (más reciente primero)

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"

class Pedido(models.Model):
    """
    Modelo que representa un pedido realizado por un usuario.
    Contiene la información del pedido y su estado.
    """
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pedidos',
        help_text="Usuario que realiza el pedido"
    )
    fecha_pedido = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha en que se realizó el pedido"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        help_text="Estado actual del pedido"
    )
    productos = models.ManyToManyField(
        Producto,
        through='DetallePedido',
        help_text="Productos incluidos en el pedido"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

    def total(self):
        """Calcula el total del pedido"""
        return sum(detalle.subtotal() for detalle in self.detalles.all())

class DetallePedido(models.Model):
    """
    Modelo intermedio para la relación entre Pedido y Producto.
    Almacena la cantidad de cada producto en un pedido.
    """
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles',
        help_text="Pedido al que pertenece este detalle"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        help_text="Producto incluido en el pedido"
    )
    cantidad = models.PositiveIntegerField(
        help_text="Cantidad del producto"
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio del producto al momento de la compra"
    )

    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedidos"

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} en Pedido #{self.pedido.id}"

    def subtotal(self):
        """Calcula el subtotal de este detalle"""
        return self.cantidad * self.precio_unitario