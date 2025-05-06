# productos/urls.py

from django.urls import path
from .views import (
    ProductoListCreateView,
    ProductoRetrieveUpdateDestroyView,
    PedidoListView,
    PedidoCreateView
)

app_name = 'productos'

urlpatterns = [
    # URLs para Productos
    path('productos/',
         ProductoListCreateView.as_view(),
         name='producto-list-create'),

    path('productos/<int:pk>/',
         ProductoRetrieveUpdateDestroyView.as_view(),
         name='producto-detail'),

    # URLs para Pedidos
    path('pedidos/',
         PedidoListView.as_view(),
         name='pedido-list'),

    path('pedidos/crear/',
         PedidoCreateView.as_view(),
         name='pedido-create'),
]