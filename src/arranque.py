"""Arranque del sistema: arma el servicio, la auditoría y el guardado automático."""

from pathlib import Path

from src.auditoria import RegistroAuditoria
from src.eventos import ATENCION_REGISTRADA, CITA_AGENDADA, PACIENTE_REGISTRADO
from src.servicio import ServicioClinico

RUTA_DATOS_POR_DEFECTO = "datos_local.json"


def crear_servicio(ruta_datos=None):
    """Devuelve (servicio, auditoria) listos para usar.

    Con `ruta_datos`, el sistema recupera lo guardado y guarda SOLO tras cada
    cambio: si el equipo se apaga por un corte de luz, no se pierde lo registrado.
    Sin `ruta_datos` trabaja únicamente en memoria (pruebas y demostraciones).
    El sistema siempre parte vacío: los datos los ingresa quien lo usa.
    """
    servicio = ServicioClinico()
    auditoria = RegistroAuditoria()
    bus = servicio.bus
    bus.suscribir(ATENCION_REGISTRADA, lambda atencion: auditoria.al_registrar_atencion(atencion))
    bus.suscribir(CITA_AGENDADA, lambda cita: auditoria.al_agendar_cita(cita))

    if ruta_datos:
        if Path(ruta_datos).exists():
            servicio.repositorio.cargar(ruta_datos)

        def guardar_automaticamente(**_datos_del_evento):
            servicio.repositorio.guardar(ruta_datos)

        for evento in (PACIENTE_REGISTRADO, ATENCION_REGISTRADA, CITA_AGENDADA):
            bus.suscribir(evento, guardar_automaticamente)
    return servicio, auditoria
