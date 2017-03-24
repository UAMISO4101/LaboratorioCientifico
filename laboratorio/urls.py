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
    url(r'^busquedaproductodetalle/$', views.busquedaProductoDetalle, name='busquedaproductodetalle'),
    url(r'^verproductobusquedadetalle/$', views.verProductoBusquedaDetalle, name='verproductobusquedadetalle'),
    url(r'^verproductobusqueda/$', views.verProductoBusqueda, name='verproductobusqueda'),
    url(r'^bodegas/$', views.ir_bodegas, name='bodegas'),
    url(r'^obtenerBodegas/$', views.obtenerBodegas, name='obtenerBodegas'),
    url(r'^obtenerBodega/$', views.obtenerBodega, name='obtenerBodega'),

    url(r'^transaccion/$', views.ir_crear_transaccion, name='transaccion'),
    url(r'^crearTransaccion/$', views.crear_transaccion, name='crearTransaccion'),
    url(r'^obtenerTipos/$', views.obtenerTipos, name='obtenerTipos'),
    url(r'^obtenerProductosBodega/$', views.obtenerProductosBodega, name='obtenerProductosBodega'),
  
    url(r'^obtenerExperimentos/$', views.obtenerExperimentos, name='obtenerExperimentos'),
    url(r'^obtenerExperimentosPorUsuario/$', views.obtenerExperimentosPorUsuario, name='obtenerExperimentosPorUsuario'),
    url(r'^obtenerProtocolosPorExperimento/$', views.obtenerProtocolosPorExperimento, name='obtenerProtocolosPorExperimento'),
    url(r'^obtenerPPPorProtocolo/$', views.obtenerPPPorProtocolo, name='obtenerPPPorProtocolo'),
    url(r'^experimentos/$', views.experimentos, name='experimentos'),

    url(r'^recursos/$', views.ir_recursos, name='recursos'),
    url(r'^registrarInsumo/$', views.ir_regitrarInsumos, name='registrarInsumo'),
    url(r'^guardarInsumo/$', views.registrarInsumoReactivo, name='guardarInsumo'),
    url(r'^obtenerTiposMedida/$', views.obtenerTiposMedida, name='obtenerTiposMedida'),
    url(r'^verRecursos/$', views.ir_ver_recursos, name='verRecursos'),
    url(r'^obtenerRecursos/$', views.obtenerRecursos, name='obtenerRecursos'),
    url(r'^editarRecurso/(?P<recurso_id>\d+)/$', views.ir_editarRecurso, name='editarRecurso'),
    url(r'obtenerRecurso/$', views.obtenerRecurso, name='obtenerRecurso'),
    url(r'^guardarEdicionInsumo/$', views.guardarEdicionInsumo, name='guardarEdicionInsumo'),
]
