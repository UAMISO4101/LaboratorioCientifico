import json
import unittest
import datetime

from django.http.request import HttpRequest

from laboratorio.models import ConteoInventario, Tipo, DetalleProductos
from laboratorio.views_conteoabc_manual import obtener_conteos_abc, obtener_conteo_abc, actualizar_conteo_fisico

"""Clase ConteoFisicoTestCase.

Clase encargada de generar las pruebas unitarias para ingresar el conteo fisico

"""
class ConteoFisicoTestCase(unittest.TestCase):

    """Metodo setUp
    Configuracion inicial de datos

    """
    def setUp(self):
        if Tipo.objects.filter(grupo="STATUSCONTEO",nombre="Ejecutada").count() == 0:
            estado = Tipo(grupo="STATUSCONTEO",
                    nombre="Ejecutada"
                    )
            estado.save()
        else:
            estado = Tipo.objects.get(grupo="STATUSCONTEO",nombre="Ejecutada")
        if Tipo.objects.filter(grupo="STATUSCONTEO", nombre="Ajustes").count() == 0:
            ajustes = Tipo(grupo="STATUSCONTEO",
                          nombre="Ajustes"
                          )
            ajustes.save()
        if Tipo.objects.filter(grupo="STATUSCONTEO", nombre="Cerrada").count() == 0:
            cerrada = Tipo(grupo="STATUSCONTEO",
                          nombre="Cerrada"
                          )
            cerrada.save()
        if Tipo.objects.filter(grupo="TIPODIFERENCIA", nombre="Exceso").count() == 0:
            tipo_diferencia1 = Tipo(grupo="TIPODIFERENCIA",
                    nombre="Exceso"
                    )
            tipo_diferencia1.save()

        if Tipo.objects.filter(grupo="TIPODIFERENCIA", nombre="Defecto").count() == 0:
            tipo_diferencia2 = Tipo(grupo="TIPODIFERENCIA",
                    nombre="Defecto"
                    )
            tipo_diferencia2.save()

        if Tipo.objects.filter(grupo="TIPODIFERENCIA", nombre="-").count() == 0:
            tipo_diferencia3 = Tipo(grupo="TIPODIFERENCIA",
                    nombre="-"
                    )
            tipo_diferencia3.save()

        cont_inventario = ConteoInventario(id=1,
                                             estado=estado,
                                             fecha_creacion=datetime.datetime.now())

        cont_inventario.save()
        detalle_producto = DetalleProductos(id=1,
                                            conteoinventario=cont_inventario,
                                            cantidad_contada=20,
                                            )

        detalle_producto.save()

    """Metodo test obtener conteos abc.

    Prueba unitaria que verifica la existencia de conteos fisico,
    Se prueba el metodo de view: views_conteoabc_manual: obtener_conteos_abc

    La respuesta debe obtener un listado de conteos fisicos en json

    """
    def test_1_obtener_conteos_abc(self):
        request = HttpRequest()
        request.method = 'GET'
        jsonResponse = obtener_conteos_abc(request)
        self.assertFalse(jsonResponse.content.__eq__("\"[]\""))

    """Metodo test existe conteo fisico.

    Prueba unitaria que verifica si existe el conteo fisico y sus correspondientes detalle producto de ese conteo,
    el metodo de view: views_conteoabc_manual: obtener_conteo_abc

    La respuesta debe contener un elemento json que representa el detalle de producto para el conteo

    """
    def test_2_obtener_conteo_abc(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET["id_conteo"] = 1
        jsonResponse = obtener_conteo_abc(request)
        self.assertFalse(jsonResponse.content.__eq__("\"[]\""))

    """Metodo test verificar ajuste.

    Prueba unitaria que verifica el ajuste del conteo fisico con sus correspondientes detalle producto de ese conteo,
    el metodo de view: views_conteoabc_manual: actualizar_conteo_fisico

    La respuesta debe contener un elemento json que representa la diferencia y tipo para ese detalle producto, NO AJUSTE
    """
    def test_3_actualizar_conteo_fisico_no_ajuste(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["id_detalle_conteo"] = "1"
        request.POST["cantidad_fisica"] = "20"
        jsonResponse = actualizar_conteo_fisico(request)
        respuesta = json.loads(jsonResponse.content)
        self.assertEquals(respuesta.items()[0][1], "0")
        self.assertEquals(respuesta.items()[3][1], "-")

    """Metodo test verificar ajuste.

    Prueba unitaria que verifica el ajuste del conteo fisico con sus correspondientes detalle producto de ese conteo,
    el metodo de view: views_conteoabc_manual: actualizar_conteo_fisico

    La respuesta debe contener un elemento json que representa la diferencia y tipo para ese detalle producto, Exceso
    """
    def test_4_actualizar_conteo_fisico_exceso(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["id_detalle_conteo"] = "1"
        request.POST["cantidad_fisica"] = "30"
        jsonResponse = actualizar_conteo_fisico(request)
        respuesta = json.loads(jsonResponse.content)
        self.assertEquals(respuesta.items()[0][1], "10")
        self.assertEquals(respuesta.items()[3][1], "Exceso")

    """Metodo test verificar ajuste.

    Prueba unitaria que verifica el ajuste del conteo fisico con sus correspondientes detalle producto de ese conteo,
    el metodo de view: views_conteoabc_manual: actualizar_conteo_fisico

    La respuesta debe contener un elemento json que representa la diferencia y tipo para ese detalle producto, Defecto
    """
    def test_5_actualizar_conteo_fisico_defecto(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["id_detalle_conteo"] = "1"
        request.POST["cantidad_fisica"] = "15"
        jsonResponse = actualizar_conteo_fisico(request)
        respuesta = json.loads(jsonResponse.content)
        self.assertEquals(respuesta.items()[0][1], "5")
        self.assertEquals(respuesta.items()[3][1], "Defecto")

"""Metodo principal de test.
"""
if __name__ == '__main__':
    unittest.main()