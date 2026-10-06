"""Genera el diagrama de clases UML de SistemaRural-PE con Graphviz (software libre).

Uso:  python3 docs/uml/generar_uml.py     (requiere el programa `dot` de Graphviz)
Salida: diagrama_clases (completo), diagrama_dominio y diagrama_arquitectura (.dot/.png/.svg)
"""

import subprocess
from html import escape
from pathlib import Path

CARPETA = Path(__file__).parent

COLORES = {
    "normal": "#FFFFFF", "singleton": "#DCE9F7", "factory": "#DDF0DD",
    "observer": "#FFF3CC", "modulo": "#EEEEEE", "error": "#FBE3E3",
}

# nombre: (estereotipo, color, atributos, métodos)
CLASES = {
    "Persona": ("", "normal", ["- nombre: str", "- edad: int"], ["+ descripcion(): str"]),
    "Paciente": ("", "normal",
                 ["- huella_dni: str", "- dni_enmascarado: str", "- centro_poblado: str"],
                 ["+ get_dni_enmascarado(): str", "+ coincide_dni(dni): bool", "+ descripcion(): str"]),
    "PersonalSalud": ("", "normal", ["- cargo: str"], ["+ descripcion(): str"]),
    "HistorialClinico": ("", "normal", ["- atenciones: list"], ["+ agregar(atencion)"]),
    "Atencion": ("", "normal",
                 ["- tipo: str", "- fecha: date", "- campana: str"], ["+ descripcion(): str"]),
    "AtencionEnPuesto": ("", "normal", [], ["+ descripcion(): str"]),
    "AtencionBrigada": ("", "normal", [], ["+ descripcion(): str"]),
    "Cita": ("", "normal", ["- fecha_hora: datetime", "- motivo: str"], []),
    "AgendaCitas": ("", "normal", ["- citas: dict"],
                    ["+ agendar(cita)", "+ citas_del_dia(dia): list"]),
    "RepositorioClinico": ("Singleton", "singleton",
                           ["- instancia: RepositorioClinico", "- pacientes: dict", "- atenciones: list"],
                           ["+ buscar_por_dni(dni): Paciente", "+ agregar_paciente(p)",
                            "+ registrar_atencion(a)", "+ guardar(ruta)", "+ cargar(ruta)"]),
    "FabricaAtenciones": ("Factory", "factory", [],
                          ["+ crear(paciente, tipo, fecha, campana): Atencion"]),
    "BusEventos": ("Observer", "observer", ["- manejadores: dict"],
                   ["+ suscribir(evento, manejador)", "+ publicar(evento, datos)"]),
    "RegistroAuditoria": ("", "observer", ["- lineas: list"],
                          ["+ al_registrar_atencion(a)", "+ al_agendar_cita(c)"]),
    "ServicioClinico": ("", "normal", ["- repositorio", "- bus"],
                        ["+ registrar_paciente(...)", "+ registrar_atencion(...)",
                         "+ agendar_cita(...)", "+ reporte_periodo(inicio, fin)"]),
    "reportes": ("modulo funcional", "modulo", [],
                 ["+ filtrar_atenciones_campana()", "+ generar_reporte()", "+ contar_atenciones()",
                  "+ filtrar_por_periodo()", "+ contar_por_centro_poblado()",
                  "+ generar_reporte_periodo()"]),
    "SistemaRuralError": ("", "error", [], []),
    "DatosInvalidosError": ("", "error", [], []),
    "CitaDuplicadaError": ("", "error", [], []),
    "PacienteNoEncontradoError": ("", "error", [], []),
}

# (origen, destino, tipo, etiqueta)  -> el origen es el "todo" / el padre / el cliente
RELACIONES = [
    ("Persona", "Paciente", "herencia", ""),
    ("Persona", "PersonalSalud", "herencia", ""),
    ("Atencion", "AtencionEnPuesto", "herencia", ""),
    ("Atencion", "AtencionBrigada", "herencia", ""),
    ("SistemaRuralError", "DatosInvalidosError", "herencia", ""),
    ("SistemaRuralError", "CitaDuplicadaError", "herencia", ""),
    ("SistemaRuralError", "PacienteNoEncontradoError", "herencia", ""),
    ("Paciente", "HistorialClinico", "composicion", "1"),
    ("RepositorioClinico", "AgendaCitas", "composicion", "1"),
    ("HistorialClinico", "Atencion", "agregacion", "0..*"),
    ("AgendaCitas", "Cita", "agregacion", "0..*"),
    ("RepositorioClinico", "Paciente", "agregacion", "0..*"),
    ("Atencion", "PersonalSalud", "asociacion", "0..1"),
    ("Cita", "Paciente", "asociacion", "1"),
    ("ServicioClinico", "RepositorioClinico", "asociacion", ""),
    ("ServicioClinico", "BusEventos", "asociacion", ""),
    ("ServicioClinico", "FabricaAtenciones", "dependencia", "usa"),
    ("ServicioClinico", "reportes", "dependencia", "usa"),
    ("FabricaAtenciones", "Atencion", "dependencia", "crea"),
    ("RegistroAuditoria", "BusEventos", "dependencia", "se suscribe"),
]

