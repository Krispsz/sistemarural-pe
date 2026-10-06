"""Demostración AUTOMÁTICA con datos ficticios (para evidencia y pruebas de humo).

El sistema real es main.py: parte vacío y pide los datos a quien lo usa."""

from datetime import date, datetime

from src.arranque import crear_servicio
from src.datos_prueba import cargar_datos_prueba
from src.excepciones import SistemaRuralError


def main():
    servicio, auditoria = crear_servicio()  # solo en memoria: no toca ningún archivo

    print("=== SistemaRural-PE: Puesto de Salud Mushit (Chugay) ===\n")
    cargar_datos_prueba(servicio)
    print(f"Pacientes registrados: {len(servicio.repositorio.pacientes)}")
    for paciente in servicio.repositorio.pacientes:
        print(" -", paciente.descripcion())

    print("\n--- Agenda (RF2) ---")
    servicio.agendar_cita("12345678", datetime(2026, 10, 7, 9, 0), "control prenatal")
    print("Cita agendada el 07/10/2026 a las 09:00.")
    try:
        servicio.agendar_cita("87654321", datetime(2026, 10, 7, 9, 0), "consulta general")
    except SistemaRuralError as error:
        print(f"Error controlado: {error}")

    print("\n--- Reporte semanal para la Red de Salud (RF4, RF5) ---")
    reporte = servicio.reporte_periodo(date(2026, 9, 8), date(2026, 9, 14))
    print(f"Total de atenciones: {reporte['total']} (en brigada: {reporte['brigadas']})")
    print(f"Por centro poblado: {reporte['por_centro_poblado']}")
    for linea in reporte["lineas"]:
        print(" -", linea)

    print("\n--- Auditoría por eventos (sin DNI en texto plano) ---")
    for linea in auditoria.lineas:
        print(" -", linea)

    print("\n--- Verificación Ley N.° 29733 ---")
    paciente = servicio.repositorio.buscar_por_dni("12345678")
    print(f"repr(paciente) = {paciente!r}")
    print(f"El DNI completo aparece en la representación: {'12345678' in repr(paciente)}")


if __name__ == "__main__":
    main()
