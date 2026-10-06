"""Paciente del establecimiento (RF1, RNF2)."""

import hmac

from src.excepciones import DatosInvalidosError
from src.historial import HistorialClinico
from src.persona import Persona
from src.seguridad import enmascarar_dni, huella_dni


class Paciente(Persona):
    """Persona atendida. Su DNI jamás se conserva en texto plano."""

    __slots__ = ("__huella_dni", "__dni_enmascarado", "__centro_poblado", "__historial")

    def __init__(self, dni, nombre, edad, centro_poblado):
        super().__init__(nombre, edad)
        self.__huella_dni = huella_dni(dni)          # valida el DNI
        self.__dni_enmascarado = enmascarar_dni(dni)
        self.centro_poblado = centro_poblado
        self.__historial = HistorialClinico()        # composición

    @classmethod
    def restaurar(cls, huella, dni_enmascarado, nombre, edad, centro_poblado):
        """Reconstruye un paciente guardado, sin necesidad del DNI original."""
        paciente = cls.__new__(cls)
        Persona.__init__(paciente, nombre, edad)
        paciente.__huella_dni = huella
        paciente.__dni_enmascarado = dni_enmascarado
        paciente.centro_poblado = centro_poblado
        paciente.__historial = HistorialClinico()
        return paciente

    @property
    def centro_poblado(self):
        return self.__centro_poblado

    @centro_poblado.setter
    def centro_poblado(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError("El centro poblado no puede estar vacío.")
        self.__centro_poblado = valor.strip()

    @property
    def huella_dni(self):
        return self.__huella_dni

    @property
    def historial(self):
        return self.__historial

    def get_dni_enmascarado(self):
        return self.__dni_enmascarado

    def coincide_dni(self, dni):
        """Comprueba un DNI sin exponer el almacenado (comparación en tiempo constante)."""
        try:
            return hmac.compare_digest(self.__huella_dni, huella_dni(dni))
        except DatosInvalidosError:
            return False

    def descripcion(self):
        return f"Paciente {super().descripcion()}, DNI {self.__dni_enmascarado}, {self.centro_poblado}"

    def __repr__(self):
        # Seguridad: ningún log o depuración debe exponer el DNI en texto plano.
        return f"Paciente(dni={self.__dni_enmascarado}, nombre={self.nombre})"
