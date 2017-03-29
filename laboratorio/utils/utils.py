from decimal import Decimal

from laboratorio.models import Tipo

"""Clase utilidades que servira para cualquier funcionalidad de la aplicacion
"""
class utils(object):

    """Metodo estatico convertir

    HU: 4 y 12 Convertir de una unidad a otra
    Sirve para convertir una cantidad de una medida origen a una destino

    cantidad, cantidad a convertir
    medidaOrigen, es la unidad de medida como viene originalmente la cantidad
    medidaDestino, es la unidad de medidad que se convertira la unidad
    return cantidad convertida
    """
    @staticmethod
    def convertir(cantidad, medidaOrigen, medidaDestino):

        tipo = Tipo.objects.filter(grupo__contains='CONVERSION', nombre=medidaOrigen, medidaDestino=medidaDestino).first()
        valor = tipo.valor
        res = Decimal(cantidad)*valor
        return res