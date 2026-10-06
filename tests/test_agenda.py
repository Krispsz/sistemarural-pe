from datetime import date, datetime

import pytest

from src.cita import AgendaCitas, Cita
from src.excepciones import CitaDuplicadaError, DatosInvalidosError
from src.paciente import Paciente


@pytest.fixture
def paciente():
    return Paciente("12345678", "Juana Ramos", 34, "Cochabamba")


def test_agendar_una_cita(paciente):
    agenda = AgendaCitas()
    agenda.agendar(Cita(paciente, datetime(2026, 10, 7, 9, 0), "control"))
    assert len(agenda.citas) == 1


def test_no_permite_dos_citas_en_el_mismo_horario(paciente):
    agenda = AgendaCitas()
    agenda.agendar(Cita(paciente, datetime(2026, 10, 7, 9, 0), "control"))
    with pytest.raises(CitaDuplicadaError):
        agenda.agendar(Cita(paciente, datetime(2026, 10, 7, 9, 0), "otro motivo"))


def test_las_citas_se_listan_ordenadas(paciente):
    agenda = AgendaCitas()
    agenda.agendar(Cita(paciente, datetime(2026, 10, 7, 11, 0), "tarde"))
    agenda.agendar(Cita(paciente, datetime(2026, 10, 7, 8, 0), "temprano"))
    assert [c.motivo for c in agenda.citas] == ["temprano", "tarde"]


def test_citas_del_dia_filtra_por_fecha(paciente):
    agenda = AgendaCitas()
    agenda.agendar(Cita(paciente, datetime(2026, 10, 7, 9, 0), "hoy"))
    agenda.agendar(Cita(paciente, datetime(2026, 10, 8, 9, 0), "mañana"))
    assert [c.motivo for c in agenda.citas_del_dia(date(2026, 10, 7))] == ["hoy"]


def test_una_cita_con_datos_invalidos_lanza_error(paciente):
    with pytest.raises(DatosInvalidosError):
        Cita(paciente, "mañana", "control")
    with pytest.raises(DatosInvalidosError):
        Cita(paciente, datetime(2026, 10, 7, 9, 0), "  ")
