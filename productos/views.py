# productos/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Producto, Pedido, DetallePedido
from .serializers import (
    ProductoSerializer, PedidoSerializer, CrearPedidoSerializer
)

class ProductoListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todos los productos y crear nuevos productos.
    Permite a los usuarios autenticados crear productos.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para obtener, actualizar y eliminar un producto específico.
    Permite a los usuarios autenticados modificar o eliminar productos.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
class PedidoListView(generics.ListAPIView):
    """
    Vista para listar todos los pedidos del usuario autenticado.
    Solo los usuarios autenticados pueden ver sus pedidos.
    """
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra los pedidos para mostrar solo los del usuario actual.
        """
        return Pedido.objects.filter(usuario=self.request.user)

class PedidoCreateView(generics.CreateAPIView):
    """
    Vista para crear un nuevo pedido.
    Requiere que el usuario esté autenticado.
    """
    serializer_class = CrearPedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo pedido y devuelve una respuesta.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)   