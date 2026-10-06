"""Excepciones propias del dominio de SistemaRural-PE.

Todas heredan de SistemaRuralError, de modo que la interfaz puede capturar
cualquier error controlado con un solo `except` sin ocultar fallos inesperados.
"""


class SistemaRuralError(Exception):
    """Base de todos los errores controlados del sistema."""


class DatosInvalidosError(SistemaRuralError):
    """Un dato ingresado no cumple las reglas de validación."""


class CitaDuplicadaError(SistemaRuralError):
    """Ya existe una cita agendada en ese mismo horario (RF2)."""


class PacienteNoEncontradoError(SistemaRuralError):
    """No existe un paciente registrado con el DNI indicado."""
