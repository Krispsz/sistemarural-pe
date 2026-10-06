from datetime import date

import pytest

from src.excepciones import DatosInvalidosError
from src.reportes import (contar_atenciones, contar_por_centro_poblado,
                          filtrar_atenciones_campana, filtrar_por_periodo,
                          generar_reporte, generar_reporte_periodo)


def test_filter_deja_solo_las_atenciones_de_brigada(servicio):
    brigadas = filtrar_atenciones_campana(servicio.repositorio.atenciones)
    assert len(brigadas) == 2
    assert all(a.campana is not None for a in brigadas)


def test_map_genera_lineas_con_el_dni_enmascarado(servicio):
    lineas = generar_reporte(filtrar_atenciones_campana(servicio.repositorio.atenciones))
    assert lineas[0] == "12***78 | control prenatal | brigada: Cochabamba"
    assert all("12345678" not in linea and "87654321" not in linea for linea in lineas)


def test_reduce_cuenta_las_atenciones(servicio):
    assert contar_atenciones(servicio.repositorio.atenciones) == 3
    assert contar_atenciones([]) == 0


def test_reduce_agrupa_por_centro_poblado(servicio):
    conteo = contar_por_centro_poblado(servicio.repositorio.atenciones)
    assert conteo == {"Cochabamba": 1, "Uchubamba": 1, "Chugay Centro": 1}


def test_filtrar_por_periodo_incluye_los_extremos(servicio):
    atenciones = servicio.repositorio.atenciones
    assert len(filtrar_por_periodo(atenciones, date(2026, 9, 9), date(2026, 9, 9))) == 2


def test_reporte_del_periodo_completo(servicio):
    reporte = servicio.reporte_periodo(date(2026, 9, 8), date(2026, 9, 14))
    assert reporte["total"] == 3
    assert reporte["brigadas"] == 2
    assert len(reporte["lineas"]) == 3
    assert reporte["lineas"][0].startswith("2026-09-08")


def test_el_reporte_no_incluye_atenciones_fuera_del_periodo(servicio):
    assert servicio.reporte_periodo(date(2026, 1, 1), date(2026, 1, 31))["total"] == 0


def test_un_periodo_invertido_lanza_error(servicio):
    with pytest.raises(DatosInvalidosError):
        servicio.reporte_periodo(date(2026, 9, 14), date(2026, 9, 8))


def test_las_funciones_son_puras_y_no_modifican_la_coleccion(servicio):
    original = servicio.repositorio.atenciones
    copia = tuple(original)
    filtrar_atenciones_campana(original)
    generar_reporte_periodo(original, date(2026, 9, 1), date(2026, 9, 30))
    assert original == copia
