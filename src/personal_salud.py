"""Personal del establecimiento que realiza las atenciones."""

from src.excepciones import DatosInvalidosError
from src.persona import Persona


class PersonalSalud(Persona):
    __slots__ = ("__cargo",)

    def __init__(self, nombre, edad, cargo):
        super().__init__(nombre, edad)
        if not isinstance(cargo, str) or not cargo.strip():
            raise DatosInvalidosError("El cargo no puede estar vacío.")
        self.__cargo = cargo.strip()

    @property
    def cargo(self):
        return self.__cargo

    def descripcion(self):
        return f"{self.cargo} {super().descripcion()}"
