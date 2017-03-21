from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.ir_index, name=''),
    url(r'^index/$', views.ir_index, name=''),
    url(r'^pie/$', views.ir_pie, name=''),
    url(r'^encabezado/$', views.ir_encabezado, name=''),
    url(r'^bodega/$', views.ir_crear_bodega, name='bodega'),
    url(r'^obtenerTiposBodega/$', views.obtenerTiposBodega, name='obtenerTiposBodega'),
    url(r'^obtenerUsuarios/$', views.obtenerUsuarios, name='obtenerUsuarios'),
    url(r'^crearBodega/$', views.crearBodega, name='crearBodega'),
    url(r'^busquedaproducto/$', views.busquedaProducto, name='busquedaproducto'),
    url(r'^verproductolista/$', views.verProductoLista, name='verproductolista'),
    url(r'^bodegas/$', views.ir_bodegas, name='bodegas'),
    url(r'^obtenerBodegas/$', views.obtenerBodegas, name='obtenerBodegas'),
    url(r'^obtenerBodega/$', views.obtenerBodega, name='obtenerBodega'),
]
