from django.contrib import admin

# Register your models here.

from laboratorio.models import (Bodega, Tipo, Producto, Rol, Usuario, ProductosEnBodega,
                                Experimento, Protocolo, ProductoProtocolo, TransaccionInventario, OrdenPedido,
                                DetalleOrden, ComentarioOrden)

admin.site.register(Bodega)
admin.site.register(Tipo)
admin.site.register(Producto)
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(ProductosEnBodega)
admin.site.register(TransaccionInventario)
admin.site.register(Experimento)
admin.site.register(Protocolo)
admin.site.register(ProductoProtocolo)
admin.site.register(OrdenPedido)
admin.site.register(DetalleOrden)
admin.site.register(ComentarioOrden)