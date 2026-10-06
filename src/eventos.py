"""Programación orientada a eventos: un bus de eventos con manejadores (Observer)."""

from collections import defaultdict

ATENCION_REGISTRADA = "atencion_registrada"
CITA_AGENDADA = "cita_agendada"
PACIENTE_REGISTRADO = "paciente_registrado"


class BusEventos:
    """Quien publica un evento no conoce a sus manejadores (bajo acoplamiento)."""

    def __init__(self):
        self.__manejadores = defaultdict(list)
        self.__errores = []

    def suscribir(self, evento, manejador):
        self.__manejadores[evento].append(manejador)

    def publicar(self, evento, **datos):
        for manejador in list(self.__manejadores[evento]):
            try:
                manejador(**datos)
            except Exception as error:  # un manejador defectuoso no debe frenar el registro
                self.__errores.append(f"{evento}: {type(error).__name__}: {error}")

    @property
    def errores(self):
        return tuple(self.__errores)
