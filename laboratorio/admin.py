from django.contrib import admin

# Register your models here.
from laboratorio.models import Bodega, TipoBodega, Producto, Rol, Usuario

admin.site.register(Bodega)
admin.site.register(TipoBodega)
admin.site.register(Producto)
admin.site.register(Rol)
admin.site.register(Usuario)