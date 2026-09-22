from datetime import date

from src.paciente import Paciente
from src.atencion import Atencion

# Datos 100% ficticios, usados únicamente para desarrollo y demostración.
# Nunca deben reemplazarse por información real de pacientes.

pacientes = [
    Paciente("12345678", "Juana Ramos", 34, "Cochabamba"),
    Paciente("87654321", "Pedro Ishpilco", 61, "Uchubamba"),
    Paciente("11223344", "Rosa Chavez", 5, "Chugay Centro"),
]

atenciones = [
    Atencion(pacientes[0], "control prenatal", date(2026, 9, 8), campana="Cochabamba"),
    Atencion(pacientes[1], "consulta general", date(2026, 9, 9), campana="Uchubamba"),
    Atencion(pacientes[2], "vacunacion", date(2026, 9, 9), campana=None),
]
