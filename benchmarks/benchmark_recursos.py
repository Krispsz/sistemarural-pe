"""Mide tiempo y memoria del sistema con un volumen MAYOR al de un puesto real.

Un puesto como Mushit atiende ~120 pacientes por semana (~6 000 al año). Aquí se
simulan 5 000 pacientes y 20 000 atenciones para comprobar que el sistema
sigue siendo ágil en un equipo modesto (restricción de diseño 3).

Uso:  python3 benchmarks/benchmark_recursos.py
"""

import subprocess
import sys
import tempfile
import time
import tracemalloc
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from src.repositorio import RepositorioClinico  # noqa: E402
from src.servicio import ServicioClinico  # noqa: E402

N_PACIENTES, N_ATENCIONES = 5000, 20000
CENTROS = ["Cochabamba", "Uchubamba", "Chugay Centro", "Huaylillas", "Shiracmaca"]
BASE = date(2026, 9, 1)


def poblar():
    RepositorioClinico.reiniciar()
    servicio = ServicioClinico()
    for i in range(N_PACIENTES):
        servicio.registrar_paciente(f"{i:08d}", f"Paciente {i}", 20 + i % 60, CENTROS[i % 5])
    for j in range(N_ATENCIONES):
        servicio.registrar_atencion(f"{j % N_PACIENTES:08d}", "control", BASE + timedelta(days=j % 30),
                                    CENTROS[j % 5] if j % 3 == 0 else None)
    return servicio


def rss_maximo_mb(comando, entrada=""):
    """Memoria máxima (MB) de un proceso hijo, medida en un intérprete limpio."""
    codigo = ("import resource, subprocess, sys;"
              f"subprocess.run({comando!r}, input={entrada!r}, text=True, capture_output=True, cwd={str(RAIZ)!r});"
              "print(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)")
    salida = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True).stdout
    return int(salida.strip()) / 1024


def main():
    inicio = time.perf_counter()
    servicio = poblar()
    t_carga = time.perf_counter() - inicio

    inicio = time.perf_counter()
    reporte = servicio.reporte_periodo(BASE, BASE + timedelta(days=6))
    t_reporte = time.perf_counter() - inicio

    with tempfile.TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "datos.json"
        inicio = time.perf_counter()
        servicio.repositorio.guardar(ruta)
        t_guardar = time.perf_counter() - inicio
        tamano_kb = ruta.stat().st_size / 1024
        inicio = time.perf_counter()
        servicio.repositorio.cargar(ruta)
        t_cargar = time.perf_counter() - inicio

    tracemalloc.start()
    poblar()
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Volumen simulado: {N_PACIENTES} pacientes, {N_ATENCIONES} atenciones")
    print(f"Cargar el volumen completo:        {t_carga:7.3f} s")
    print(f"Reporte de una semana ({reporte['total']} atenciones): {t_reporte * 1000:7.1f} ms   (criterio: < 5 s)")
    print(f"Guardar en disco ({tamano_kb:,.0f} KB):      {t_guardar * 1000:7.1f} ms")
    print(f"Cargar desde disco:                {t_cargar * 1000:7.1f} ms")
    print(f"Memoria de los datos en RAM:       {pico / 1024 / 1024:7.1f} MB (pico)")
    base = rss_maximo_mb([sys.executable, "-c", "pass"])
    app = rss_maximo_mb([sys.executable, "main.py", "--demo"], "0\n") if (RAIZ / "main.py").read_text().count("--demo") else None
    print(f"Python vacío (referencia):         {base:7.1f} MB")
    if app:
        print(f"SistemaRural-PE (consola, demo):   {app:7.1f} MB")


if __name__ == "__main__":
    main()
