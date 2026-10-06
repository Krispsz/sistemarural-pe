"""Historial clínico básico de un paciente (RF3)."""


class HistorialClinico:
    """Lista de atenciones de UN paciente. Nace y muere con él (composición)."""

    __slots__ = ("__atenciones",)

    def __init__(self):
        self.__atenciones = []

    def agregar(self, atencion):
        self.__atenciones.append(atencion)

    @property
    def atenciones(self):
        # Se entrega una tupla: nadie puede modificar el historial desde fuera.
        return tuple(self.__atenciones)

    def __len__(self):
        return len(self.__atenciones)
