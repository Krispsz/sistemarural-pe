"""Atenciones médicas: en el puesto fijo o en brigada itinerante (RF3, RF5)."""

from datetime import date

from src.excepciones import DatosInvalidosError


class Atencion:
    """Atención brindada a un paciente. Las subclases la especializan (polimorfismo)."""

    __slots__ = ("__paciente", "__tipo", "__fecha", "__campana", "__personal")

    def __init__(self, paciente, tipo, fecha, campana=None, personal=None):
        if not isinstance(tipo, str) or not tipo.strip():
            raise DatosInvalidosError("El tipo de atención no puede estar vacío.")
        if not isinstance(fecha, date):
            raise DatosInvalidosError("La fecha de atención no es válida.")
        self.__paciente = paciente
        self.__tipo = tipo.strip()
        self.__fecha = fecha
        self.__campana = campana
        self.__personal = personal

    @property
    def paciente(self):
        return self.__paciente

    @property
    def tipo(self):
        return self.__tipo

    @property
    def fecha(self):
        return self.__fecha

    @property
    def campana(self):
        """None si fue en el puesto fijo; nombre de la brigada si fue itinerante."""
        return self.__campana

    @property
    def personal(self):
        return self.__personal

    def descripcion(self):
        return f"{self.tipo} ({self.fecha.isoformat()})"


class AtencionEnPuesto(Atencion):
    """Atención realizada en el establecimiento."""

    __slots__ = ()

    def __init__(self, paciente, tipo, fecha, personal=None):
        super().__init__(paciente, tipo, fecha, campana=None, personal=personal)

    def descripcion(self):
        return f"{super().descripcion()} en el puesto"


class AtencionBrigada(Atencion):
    """Atención realizada fuera del puesto, en una brigada itinerante (RF5)."""

    __slots__ = ()

    def __init__(self, paciente, tipo, fecha, campana, personal=None):
        if not isinstance(campana, str) or not campana.strip():
            raise DatosInvalidosError("Una atención de brigada necesita el nombre de la brigada.")
        super().__init__(paciente, tipo, fecha, campana=campana.strip(), personal=personal)

    def descripcion(self):
        return f"{super().descripcion()} en brigada {self.campana}"
