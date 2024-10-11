from django.shortcuts import render
from .models import Producto
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import Carrito, ItemCarrito, Cliente
from .models import Pedido, PedidoItem
from django.db import transaction
from django.core.paginator import Paginator
from django.utils import timezone


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tiendacalcal/lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tiendacalcal/detalle_producto.html', {'producto': producto})

def agregar_al_carrito(request, producto_id):
    cliente = Cliente.objects.get(usuario=request.user)  # Cliente autenticado
    carrito, creado = Carrito.objects.get_or_create(cliente=cliente)  # Crear carrito si no existe
    producto = get_object_or_404(Producto, id=producto_id)

    # Buscar si el producto ya está en el carrito
    item_carrito, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not creado:
        item_carrito.cantidad += 1  # Incrementar cantidad si ya está en el carrito
        item_carrito.save()

    return redirect('detalle_carrito')  # Redirigir al detalle del carrito

def detalle_carrito(request):
    cliente = Cliente.objects.get(usuario=request.user)
    carrito = Carrito.objects.get(cliente=cliente)
    items = carrito.items.all()  # Obtener los items del carrito

    total = sum([item.producto.precio * item.cantidad for item in items])  # Calcular el total
    return render(request, 'tiendacalcal/detalle_carrito.html', {'carrito': carrito, 'items': items, 'total': total})

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()  # Eliminar el item del carrito
    return redirect('detalle_carrito')

@transaction.atomic  # Asegurar transacción completa
def procesar_pedido(request):
    cliente = Cliente.objects.get(usuario=request.user)
    carrito = Carrito.objects.get(cliente=cliente)

    if not carrito.items.exists():
        return redirect('detalle_carrito')  # No procesar si el carrito está vacío

    # Crear el pedido
    pedido = Pedido.objects.create(cliente=cliente, total=0, pagado=False)
    
    total = 0
    for item in carrito.items.all():
        total += item.producto.precio * item.cantidad
        PedidoItem.objects.create(pedido=pedido, producto=item.producto, cantidad=item.cantidad)

    # Actualizar el total del pedido
    pedido.total = total
    pedido.save()

    # Vaciar el carrito
    carrito.items.all().delete()

    return render(request, 'tiendacalcal/pedido_confirmado.html', {'pedido': pedido})

def actualizar_cantidad_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    
    if request.method == 'POST':
        nueva_cantidad = int(request.POST.get('cantidad'))
        if nueva_cantidad > 0:
            item.cantidad = nueva_cantidad
            item.save()
        else:
            item.delete()  # Si la cantidad es 0, eliminamos el item del carrito
    
    return redirect('detalle_carrito')

def buscar_productos(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)  # Búsqueda por nombre
    else:
        productos = Producto.objects.all()
    return render(request, 'tiendacalcal/lista_productos.html', {'productos': productos})

def lista_productos(request):
    productos_lista = Producto.objects.all()
    paginator = Paginator(productos_lista, 10)  # Mostrar 10 productos por página

    pagina = request.GET.get('page')
    productos = paginator.get_page(pagina)
    
    return render(request, 'tiendacalcal/lista_productos.html', {'productos': productos})

def filtrar_por_categoria(request, categoria_id):
    productos = Producto.objects.filter(categoria_id=categoria_id)
    return render(request, 'tiendacalcal/lista_productos.html', {'productos': productos})

def procesar_pedido(request):
    usuario = request.user
    carrito = Carrito.objects.get(usuario=usuario)
    items = carrito.items.all()
    
    if items:
        # Crear el pedido
        pedido = Pedido.objects.create(
            usuario=usuario,
            fecha=timezone.now(),
            total=carrito.calcular_total()
        )
        
        # Agregar los items del carrito al pedido
        for item in items:
            PedidoItem.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.producto.precio
            )
        
        # Vaciar el carrito después de procesar el pedido
        carrito.items.clear()
        
        # Redirigir a una página de confirmación
        return redirect('confirmacion_pedido', pedido_id=pedido.id)
    else:
        return redirect('detalle_carrito')

def historial_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'tiendacalcal/historial_pedidos.html', {'pedidos': pedidos})

def pago_simulado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        # Aquí se puede simular una respuesta de éxito o error en el pago
        return redirect('confirmacion_pedido', pedido_id=pedido.id)
    
    return render(request, 'tiendacalcal/pago_simulado.html', {'pedido': pedido})
