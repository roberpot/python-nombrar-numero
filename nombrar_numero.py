# -*- coding: utf-8 -*-

# Copyright (C) 2016 Roberto García Carvajal
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Módulo para nombrar números enteros no negativos (en castellano).
    
    Uso: nombrar_numero(entero_no_negativo).
"""

__all__ = ['nombrar_numero']

__author__ = u'Roberto García Carvajal'


def _desempaquetar_segmento(x):
    """
        Extrae de la cadena las centenas, decenas y unidades por separado.
        Tener en cuenta que puede que la cadena tenga una longitud inferior 3.
        :param x: str de como mucho 3 caracteres.
        :return tuple: tupla de 3 enteros que representan a centenas, decenas y
         unidades.
    """
    index = 0
    c = 0
    d = 0
    u = 0
    l = len(x)
    if l > 3:
        raise ValueError(u"El segmento debe ser como mucho de longitud 3.")
    if l > 2:
        c = int(x[index])
        index += 1
    if l > 1:
        d = int(x[index])
        index += 1
    if l > 0:
        u = int(x[index])
    return c, d, u


def _nombrar_segmento(x, unidad_larga=False):
    """
        Nombra un segmento determinado. No incluye puntuación.
        :param x: str de, como mucho, 3 caracteres numéricos.
        :param unidad_larga: bool. Indica si la unidad se escribo como "uno"o 
        "un".
        :return str con la transcripción del número.
    """
    c, d, u = _desempaquetar_segmento(x)
    # Mapa para las centenas. Con cuidado de '1', que será 'cien' si decenas y 
    # unidades son 0.
    c_dict = {
        0: u"",
        1: ((d + u) > 0 and u"ciento" or u"cien"),
        2: u"doscientos",
        3: u"trescientos",
        4: u"cuatrocientos",
        5: u"quinientos",
        6: u"seiscientos",
        7: u"setecientos",
        8: u"ochocientos",
        9: u"novecientos",
    }
    # Mapa para decenas, con cuidado de que las unidades sean 0.
    d_dict = {
        0: u"",
        1: (u and u"dieci" or u"diez"),
        2: (u and u"veinti" or u"veinte"),
        3: (u and u"treinta y " or u"treinta"),
        4: (u and u"cuarenta y " or u"cuarenta"),
        5: (u and u"cincuenta y " or u"cincuenta"),
        6: (u and u"sesenta y " or u"sesenta"),
        7: (u and u"setenta y " or u"setenta"),
        8: (u and u"ochenta y " or u"ochenta"),
        9: (u and u"noventa y " or u"noventa"),
    }
    # Mapa de unidades, teniendo en cuenta la unidad_larga.
    # Además, si las decenas es 2, algunos números llevan tildes.
    u_dict = {
        0: u"",
        1: (unidad_larga and u"uno") or (d == 2 and u"ún") or u"un",
        2: (d == 2 and u"dós") or u"dos",
        3: (d == 2 and u"trés") or u"tres",
        4: u"cuatro",
        5: u"cinco",
        6: (d in (1, 2) and u"séis") or u"seis",
        7: u"siete",
        8: u"ocho",
        9: u"nueve",
    }
    c_res = c_dict[c]
    d_u_res = d_dict[d] + u_dict[u]
    # Caso especial de los números entre 11 y 15.
    if d == 1 and 0 < u < 6:
        d_u_res = {
            11: u"once",
            12: u"doce",
            13: u"trece",
            14: u"catorce",
            15: u"quince",
        }[10 + u]
    # Sólo incluimos separador si las dos partes del segmento tienen valores.
    separator = u""
    if c_res and d_u_res:
        separator = u" "
    return c_res + separator + d_u_res


def nombrar_numero(x):
    """
        Convierte un número a su formato escrito. Sólo acepta números enteros 
        no negativos.
        :param x: int, entero no negativo a convertir a formato escrito.
        :return unicode: devuelve el número en formato alfabético.
    """
    # Comprobación del tipo.
    if not isinstance(x, int):
        raise ValueError(u"Tipo incorrecto. Se esperaba int, encontrado %s" %
                         x.__class__.__name__)
    # Comprobación de signo.
    if x < 0:
        raise ValueError(u"Se esperaba un entero no negativo.")
    if x == 0:
        return u"cero"
    # Ahora vamos a trocear el número en grupos de 3 en 3, empezando desde la 
    # derecha y tomando nota del número de segmentos que tiene el número. 
    # Almacenamos los segmentos en una lista de cadenas en orden inverso. 
    # Ejemplos:
    # 1 -> ["1"]
    # 4234 -> ["234", "4"]
    # 10001 -> ["001", "10"]
    xx = u"%s" % x
    xx = xx[::-1]
    l = len(xx) / 3 + {False: 0, True: 1}[(len(xx) % 3) > 0]
    vx = []
    for i in range(0, l):
        vx.append(xx[3 * i:3 * (i + 1)][::-1])
    # vx = vx[::-1]

    resultado = u""
    mapa_sufijos_singular = {
        0: u"",
        1: u"mil",
        2: u"millón",
        3: u"mil",
        4: u"billón",
        5: u"mil",
        6: u"trillón",
    }
    mapa_sufijos_plural = {
        0: u"",
        1: u"mil",
        2: u"millones",
        3: u"mil",
        4: u"billones",
        5: u"mil",
        6: u"trillones",
    }
    # Recorremos los segmentos. Recordar que vamos a nombrar el número por 
    # grupos de tres desde la derecha, añadiendo el sufijo según puntuación, si
    # corresponde.
    for index, v in enumerate(vx):
        resultado_segmento = _nombrar_segmento(v, unidad_larga=(index == 0))
        # Si el segmento es de millares y el resultado tiene valor o el segmento
        # es de millones, se añade el sufijo. Ejemplos:
        # - Para 1000001, segmentos '1', '000', '001'. Si estamos en el segmento
        #   '000', no deberíamos de poner 'mil'.
        # - Para 1000020001, segmentos '1', '000', '020', '001'. Si estamos en
        #   el segmento '000', deberíamos de poner "millones".
        if (resultado_segmento or (index % 2) == 0) and index > 0:
            resultado_segmento += u" "
            # Distinguimos entre singular o plural.
            if resultado_segmento == u"un ":
                # Si el resultado es un 1 y estamos nombrando millares, lo
                # dejamos vacío. Es decir: para 1000 no vamos a decir
                # 'un mil', sino sólo mil.
                if (index % 2) == 1:
                    resultado_segmento = mapa_sufijos_singular[index]
                else:
                    resultado_segmento += mapa_sufijos_singular[index]
            else:
                resultado_segmento += mapa_sufijos_plural[index]
        if resultado_segmento:
            resultado = u" " + resultado_segmento + resultado
    # Probablemente queden espacios a la izquierda (un mínimo de 1). 
    # Los eliminamos.
    return resultado.lstrip()
