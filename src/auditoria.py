"""Manejador de eventos: bitácora de actividad SIN datos personales en claro."""


class RegistroAuditoria:
    def __init__(self):
        self.__lineas = []

    def al_registrar_atencion(self, atencion):
        paciente = atencion.paciente
        self.__lineas.append(
            f"ATENCION | {atencion.fecha.isoformat()} | "
            f"{paciente.get_dni_enmascarado()} | {atencion.tipo}"
        )

    def al_agendar_cita(self, cita):
        self.__lineas.append(
            f"CITA | {cita.fecha_hora:%Y-%m-%d %H:%M} | "
            f"{cita.paciente.get_dni_enmascarado()} | {cita.motivo}"
        )

    @property
    def lineas(self):
        return tuple(self.__lineas)
