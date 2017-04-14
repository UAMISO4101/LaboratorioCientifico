from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from laboratorio import views_orden_pedido, views_busqueda_producto, views_vencimiento_productos
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
    url(r'^bodegas/$', views.ir_bodegas, name='bodegas'),
    url(r'^obtenerBodegas/$', views.obtenerBodegas, name='obtenerBodegas'),
    url(r'^obtenerBodega/$', views.obtenerBodega, name='obtenerBodega'),
    url(r'^obtenerTipo/$', views.obtenerTipo, name='obtenerTipo'),
    url(r'^obtenerUnidadesMedida/$', views.obtenerUnidadesMedida, name='obtenerUnidadesMedida'),

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
    url(r'^obtenerProveedores/$', views.obtenerProveedores, name='obtenerProveedores'),

    url(r'^obtenerTransacciones/$', views.obtenerTransacciones, name='obtenerTransacciones'),
    url(r'^transacciones/$', views.ir_transacciones, name='transacciones'),

    url(r'^busquedaproducto/$', views_busqueda_producto.busqueda_producto, name='busquedaproducto'),
    url(r'^busquedaproductodetalle/$', views_busqueda_producto.busqueda_producto_detalle, name='busquedaproductodetalle'),
    url(r'^verproductobusquedadetalle/$', views_busqueda_producto.ver_producto_busqueda_detalle, name='verproductobusquedadetalle'),
    url(r'^verproductobusqueda/$', views_busqueda_producto.ver_producto_busqueda, name='verproductobusqueda'),
    url(r'^obtenerlistaproductos/$', views_busqueda_producto.llenar_listado_productos_busqueda, name='obtenerlistaproductos'),
    url(r'^obtenerlistabodegas/$', views_busqueda_producto.llenar_listado_bodegas_busqueda, name='obtenerlistabodegas'),
    url(r'^convertirUnidad/$', views.convertirUnidad, name='convertirUnidad'),

    url(r'^verordenespedido/$', views_orden_pedido.ir_ver_ordenes_pedido, name='verordenespedido'),
    url(r'^actordenpedido/$', views_orden_pedido.ir_act_orden_pedido, name='actordenpedido'),
    url(r'^ordenpedido/$', views_orden_pedido.ir_orden_pedido, name='ordenpedido'),
    url(r'^obtenerSoloUsuarios/$', views_orden_pedido.obtenerSoloUsuarios, name='obtenerSoloUsuarios'),
    url(r'^obtenerEstadosOP/$', views_orden_pedido.obtenerEstadosOP, name='obtenerEstadosOP'),
    url(r'^obtenerFechaActual/$', views_orden_pedido.obtener_fecha_actual, name='obtenerFechaActual'),
    url(r'^crearOPedido/$', views_orden_pedido.crear_orden_pedido, name='crearOPedido'),
    url(r'^obtener_op/$', views_orden_pedido.obtener_op, name='obtener_op'),
    url(r'^obtenerFP/$', views_orden_pedido.obtener_fecha_peticion_op, name='obtenerFP'),
    url(r'^obtenerOrdenesPedido/$', views_orden_pedido.obtenerOrdenesPedido, name='obtenerOrdenesPedido'),

    url(r'^vencidos/$', views_vencimiento_productos.ver_vencimiento_producto, name='ver_vencimiento_producto'),
    url(r'^vencidoslista/$', views_vencimiento_productos.lista_vencidos, name='lista_vencidos'),
]
