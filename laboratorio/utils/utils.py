from laboratorio.models import Tipo

class Utils(object):

    @staticmethod
    def conversion(cantidad, medidaOrigen, medidaDestino):

        tipo = Tipo.objects.get(grupo__contains='CONVERSION', nombre=medidaOrigen, medidaDestino=medidaDestino)
        valor = tipo.valor
        res = cantidad*valor
        return res