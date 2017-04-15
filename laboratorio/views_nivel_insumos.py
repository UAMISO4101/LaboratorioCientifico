from decimal import Decimal


def calcularStockSeguridad(frecuencia_minima, cantidad_uso, tiempo, numero_minimo_veces):
    if frecuencia_minima == "Continua":
        #Muchas veces al dia
        return numero_minimo_veces*cantidad_uso*tiempo
    elif frecuencia_minima == "Frecuente":
        #Al menos una vez al dia
        return cantidad_uso*tiempo
    elif frecuencia_minima == "Ocasional":
        #Al menos una vez a la semana
        diario = cantidad_uso/7
        return diario*tiempo
    elif frecuencia_minima == "PocoUsual":
        #Al menos una vez al mes (aproximando a 30 dias)
        diario = cantidad_uso/30
        return diario*tiempo
    elif frecuencia_minima == "Rara":
        #Unas pocas veces al anio
        suma = cantidad_uso*numero_minimo_veces
        diario = suma/365
        return diario*tiempo
    elif frecuencia_minima == "MuyRara":
        #Al menos una vez al anio
        diario = cantidad_uso/365
        return diario*tiempo

def calcularPuntoPedido(stock_seguridad, frecuencia_media, cantidad_media, tiempo, numero_medio_veces):
    val = calcularStockSeguridad(frecuencia_media, cantidad_media, tiempo,numero_medio_veces)
    return val + stock_seguridad