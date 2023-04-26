import itertools
import json
import os
from models.tables import SorteosGuardados
from database.db import db


def generar_combinaciones(numeros_repitidos_a_buscar):
    assert 3 <= numeros_repitidos_a_buscar <= 7, "El número debe estar entre 3 y 7."

    sorteos_guardados = SorteosGuardados.query.all()
    data = []

    for sorteo in sorteos_guardados:
        data.append({sorteo.fecha: json.loads(sorteo.resultados)})

    combinaciones = {}
    for idx1, dic1 in enumerate(data):
        for idx2, dic2 in enumerate(data):
            if idx1 == idx2:
                continue

            key1, numeros1 = list(dic1.items())[0]
            key2, numeros2 = list(dic2.items())[0]

            comun = set(numeros1).intersection(numeros2)
            for comb in itertools.combinations(comun, numeros_repitidos_a_buscar):
                combinaciones[comb] = combinaciones.get(comb, set())
                combinaciones[comb].add(key1)
                combinaciones[comb].add(key2)

    combinaciones_por_repeticion = {}
    for comb, fechas in combinaciones.items():
        repeticiones = len(fechas)
        combinacion_numeros = ', '.join(map(str, comb))
        fechas_str = ', '.join(sorted(fechas))
        combinaciones_por_repeticion[repeticiones] = combinaciones_por_repeticion.get(repeticiones, [])
        combinaciones_por_repeticion[repeticiones].append((combinacion_numeros, fechas_str))

    resultado_texto = ""
    if combinaciones:
        for repeticiones in sorted(combinaciones_por_repeticion.keys(), reverse=True):
            resultado_texto += f"Se repiten {repeticiones} veces las siguientes combinaciones:<br>"
            for combinacion_numeros, fechas_str in combinaciones_por_repeticion[repeticiones]:
                resultado_texto += f"La combinación de números {combinacion_numeros}<br>"
                resultado_texto += f"Las fechas en las que se repite la combinación de números anterior son las siguientes: {fechas_str}<br>"
                resultado_texto += "<br>"
    else:
        resultado_texto = f"No se ha encontrado que al menos {numeros_repitidos_a_buscar} números se repitan a lo largo de las fechas ingresadas."

    return resultado_texto
