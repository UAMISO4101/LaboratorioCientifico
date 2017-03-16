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
    nombre = models.CharField(max_length=100, unique=True)

class Bodega(models.Model):
    serial = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    tipo_bodega = models.ForeignKey(TipoBodega)
    numero_bandejas = models.IntegerField()
    cupo_bandeja = models.IntegerField()
    temperatura_minima = models.DecimalField(max_digits=2, decimal_places=2)
    temperatura_media = models.DecimalField(max_digits=2, decimal_places=2)
    estado = models.BooleanField()
    limite = models.IntegerField()
    usuario_creacion = models.IntegerField()
    usuario_actualizacion = models.IntegerField()
    fecha_creacion = models.DateTimeField()
    fecha_actualizacion = models.DateTimeField()