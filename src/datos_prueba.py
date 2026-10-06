"""Datos 100% ficticios para desarrollo, pruebas y demostración.

Nunca deben reemplazarse por información real de pacientes (restricción de diseño 4).
"""

from datetime import date

PACIENTES = [
    ("12345678", "Juana Ramos", 34, "Cochabamba"),
    ("87654321", "Pedro Ishpilco", 61, "Uchubamba"),
    ("11223344", "Rosa Chavez", 5, "Chugay Centro"),
]

# (dni, tipo, fecha, brigada o None si fue en el puesto)
ATENCIONES = [
    ("12345678", "control prenatal", date(2026, 9, 8), "Cochabamba"),
    ("87654321", "consulta general", date(2026, 9, 9), "Uchubamba"),
    ("11223344", "vacunacion", date(2026, 9, 9), None),
]


def cargar_datos_prueba(servicio):
    """Registra los datos ficticios usando los casos de uso reales del servicio."""
    for dni, nombre, edad, centro in PACIENTES:
        servicio.registrar_paciente(dni, nombre, edad, centro)
    for dni, tipo, fecha, campana in ATENCIONES:
        servicio.registrar_atencion(dni, tipo, fecha, campana)
