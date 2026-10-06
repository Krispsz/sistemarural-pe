from datetime import date

import pytest

from src.atencion import Atencion, AtencionBrigada, AtencionEnPuesto
from src.excepciones import DatosInvalidosError
from src.fabrica import FabricaAtenciones
from src.paciente import Paciente


@pytest.fixture
def paciente():
    return Paciente("12345678", "Juana Ramos", 34, "Cochabamba")


def test_la_fabrica_crea_brigada_si_hay_campana(paciente):
    atencion = FabricaAtenciones.crear(paciente, "control", date(2026, 9, 8), "Cochabamba")
    assert isinstance(atencion, AtencionBrigada)
    assert atencion.campana == "Cochabamba"


@pytest.mark.parametrize("sin_campana", [None, "", "   "])
def test_la_fabrica_crea_atencion_en_puesto_sin_campana(paciente, sin_campana):
    atencion = FabricaAtenciones.crear(paciente, "vacunacion", date(2026, 9, 9), sin_campana)
    assert isinstance(atencion, AtencionEnPuesto)
    assert atencion.campana is None


def test_las_subclases_son_sustituibles_por_la_base(paciente):
    """Principio de Liskov: cualquier Atencion se usa igual, sea del tipo que sea."""
    atenciones = [
        FabricaAtenciones.crear(paciente, "control", date(2026, 9, 8), "Cochabamba"),
        FabricaAtenciones.crear(paciente, "vacunacion", date(2026, 9, 9)),
    ]
    assert all(isinstance(a, Atencion) for a in atenciones)
    assert all(a.descripcion() for a in atenciones)


def test_la_descripcion_es_polimorfica(paciente):
    brigada = AtencionBrigada(paciente, "control", date(2026, 9, 8), "Cochabamba")
    puesto = AtencionEnPuesto(paciente, "control", date(2026, 9, 8))
    assert "brigada Cochabamba" in brigada.descripcion()
    assert "en el puesto" in puesto.descripcion()


def test_una_brigada_sin_nombre_lanza_error(paciente):
    with pytest.raises(DatosInvalidosError):
        AtencionBrigada(paciente, "control", date(2026, 9, 8), "  ")


def test_una_atencion_con_fecha_invalida_lanza_error(paciente):
    with pytest.raises(DatosInvalidosError):
        AtencionEnPuesto(paciente, "control", "2026-09-08")
