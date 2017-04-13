# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
"""Clase - Modelo Rol.
"""
class Rol(models.Model):
    nombre = models.CharField(max_length=100)

"""Clase - Modelo Usuario.
"""
class Usuario(AbstractUser):
    telefono = models.CharField(max_length=1000)
    imageFile = models.ImageField(upload_to='images', null=True,  blank=True)
    roles = models.ManyToManyField(Rol)

"""Clase - Modelo Tipo.
"""
class Tipo(models.Model):
    grupo = models.CharField(max_length=100, null=True)
    nombre = models.CharField(max_length=100, null=True)
    medidaDestino = models.CharField(max_length=100, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=8, null=True)

"""Clase - Modelo Bodega.
"""
class Bodega(models.Model):
    serial = models.CharField(max_length=50, unique=True, null=True)
    nombre = models.CharField(max_length=100, null=True)
    ubicacion = models.CharField(max_length=100, null=True)
    niveles = models.IntegerField(null=True)
    secciones = models.IntegerField(null=True)
    temperatura_minima = models.DecimalField(null=True, max_digits=11,decimal_places=8)
    temperatura_media = models.DecimalField(null=True, max_digits=11,decimal_places=8)
    estado = models.BooleanField(default=True)
    usuario_creacion = models.IntegerField(null=True)
    usuario_actualizacion = models.IntegerField(null=True)
    fecha_creacion = models.DateTimeField(null=True)
    fecha_actualizacion = models.DateTimeField(null=True)
    unidad_medida = models.ForeignKey(Tipo, null=True)
    tipo_bodega = models.ForeignKey(Tipo, related_name="BODEGA", null=True)  # Segun el excel se toma el nombre BODEGA
    usuario = models.ForeignKey(Usuario, null=True)

