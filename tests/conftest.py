import pytest

from src.datos_prueba import cargar_datos_prueba
from src.repositorio import RepositorioClinico
from src.servicio import ServicioClinico


@pytest.fixture(autouse=True)
def repositorio_limpio():
    """Cada prueba parte de un repositorio nuevo (el Singleton se reinicia)."""
    RepositorioClinico.reiniciar()
    yield
    RepositorioClinico.reiniciar()


@pytest.fixture
def servicio_vacio():
    return ServicioClinico()


@pytest.fixture
def servicio():
    """Servicio con los 3 pacientes y 3 atenciones ficticias ya registrados."""
    servicio = ServicioClinico()
    cargar_datos_prueba(servicio)
    return servicio
