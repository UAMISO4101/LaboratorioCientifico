from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from laboratorio import views_orden_pedido, views_busqueda_producto, views_vencimiento_productos, views_nivel_insumos, \
    views_bodegas, views_usuarios, views_transacciones, views_recursos, views_orden_reposicion
from . import views

urlpatterns = [
    url(r'^$', views.ir_index, name=''),
    url(r'^index/$', views.ir_index, name=''),
    url(r'^pie/$', views.ir_pie, name=''),
    url(r'^encabezado/$', views.ir_encabezado, name=''),
    url(r'^bodega/$', views_bodegas.ir_crear_bodega, name='bodega'),
    url(r'^obtenerTiposBodega/$', views_bodegas.obtenerTiposBodega, name='obtenerTiposBodega'),
    url(r'^obtenerUsuarios/$', views_usuarios.obtenerUsuarios, name='obtenerUsuarios'),
    url(r'^crearBodega/$', views_bodegas.crearBodega, name='crearBodega'),
    url(r'^bodegas/$', views_bodegas.ir_bodegas, name='bodegas'),
    url(r'^obtenerBodegas/$', views_bodegas.obtenerBodegas, name='obtenerBodegas'),
    url(r'^obtenerBodegas/(?P<tipo_bodega>\D+)$', views_bodegas.obtenerBodegas, name='obtenerBodegas'),
    url(r'^obtenerBodega/$', views_bodegas.obtenerBodega, name='obtenerBodega'),
    url(r'^obtenerTipo/$', views.obtenerTipo, name='obtenerTipo'),
    url(r'^obtenerUnidadesMedida/$', views.obtenerUnidadesMedida, name='obtenerUnidadesMedida'),

    url(r'^transaccion/$', views_transacciones.ir_crear_transaccion, name='transaccion'),
    url(r'^crearTransaccion/$', views_transacciones.crear_transaccion, name='crearTransaccion'),
    url(r'^obtenerTipos/$', views.obtenerTipos, name='obtenerTipos'),
    url(r'^obtenerProductosBodega/$', views.obtenerProductosBodega, name='obtenerProductosBodega'),

    url(r'^obtenerExperimentos/$', views.obtenerExperimentos, name='obtenerExperimentos'),
    url(r'^obtenerExperimentosPorUsuario/$', views.obtenerExperimentosPorUsuario, name='obtenerExperimentosPorUsuario'),
    url(r'^obtenerProtocolosPorExperimento/$', views.obtenerProtocolosPorExperimento, name='obtenerProtocolosPorExperimento'),
    url(r'^obtenerPPPorProtocolo/$', views.obtenerPPPorProtocolo, name='obtenerPPPorProtocolo'),
    url(r'^experimentos/$', views.experimentos, name='experimentos'),

    url(r'^recursos/$', views_recursos.ir_recursos, name='recursos'),
    url(r'^registrarInsumo/$', views_recursos.ir_regitrarInsumos, name='registrarInsumo'),
    url(r'^guardarInsumo/$', views_recursos.registrarInsumoReactivo, name='guardarInsumo'),
    url(r'^obtenerTiposMedida/$', views.obtenerTiposMedida, name='obtenerTiposMedida'),
    url(r'^verRecursos/$', views_recursos.ir_ver_recursos, name='verRecursos'),
    url(r'^obtenerRecursos/$', views_recursos.obtenerRecursos, name='obtenerRecursos'),
    url(r'^editarRecurso/(?P<recurso_id>\d+)/$', views_recursos.ir_editarRecurso, name='editarRecurso'),
    url(r'obtenerRecurso/$', views_recursos.obtenerRecurso, name='obtenerRecurso'),
    url(r'^guardarEdicionInsumo/$', views_recursos.guardarEdicionInsumo, name='guardarEdicionInsumo'),
    url(r'^obtenerProveedores/$', views_usuarios.obtenerProveedores, name='obtenerProveedores'),

    url(r'^obtenerTransacciones/$', views_transacciones.obtenerTransacciones, name='obtenerTransacciones'),
    url(r'^transacciones/$', views_transacciones.ir_transacciones, name='transacciones'),

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
    url(r'^obtenerProductos/$', views_orden_pedido.obtenerProductos, name='obtenerProductos'),
    url(r'^modal_do/$', views_orden_pedido.ir_modal_do, name=''),
    url(r'^guardarOrdenDetalle/$', views_orden_pedido.guardarOrdenDetalle, name='guardarOrdenDetalle'),
    url(r'^obtenerDetalleOrden/$', views_orden_pedido.obtener_do, name='obtenerDetalleOrden'),
    url(r'^recibirordenpedido/$', views_orden_pedido.ir_recibir_orden_pedido, name='recibirordenpedido'),
    url(r'^recibirOrdenDetalle/$', views_orden_pedido.ejecutar_transacciones_orden, name='recibirOrdenDetalle'),
    url(r'^procesoAprobacionOrden/$', views_orden_pedido.proceso_aprobacion_orden, name='procesoAprobacionOrden'),
    url(r'^aprobarOrden/$', views_orden_pedido.aprobar_orden, name='aprobarOrden'),
    url(r'^rechazarOrden/$', views_orden_pedido.rechazar_orden, name='rechazarOrden'),
    url(r'^obtenerComentariosOrden/$', views_orden_pedido.obtener_comentarios_orden, name='obtenerComentariosOrden'),
    url(r'^enProveedor/$', views_orden_pedido.cambiar_aprobada_en_proveedor, name='enProveedor'),

    url(r'^nivelInsumo/(?P<id>\d+)$',views_nivel_insumos.ir_nivel_insumos, name='nivelInsumo'),
    url(r'^nivelActual/$', views_nivel_insumos.recalcular_nivel_actual_, name='nivelActual'),
    url(r'^historialNivel/$', views_nivel_insumos.historial_nivel, name='historialNivel'),

    url(r'^vencidos/$', views_vencimiento_productos.ver_vencimiento_producto, name='ver_vencimiento_producto'),
    url(r'^vencidoslista/$', views_vencimiento_productos.lista_vencidos, name='lista_vencidos'),

    url(r'^crearOrdenReposicion/$', views_orden_reposicion.crearOrdenPedido, name='crearOrdenReposicion'),
    url(r'^obtenerInfoProducto/$', views_orden_reposicion.obtenerInfoProducto, name='obtenerInfoProducto'),
    url(r'^modal_or/$', views_orden_reposicion.ir_modal_or, name=''),
    url(r'^guardarDetalleOrdenReposicion/$', views_orden_reposicion.guardarDetalleOrdenReposicion, name='guardarDetalleOrdenReposicion'),
    url(r'^fechaPeticionOrRep/$', views_orden_reposicion.fechaPeticionOrdenReposicion, name='fechaPeticionOrRep'),
]
