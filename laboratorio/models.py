from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Rol(models.Model):
    nombre = models.CharField(max_length=100)

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=1000)
    imageFile = models.ImageField(upload_to='images', null=True,  blank=True)
    roles = models.ManyToManyField(Rol)

class TipoBodega(models.Model):
    nombre = models.CharField(max_length=100, unique=True, null=True)

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
    tipo_bodega = models.ForeignKey(TipoBodega, null=True)
    usuario = models.ForeignKey(Usuario, null=True)

class Producto(models.Model):
    codigo = models.CharField(max_length=10, unique= True, null= True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    valorUnitario = models.DecimalField(max_digits=7,decimal_places=4)
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
    unidadMedida_choices = (
        ('mg', 'Miligramos'),
        ('g', 'Gramos'),
        ('kg', 'Kilogramos'),
        ('ml', 'Mililitros'),
        ('l', 'Litros'),
        ('unknown', 'unknown'),)
    unidadMedida = models.CharField(max_length=10, choices=unidadMedida_choices, default='unknown')
    imageFile = models.ImageField(upload_to='images', null=True, blank=True)
