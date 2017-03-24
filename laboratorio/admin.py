from django.contrib import admin

# Register your models here.
from laboratorio.models import Bodega, Tipo, Producto, Rol, Usuario, ProductosEnBodega, TransaccionInventario

admin.site.register(Bodega)
admin.site.register(Tipo)
admin.site.register(Producto)
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(ProductosEnBodega)
admin.site.register(TransaccionInventario)