"""Clase - Modelo Producto.
"""
class Producto(models.Model):
    codigo = models.CharField(max_length=10, unique= True, null= True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    valorUnitario = models.IntegerField()
    unidadesExistentes = models.IntegerField()
    clasificacion_choices = (
        ('Materiales Vivos',(
                ('Bac', 'Bacterias'),
                ('Hon', 'Hongos'),
            )
         ),
        ('Medios de Cultivo', (
                ('Glu', 'Glucosa'),
                ('Fru', 'Fructuosa'),
                ('Tri', 'Triptona'),
                ('Pep', 'Peptona'),
            )
         ),
        ('Micronutrientes', (
                ('Fe', 'Hierro'),
                ('Mg', 'Magnesio'),
                ('P', 'Fosforo'),
            )
         ),
        ('Manipulacion ADN y Proteinas', (
                ('Pri', 'Primers'),
                ('Kem', 'Kits de extraccion metagenomica'),
                ('KeADN', 'Kits de extraccion ADN aislado'),
                ('Pup', 'Purificador de proteinas'),
                ('Enr', 'Enzimas de restriccion'),
                ('Pro', 'Proteasas'),
            )
         ),
        ('Otros', 'Moleculas genericas'),
    )
    clasificacion = models.CharField(max_length=35,choices=clasificacion_choices)
    unidad_medida = models.ForeignKey(Tipo, related_name="prod_tipo_unidadmedida", null=True)  # Segun TransaccionInventario.unidad_medida, seria tipo_unidadmedida
    unidad_unitaria = models.DecimalField(max_digits=11,decimal_places=8, null=True)
    imageFile = models.ImageField(upload_to='images', null=True, blank=True)
    proveedor = models.ForeignKey(Usuario, null=True)

"""Clase - Modelo ProductosEnBodega.
"""
class ProductosEnBodega(models.Model):
    bodega = models.ForeignKey(Bodega, null=True)
    producto = models.ForeignKey(Producto, null=True)
    nivel = models.IntegerField(null=True)
    seccion = models.IntegerField(null=True)
    cantidad = models.IntegerField(null=True)
    unidad_medida = models.ForeignKey(Tipo, related_name="prodbod_tipo_unidadmedida", null=True)
    # Sprint2 fecha_vencimiento. Por aplicación se validará que los Productos que deban tener fecha de vencimiento sean
    # los que están en control del Jefe de Bodega, es decir los que en su historial de transacciones
    # NO figure un TIPOTRX "Traslado a experimento", "Devolucion a proveedor", "Mover por perdida o desperdicio" o
    # "Devolucion a proveedor"
    fecha_vencimiento = models.DateField(null=True)

"""Clase - Modelo TransaccionInventario.
"""
class TransaccionInventario(models.Model):
    fecha_creacion = models.DateTimeField(null=False)
    fecha_ejecucion = models.DateTimeField(null=False)
    tipo = models.ForeignKey(Tipo, related_name="TIPOTRX", null=True)
    estado = models.ForeignKey(Tipo, related_name="STATUSTRX", null=True)
    bodega_origen = models.ForeignKey(Bodega, related_name="bodegaOrigen",null=False)
    bodega_destino = models.ForeignKey(Bodega, related_name="bodegaDestino",null=False)
    producto_bodega_origen = models.ForeignKey(ProductosEnBodega, related_name="ubucacionOrigen", null=True)
    producto_bodega_destino = models.ForeignKey(ProductosEnBodega, related_name="ubucacionDestino", null=True)
    nivel_origen = models.IntegerField(null=True)
    seccion_origen = models.IntegerField(null=True)
    nivel_destino = models.IntegerField(null=True)
    seccion_destino = models.IntegerField(null=True)
    producto = models.ForeignKey(Producto, null=True)
    cantidad = models.IntegerField(null=False,default=0)
    unidad_medida = models.ForeignKey(Tipo, related_name="trx_tipo_unidadmedida", null=True)
    usuario = models.ForeignKey(Usuario, related_name="usuarioTrx", null=True)
    autoriza = models.ForeignKey(Usuario, related_name="autorizaTrx", null=True)
    comentarios = models.CharField(max_length=200, null=True)

"""Clase - Modelo Protocolo.
"""
class Protocolo(models.Model):

    version = models.BigIntegerField(null=True)
    nombre = models.CharField(max_length=50)
    fecha = models.DateField(null=True)
    descripcion = models.CharField(max_length=1000)

"""Clase - Modelo ProductoProtocolo.
"""
class ProductoProtocolo(models.Model):

    descripcion = models.CharField(max_length=50)
    cantidadUtilizada = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    protocolo = models.ForeignKey(Protocolo, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, null=True)

"""Clase - Modelo Experimento.
"""
class Experimento(models.Model):

    codigo = models.CharField(max_length=10, unique=True, null=True)
    nombre = models.CharField(max_length=50)
    fecha = models.DateField(null=True)
    estado = models.CharField(max_length=50)
    protocolo = models.ManyToManyField(Protocolo)
    asignado = models.ManyToManyField(Usuario)

"""Clase - Orden de Pedido.
"""
class OrdenPedido(models.Model):
    fecha_peticion = models.DateTimeField(null=True)
    fecha_recepcion = models.DateTimeField(null=True)
    observaciones = models.CharField(max_length=500)
    usuario_creacion = models.ForeignKey(Usuario, related_name="op_usuario_creacion", null=True)
    usuario_aprobacion = models.ForeignKey(Usuario, related_name="op_usuario_aprobacion", null=True)
    proveedor = models.ForeignKey(Usuario, related_name="op_proveedor", null=True)
    notas_aprobacion = models.CharField(max_length=500)
    estado = models.ForeignKey(Tipo, related_name="op_estado", null=True)

"""Clase - Detalle Orden Pedido.
"""
class DetalleOrden(models.Model):
    producto = models.ForeignKey(Producto, null=True)
    cantidad = models.DecimalField(null=True, max_digits=11, decimal_places=8)
    estado = models.ForeignKey(Tipo, related_name="do_estado", null=True)
    transaccion_inventario = models.ForeignKey(TransaccionInventario, related_name="do_transaccion", null=True)
    fecha_movimiento = models.DateTimeField(null=True)
    bodega = models.ForeignKey(Bodega, null=True)
    nivel_bodega_destino = models.IntegerField(null=True)
    seccion_bodega_destino = models.IntegerField(null=True)