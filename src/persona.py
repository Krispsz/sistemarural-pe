"""Clase base del dominio: Persona (herencia y encapsulamiento)."""

from src.excepciones import DatosInvalidosError

EDAD_MAXIMA = 120


class Persona:
    """Datos comunes de cualquier persona del sistema, siempre validados."""

    __slots__ = ("__nombre", "__edad")  # sin __dict__ por objeto: ahorra memoria

    def __init__(self, nombre, edad):
        self.nombre = nombre  # pasa por el setter, que valida
        self.edad = edad

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or not 0 <= valor <= EDAD_MAXIMA:
            raise DatosInvalidosError(f"La edad debe ser un entero entre 0 y {EDAD_MAXIMA}.")
        self.__edad = valor

    def descripcion(self):
        """Texto de presentación; las subclases lo especializan (polimorfismo)."""
        return f"{self.nombre} ({self.edad} años)"