# Aristas que no deben influir en la posición vertical de las clases (solo mejoran el orden visual)
LIBRES = {("Atencion", "PersonalSalud"), ("Cita", "Paciente")}

ESTILO = {
    "herencia":    'dir=back arrowtail=onormal',
    "composicion": 'dir=back arrowtail=diamond',
    "agregacion":  'dir=back arrowtail=odiamond',
    "asociacion":  'arrowhead=vee',
    "dependencia": 'arrowhead=vee style=dashed',
}


def nodo(nombre, estereotipo, color, atributos, metodos, resumida=False):
    if resumida:
        atributos, metodos = [], []
    encabezado = ""
    if estereotipo:
        encabezado = f'<FONT POINT-SIZE="10">&laquo;{escape(estereotipo)}&raquo;</FONT><BR/>'
    filas = [f'<TR><TD BGCOLOR="{COLORES[color]}">{encabezado}<B>{escape(nombre)}</B></TD></TR>']
    if atributos or metodos:
        attrs = "".join(f'{escape(a)}<BR ALIGN="LEFT"/>' for a in atributos) or " "
        filas.append(f'<TR><TD ALIGN="LEFT">{attrs}</TD></TR>')
        mets = "".join(f'{escape(m)}<BR ALIGN="LEFT"/>' for m in metodos) or " "
        filas.append(f'<TR><TD ALIGN="LEFT">{mets}</TD></TR>')
    return (f'  {nombre} [shape=plain label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" '
            f'CELLPADDING="4">{"".join(filas)}</TABLE>>];')


# Vistas para el informe: cada una muestra solo un subconjunto, con letra legible en A4.
VISTAS = {
    "dominio": {
        "clases": ["Persona", "Paciente", "PersonalSalud", "HistorialClinico", "Atencion",
                   "AtencionEnPuesto", "AtencionBrigada", "Cita", "AgendaCitas"],
        "resumidas": [],
    },
    "arquitectura": {
        "clases": ["ServicioClinico", "RepositorioClinico", "FabricaAtenciones", "BusEventos",
                   "RegistroAuditoria", "reportes", "Atencion", "Paciente", "AgendaCitas"],
        "resumidas": ["Atencion", "Paciente", "AgendaCitas"],
        "direccion": "LR",
    },
}


def construir_dot(clases_vista=None, resumidas=(), tamano_letra=11, direccion="TB"):
    visibles = set(clases_vista) if clases_vista else set(CLASES)
    lineas = ["digraph SistemaRuralPE {",
              f'  rankdir={direccion}; nodesep=0.4; ranksep=0.9; splines=true;',
              f'  node [fontname="Helvetica" fontsize={tamano_letra}]; '
              f'edge [fontname="Helvetica" fontsize={tamano_letra - 1} arrowsize=0.9];']
    lineas += [nodo(n, *datos, resumida=(n in resumidas)) for n, datos in CLASES.items() if n in visibles]
    for origen, destino, tipo, etiqueta in RELACIONES:
        if origen not in visibles or destino not in visibles:
            continue
        extra = f' headlabel="{etiqueta}"' if etiqueta and tipo != "dependencia" else ""
        extra = f' label="{etiqueta}"' if etiqueta and tipo == "dependencia" else extra
        libre = " constraint=false" if (origen, destino) in LIBRES else ""
        lineas.append(f"  {origen} -> {destino} [{ESTILO[tipo]}{extra}{libre}];")
    lineas.append("}")
    return "\n".join(lineas)


def generar(nombre, dot, dpi):
    (CARPETA / f"{nombre}.dot").write_text(dot, encoding="utf-8")
    for formato, extra in (("png", [f"-Gdpi={dpi}"]), ("svg", [])):
        subprocess.run(["dot", f"-T{formato}", *extra, str(CARPETA / f"{nombre}.dot"),
                        "-o", str(CARPETA / f"{nombre}.{formato}")], check=True)


if __name__ == "__main__":
    generar("diagrama_clases", construir_dot(), 170)                       # completo (referencia)
    for nombre, vista in VISTAS.items():
        generar(f"diagrama_{nombre}", construir_dot(vista["clases"], vista["resumidas"], 13, vista.get("direccion", "TB")), 200)
    print("Diagramas generados en", CARPETA)
