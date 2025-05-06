from django.contrib import admin
from .models import Producto, Pedido, DetallePedido

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'created_at')
    search_fields = ('nombre',)
    list_filter = ('created_at',)

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__username',)
    inlines = [DetallePedidoInline]