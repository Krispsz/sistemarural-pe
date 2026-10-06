from datetime import date, datetime

import pytest

from src.excepciones import (CitaDuplicadaError, DatosInvalidosError,
                             PacienteNoEncontradoError, SistemaRuralError)
from src.repositorio import RepositorioClinico
from src.servicio import ServicioClinico


def test_registrar_una_atencion_actualiza_historial_y_repositorio(servicio_vacio):
    paciente = servicio_vacio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    servicio_vacio.registrar_atencion("12345678", "control", date(2026, 9, 8), "Cochabamba")
    assert len(paciente.historial) == 1
    assert len(servicio_vacio.repositorio.atenciones) == 1


def test_atender_a_un_paciente_inexistente_lanza_error(servicio_vacio):
    with pytest.raises(PacienteNoEncontradoError):
        servicio_vacio.registrar_atencion("12345678", "control", date(2026, 9, 8))


def test_no_se_puede_registrar_dos_veces_el_mismo_dni(servicio_vacio):
    servicio_vacio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    with pytest.raises(DatosInvalidosError):
        servicio_vacio.registrar_paciente("12345678", "Otra Persona", 20, "Chugay")


def test_agendar_dos_citas_a_la_misma_hora_lanza_error(servicio):
    servicio.agendar_cita("12345678", datetime(2026, 10, 7, 9, 0), "control")
    with pytest.raises(CitaDuplicadaError):
        servicio.agendar_cita("87654321", datetime(2026, 10, 7, 9, 0), "consulta")


def test_todos_los_errores_controlados_comparten_una_base():
    for error in (DatosInvalidosError, CitaDuplicadaError, PacienteNoEncontradoError):
        assert issubclass(error, SistemaRuralError)


def test_guardar_y_cargar_conserva_los_datos(servicio, tmp_path):
    servicio.agendar_cita("12345678", datetime(2026, 10, 7, 9, 0), "control")
    ruta = tmp_path / "datos.json"
    servicio.repositorio.guardar(ruta)

    RepositorioClinico.reiniciar()
    nuevo = ServicioClinico()
    nuevo.repositorio.cargar(ruta)

    assert len(nuevo.repositorio.pacientes) == 3
    assert len(nuevo.repositorio.atenciones) == 3
    assert len(nuevo.repositorio.agenda.citas) == 1
    assert nuevo.repositorio.buscar_por_dni("12345678").nombre == "Juana Ramos"


def test_el_archivo_guardado_no_contiene_ningun_dni_en_texto_plano(servicio, tmp_path):
    ruta = tmp_path / "datos.json"
    servicio.repositorio.guardar(ruta)
    contenido = ruta.read_text(encoding="utf-8")
    for dni in ("12345678", "87654321", "11223344"):
        assert dni not in contenido


def test_cargar_un_archivo_inexistente_o_corrupto_lanza_error(servicio_vacio, tmp_path):
    with pytest.raises(DatosInvalidosError):
        servicio_vacio.repositorio.cargar(tmp_path / "no_existe.json")
    corrupto = tmp_path / "corrupto.json"
    corrupto.write_text("{esto no es json", encoding="utf-8")
    with pytest.raises(DatosInvalidosError):
        servicio_vacio.repositorio.cargar(corrupto)
