from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),  # Lista de productos
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),  # Detalle de producto
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # Agregar al carrito
    path('carrito/', views.detalle_carrito, name='detalle_carrito'),  # Ver el carrito
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),  # Eliminar del carrito
    path('procesar/', views.procesar_pedido, name='procesar_pedido'),  # Procesar pedido
    path('actualizar/<int:item_id>/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),
    path('categoria/<int:categoria_id>/', views.filtrar_por_categoria, name='filtrar_por_categoria'),
    path('procesar/', views.procesar_pedido, name='procesar_pedido'),
    path('historial/', views.historial_pedidos, name='historial_pedidos'),
    path('pago/<int:pedido_id>/', views.pago_simulado, name='pago_simulado'),

]
