"""Funciones de orden superior para generar reportes (RF4, RF5)."""

from functools import reduce


def filtrar_atenciones_campana(atenciones):
    """Se queda solo con las atenciones ligadas a una brigada itinerante."""
    return list(filter(lambda a: a.campana is not None, atenciones))


def generar_reporte(atenciones_campana):
    """Transforma cada atencion en una linea de reporte, protegiendo el DNI."""
    return list(map(
        lambda a: f"{a.paciente.get_dni_enmascarado()} | {a.tipo} | brigada: {a.campana}",
        atenciones_campana
    ))


def contar_atenciones(atenciones_campana):
    """Cuenta atenciones de campaña acumulando con reduce()."""
    return reduce(lambda acc, a: acc + 1, atenciones_campana, 0)
