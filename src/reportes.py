"""Programación funcional: reportes con funciones de orden superior (RF4, RF5).

Todas las funciones son puras: reciben colecciones y devuelven resultados
nuevos, sin modificar nada (sin efectos secundarios).
"""

from collections import Counter
from functools import reduce

from src.excepciones import DatosInvalidosError


def filtrar_atenciones_campana(atenciones):
    """Se queda solo con las atenciones ligadas a una brigada itinerante."""
    return list(filter(lambda a: a.campana is not None, atenciones))


def generar_reporte(atenciones_campana):
    """Transforma cada atención en una línea de reporte, protegiendo el DNI."""
    return list(map(
        lambda a: f"{a.paciente.get_dni_enmascarado()} | {a.tipo} | brigada: {a.campana}",
        atenciones_campana
    ))


def contar_atenciones(atenciones):
    """Cuenta atenciones acumulando con reduce()."""
    return reduce(lambda acc, a: acc + 1, atenciones, 0)


def filtrar_por_periodo(atenciones, inicio, fin):
    """Atenciones cuya fecha está entre inicio y fin (ambos incluidos)."""
    return list(filter(lambda a: inicio <= a.fecha <= fin, atenciones))


def contar_por_centro_poblado(atenciones):
    """Diccionario {centro poblado: cantidad}, calculado en una sola pasada.

    Counter + map evita el reduce con copia de diccionario en cada elemento
    (costo O(n * k)); aquí el costo es O(n) y casi no usa memoria extra.
    """
    return dict(Counter(map(lambda a: a.paciente.centro_poblado, atenciones)))


def generar_reporte_periodo(atenciones, inicio, fin):
    """Reporte de atención para la Red de Salud (RF4) en un periodo dado."""
    if inicio > fin:
        raise DatosInvalidosError("La fecha de inicio no puede ser posterior a la fecha de fin.")
    en_periodo = sorted(filtrar_por_periodo(atenciones, inicio, fin), key=lambda a: a.fecha)
    return {
        "periodo": (inicio, fin),
        "total": contar_atenciones(en_periodo),
        "brigadas": contar_atenciones(filtrar_atenciones_campana(en_periodo)),
        "por_centro_poblado": contar_por_centro_poblado(en_periodo),
        "lineas": list(map(
            lambda a: f"{a.fecha.isoformat()} | {a.paciente.get_dni_enmascarado()} | "
                      f"{a.tipo} | {a.campana or 'puesto'}",
            en_periodo
        )),
    }
