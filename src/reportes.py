"""Funciones de orden superior para generar reportes (RF4, RF5)."""


def filtrar_atenciones_campana(atenciones):
    """Se queda solo con las atenciones ligadas a una brigada itinerante."""
    return list(filter(lambda a: a.campana is not None, atenciones))
