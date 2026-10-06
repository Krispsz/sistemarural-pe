"""Casos de uso del sistema: coordina repositorio, fábrica y eventos."""

from src.cita import Cita
from src.eventos import ATENCION_REGISTRADA, CITA_AGENDADA, PACIENTE_REGISTRADO, BusEventos
from src.fabrica import FabricaAtenciones
from src.paciente import Paciente
from src.repositorio import RepositorioClinico
from src.reportes import generar_reporte_periodo


class ServicioClinico:
    """Orquesta los casos de uso. No guarda datos (eso es del repositorio) ni
    calcula reportes (eso es de `reportes`): cada clase tiene una sola razón de cambio."""

    def __init__(self, repositorio=None, bus=None):
        self.__repositorio = repositorio or RepositorioClinico()
        self.__bus = bus or BusEventos()

    @property
    def repositorio(self):
        return self.__repositorio

    @property
    def bus(self):
        return self.__bus

    def registrar_paciente(self, dni, nombre, edad, centro_poblado):
        paciente = Paciente(dni, nombre, edad, centro_poblado)
        self.__repositorio.agregar_paciente(paciente)
        self.__bus.publicar(PACIENTE_REGISTRADO, paciente=paciente)
        return paciente

    def registrar_atencion(self, dni, tipo, fecha, campana=None, personal=None):
        paciente = self.__repositorio.buscar_por_dni(dni)
        atencion = FabricaAtenciones.crear(paciente, tipo, fecha, campana, personal)
        paciente.historial.agregar(atencion)
        self.__repositorio.registrar_atencion(atencion)
        self.__bus.publicar(ATENCION_REGISTRADA, atencion=atencion)
        return atencion

    def agendar_cita(self, dni, fecha_hora, motivo):
        paciente = self.__repositorio.buscar_por_dni(dni)
        cita = Cita(paciente, fecha_hora, motivo)
        self.__repositorio.agenda.agendar(cita)
        self.__bus.publicar(CITA_AGENDADA, cita=cita)
        return cita

    def reporte_periodo(self, inicio, fin):
        return generar_reporte_periodo(self.__repositorio.atenciones, inicio, fin)
