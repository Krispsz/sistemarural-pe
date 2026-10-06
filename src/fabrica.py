"""Patrón Factory: decide qué tipo de atención crear."""

from src.atencion import AtencionBrigada, AtencionEnPuesto


class FabricaAtenciones:
    """Centraliza la creación de atenciones.

    Quien registra una atención no necesita conocer las subclases: si mañana
    existe un tercer tipo (p. ej. visita domiciliaria) solo cambia esta clase.
    """

    @staticmethod
    def crear(paciente, tipo, fecha, campana=None, personal=None):
        if isinstance(campana, str) and campana.strip():
            return AtencionBrigada(paciente, tipo, fecha, campana, personal)
        return AtencionEnPuesto(paciente, tipo, fecha, personal)
