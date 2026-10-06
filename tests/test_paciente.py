import pytest

from src.excepciones import DatosInvalidosError
from src.paciente import Paciente
from src.persona import Persona
from src.personal_salud import PersonalSalud


def crear():
    return Paciente("12345678", "Juana Ramos", 34, "Cochabamba")


def test_el_dni_se_muestra_enmascarado():
    assert crear().get_dni_enmascarado() == "12***78"


def atributos_internos(objeto):
    """Valores de todos los atributos privados (declarados en __slots__) del objeto."""
    valores = []
    for clase in type(objeto).__mro__:
        for nombre in getattr(clase, "__slots__", ()):
            real = f"_{clase.__name__.lstrip('_')}{nombre}" if nombre.startswith("__") else nombre
            valores.append(getattr(objeto, real, None))
    return str(valores)


def test_el_dni_nunca_queda_en_texto_plano():
    paciente = crear()
    for texto in (repr(paciente), paciente.descripcion(), atributos_internos(paciente)):
        assert "12345678" not in texto
    assert "12***78" in atributos_internos(paciente)  # la comprobación sí ve los atributos reales


@pytest.mark.parametrize("dni_malo", ["123", "abcdefgh", "123456789", "", None, 12345678])
def test_un_dni_invalido_lanza_error(dni_malo):
    with pytest.raises(DatosInvalidosError):
        Paciente(dni_malo, "Juana Ramos", 34, "Cochabamba")


def test_coincide_dni_compara_sin_exponer_el_dni():
    paciente = crear()
    assert paciente.coincide_dni("12345678")
    assert not paciente.coincide_dni("87654321")
    assert not paciente.coincide_dni("no-es-dni")


@pytest.mark.parametrize("edad_mala", [-1, 121, "34", 3.5, True])
def test_el_setter_de_edad_valida(edad_mala):
    with pytest.raises(DatosInvalidosError):
        crear().edad = edad_mala


def test_el_nombre_no_puede_estar_vacio():
    with pytest.raises(DatosInvalidosError):
        Paciente("12345678", "   ", 34, "Cochabamba")


def test_el_historial_se_entrega_inmutable():
    assert isinstance(crear().historial.atenciones, tuple)


def test_herencia_y_polimorfismo_de_descripcion():
    paciente = crear()
    medico = PersonalSalud("Marisol Quispe", 45, "Licenciada en enfermería")
    assert isinstance(paciente, Persona) and isinstance(medico, Persona)
    assert "DNI 12***78" in paciente.descripcion()
    assert "Licenciada en enfermería" in medico.descripcion()
    assert paciente.descripcion() != medico.descripcion()
