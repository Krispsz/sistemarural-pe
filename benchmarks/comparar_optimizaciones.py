"""Comparación A/B de cada optimización, repetida 7 veces (se toma el mejor tiempo).

Repetir y tomar el mínimo reduce el ruido de otros procesos del equipo.
Uso:  python3 benchmarks/comparar_optimizaciones.py
"""

import json
import sys
import tempfile
import timeit
import tracemalloc
from collections import Counter
from datetime import date, timedelta
from functools import reduce
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.repositorio import RepositorioClinico  # noqa: E402
from src.servicio import ServicioClinico  # noqa: E402

CENTROS = ["Cochabamba", "Uchubamba", "Chugay Centro", "Huaylillas", "Shiracmaca"]


def poblar(n_pacientes, n_atenciones):
    RepositorioClinico.reiniciar()
    servicio = ServicioClinico()
    for i in range(n_pacientes):
        servicio.registrar_paciente(f"{i:08d}", f"Paciente {i}", 20 + i % 60, CENTROS[i % 5])
    for j in range(n_atenciones):
        servicio.registrar_atencion(f"{j % n_pacientes:08d}", "control", date(2026, 9, 1) + timedelta(days=j % 30),
                                    CENTROS[j % 5] if j % 3 == 0 else None)
    return servicio


def mejor(funcion, repeticiones=7):
    return min(timeit.repeat(funcion, number=1, repeat=repeticiones))


def main():
    servicio = poblar(5000, 20000)
    atenciones = servicio.repositorio.atenciones

    # 1) JSON legible (indent=2) frente a JSON compacto
    with tempfile.TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "d.json"
        servicio.repositorio.guardar(ruta)
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    legible = json.dumps(datos, ensure_ascii=False, indent=2)
    compacto = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    t_leg = mejor(lambda: json.dumps(datos, ensure_ascii=False, indent=2))
    t_com = mejor(lambda: json.dumps(datos, ensure_ascii=False, separators=(",", ":")))
    print("1) Formato del archivo de datos (20 000 atenciones)")
    print(f"   indent=2  : {len(legible)/1024:8.0f} KB  {t_leg*1000:7.1f} ms")
    print(f"   compacto  : {len(compacto)/1024:8.0f} KB  {t_com*1000:7.1f} ms   "
          f"({100 - 100*len(compacto)/len(legible):.0f}% menos tamaño)")

    # 2) conteo por centro: reduce con copia de diccionario frente a Counter
    def con_reduce():
        return reduce(lambda c, a: {**c, a.paciente.centro_poblado: c.get(a.paciente.centro_poblado, 0) + 1},
                      atenciones, {})
    def con_counter():
        return dict(Counter(map(lambda a: a.paciente.centro_poblado, atenciones)))
    assert con_reduce() == con_counter()
    t_red, t_cnt = mejor(con_reduce), mejor(con_counter)
    print("2) Conteo por centro poblado (20 000 atenciones)")
    print(f"   reduce + copia de dict: {t_red*1000:7.1f} ms")
    print(f"   Counter + map         : {t_cnt*1000:7.1f} ms   ({t_red/t_cnt:.1f}x más rápido)")

    # 3) tiempo de guardado automático con un volumen REAL de un año (~6 000 atenciones)
    real = poblar(1000, 6000)
    with tempfile.TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "d.json"
        t_real = mejor(lambda: real.repositorio.guardar(ruta))
        kb = ruta.stat().st_size / 1024
    print("3) Guardado automático con el volumen de un año de un puesto (1 000 pacientes, 6 000 atenciones)")
    print(f"   {kb:.0f} KB, {t_real*1000:.1f} ms por registro (el usuario no lo percibe)")

    # 4) memoria de 20 000 atenciones con y sin __slots__ (clases equivalentes mínimas)
    class ConDict:
        def __init__(self): self.a, self.b, self.c, self.d, self.e = 1, 2, 3, 4, 5
    class ConSlots:
        __slots__ = ("a", "b", "c", "d", "e")
        def __init__(self): self.a, self.b, self.c, self.d, self.e = 1, 2, 3, 4, 5
    resultados = {}
    for nombre, clase in (("con __dict__", ConDict), ("con __slots__", ConSlots)):
        tracemalloc.start()
        objetos = [clase() for _ in range(20000)]
        resultados[nombre] = tracemalloc.get_traced_memory()[0] / 1024
        tracemalloc.stop()
        del objetos
    print("4) Memoria de 20 000 objetos de 5 atributos")
    for nombre, kb in resultados.items():
        print(f"   {nombre:14}: {kb:8.0f} KB")


if __name__ == "__main__":
    main()
