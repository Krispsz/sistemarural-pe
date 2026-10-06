from datetime import date, datetime

from src.auditoria import RegistroAuditoria
from src.eventos import ATENCION_REGISTRADA, CITA_AGENDADA, BusEventos
from src.repositorio import RepositorioClinico
from src.servicio import ServicioClinico


def test_singleton_devuelve_siempre_la_misma_instancia():
    assert RepositorioClinico() is RepositorioClinico()


def test_dos_servicios_comparten_los_mismos_datos():
    uno, otro = ServicioClinico(), ServicioClinico()
    uno.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    assert len(otro.repositorio.pacientes) == 1


def test_reiniciar_crea_un_repositorio_nuevo():
    antes = RepositorioClinico()
    RepositorioClinico.reiniciar()
    assert RepositorioClinico() is not antes


def test_el_bus_entrega_el_evento_a_los_manejadores_suscritos():
    bus, recibidos = BusEventos(), []
    bus.suscribir("algo", lambda dato: recibidos.append(dato))
    bus.publicar("algo", dato=42)
    assert recibidos == [42]


def test_un_manejador_defectuoso_no_frena_a_los_demas():
    bus, recibidos = BusEventos(), []
    bus.suscribir("algo", lambda dato: 1 / 0)
    bus.suscribir("algo", lambda dato: recibidos.append(dato))
    bus.publicar("algo", dato=7)
    assert recibidos == [7]
    assert "ZeroDivisionError" in bus.errores[0]


def test_la_auditoria_se_activa_por_eventos_y_no_expone_el_dni(servicio_vacio):
    auditoria = RegistroAuditoria()
    servicio_vacio.bus.suscribir(ATENCION_REGISTRADA, lambda atencion: auditoria.al_registrar_atencion(atencion))
    servicio_vacio.bus.suscribir(CITA_AGENDADA, lambda cita: auditoria.al_agendar_cita(cita))
    servicio_vacio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    servicio_vacio.registrar_atencion("12345678", "control", date(2026, 9, 8))
    servicio_vacio.agendar_cita("12345678", datetime(2026, 10, 7, 9, 0), "control")
    assert len(auditoria.lineas) == 2
    assert all("12345678" not in linea and "12***78" in linea for linea in auditoria.lineas)
