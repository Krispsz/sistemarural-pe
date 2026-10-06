"""SistemaRural-PE: sistema de gestión para establecimientos de salud rurales.

El sistema PARTE VACÍO y le pide cada dato a quien lo usa (registrar es una
función del sistema). Lo ingresado se guarda solo, en este mismo equipo.

Uso:
    python3 main.py                  usa datos_local.json (se crea al primer registro)
    python3 main.py --datos RUTA     usa otro archivo de datos
    python3 main.py --demo           carga datos FICTICIOS en memoria (no guarda nada)
"""

import argparse
from datetime import date, datetime

from src.arranque import RUTA_DATOS_POR_DEFECTO, crear_servicio
from src.datos_prueba import cargar_datos_prueba
from src.excepciones import DatosInvalidosError, SistemaRuralError

MENU = """
=== SistemaRural-PE ===
1. Registrar paciente
2. Registrar atención
3. Agendar cita
4. Reporte de un periodo
5. Listar pacientes
6. Ver auditoría
0. Salir
"""


def pedir(texto):
    return input(texto).strip()


def pedir_fecha(texto):
    try:
        return date.fromisoformat(pedir(texto))
    except ValueError as error:
        raise DatosInvalidosError("Use el formato AAAA-MM-DD, por ejemplo 2026-09-08.") from error


def pedir_entero(texto):
    try:
        return int(pedir(texto))
    except ValueError as error:
        raise DatosInvalidosError("Debe ingresar un número entero.") from error


def registrar_paciente(servicio):
    paciente = servicio.registrar_paciente(
        pedir("DNI (8 dígitos): "), pedir("Nombre completo: "),
        pedir_entero("Edad: "), pedir("Centro poblado: "))
    print("Paciente registrado:", paciente.descripcion())


def registrar_atencion(servicio):
    atencion = servicio.registrar_atencion(
        pedir("DNI del paciente: "), pedir("Tipo de atención: "),
        pedir_fecha("Fecha (AAAA-MM-DD): "),
        pedir("Brigada (Enter si fue en el puesto): ") or None)
    print("Atención registrada:", atencion.descripcion())


def agendar_cita(servicio):
    try:
        fecha_hora = datetime.strptime(pedir("Fecha y hora (AAAA-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
    except ValueError as error:
        raise DatosInvalidosError("Use el formato AAAA-MM-DD HH:MM.") from error
    servicio.agendar_cita(pedir("DNI del paciente: "), fecha_hora, pedir("Motivo: "))
    print("Cita agendada.")


def mostrar_reporte(servicio):
    reporte = servicio.reporte_periodo(pedir_fecha("Desde (AAAA-MM-DD): "), pedir_fecha("Hasta (AAAA-MM-DD): "))
    print(f"Total: {reporte['total']} | En brigada: {reporte['brigadas']}")
    print(f"Por centro poblado: {reporte['por_centro_poblado']}")
    for linea in reporte["lineas"]:
        print(" -", linea)


def listar_pacientes(servicio):
    pacientes = servicio.repositorio.pacientes
    print("\n".join(f" - {p.descripcion()}" for p in pacientes) or "(no hay pacientes registrados)")


def main():
    argumentos = argparse.ArgumentParser(description="SistemaRural-PE")
    argumentos.add_argument("--demo", action="store_true", help="datos ficticios en memoria, sin guardar")
    argumentos.add_argument("--datos", default=RUTA_DATOS_POR_DEFECTO, help="archivo local de datos")
    opciones = argumentos.parse_args()

    try:
        servicio, auditoria = crear_servicio(None if opciones.demo else opciones.datos)
    except SistemaRuralError as error:
        print(f"No se pudo iniciar: {error}")
        return
    if opciones.demo:
        cargar_datos_prueba(servicio)
        print("MODO DEMOSTRACIÓN: datos ficticios cargados en memoria (no se guarda nada).")

    acciones = {
        "1": lambda: registrar_paciente(servicio),
        "2": lambda: registrar_atencion(servicio),
        "3": lambda: agendar_cita(servicio),
        "4": lambda: mostrar_reporte(servicio),
        "5": lambda: listar_pacientes(servicio),
        "6": lambda: print("\n".join(auditoria.lineas) or "(sin actividad todavía)"),
    }
    while True:
        print(MENU)
        try:
            opcion = pedir("Opción: ")
        except EOFError:
            break
        if opcion == "0":
            print("Hasta luego.")
            break
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción no válida.")
            continue
        errores_previos = len(servicio.bus.errores)
        try:
            accion()
        except SistemaRuralError as error:
            print(f"No se pudo completar: {error}")
        if len(servicio.bus.errores) > errores_previos:
            print("ADVERTENCIA: no se pudo guardar en disco:", servicio.bus.errores[-1])


if __name__ == "__main__":
    main()
