"""Citas médicas y agenda (RF2)."""

from datetime import datetime

from src.excepciones import CitaDuplicadaError, DatosInvalidosError


class Cita:
    def __init__(self, paciente, fecha_hora, motivo):
        if not isinstance(fecha_hora, datetime):
            raise DatosInvalidosError("La fecha y hora de la cita no son válidas.")
        if not isinstance(motivo, str) or not motivo.strip():
            raise DatosInvalidosError("El motivo de la cita no puede estar vacío.")
        self.__paciente = paciente
        self.__fecha_hora = fecha_hora
        self.__motivo = motivo.strip()

    @property
    def paciente(self):
        return self.__paciente

    @property
    def fecha_hora(self):
        return self.__fecha_hora

    @property
    def motivo(self):
        return self.__motivo


class AgendaCitas:
    """Reúne las citas del establecimiento (agregación) y evita horarios repetidos."""

    def __init__(self):
        self.__citas = {}  # fecha_hora -> Cita

    def agendar(self, cita):
        if cita.fecha_hora in self.__citas:
            raise CitaDuplicadaError(
                f"Ya hay una cita agendada el {cita.fecha_hora:%d/%m/%Y a las %H:%M}."
            )
        self.__citas[cita.fecha_hora] = cita

    @property
    def citas(self):
        return tuple(sorted(self.__citas.values(), key=lambda c: c.fecha_hora))

    def citas_del_dia(self, dia):
        return list(filter(lambda c: c.fecha_hora.date() == dia, self.citas))
