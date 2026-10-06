from datetime import date

from src.arranque import crear_servicio
from src.repositorio import RepositorioClinico


def test_el_sistema_parte_vacio_sin_archivo(tmp_path):
    servicio, _ = crear_servicio(tmp_path / "datos.json")
    assert servicio.repositorio.pacientes == ()


def test_guarda_solo_despues_de_cada_registro(tmp_path):
    ruta = tmp_path / "datos.json"
    servicio, _ = crear_servicio(ruta)
    assert not ruta.exists()
    servicio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    contenido = ruta.read_text(encoding="utf-8")
    assert "Juana Ramos" in contenido and "12345678" not in contenido


def test_recupera_lo_guardado_al_volver_a_iniciar(tmp_path):
    ruta = tmp_path / "datos.json"
    servicio, _ = crear_servicio(ruta)
    servicio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    servicio.registrar_atencion("12345678", "control", date(2026, 9, 8), "Cochabamba")

    RepositorioClinico.reiniciar()  # equivale a apagar y volver a abrir el programa
    otro, _ = crear_servicio(ruta)
    assert otro.repositorio.buscar_por_dni("12345678").nombre == "Juana Ramos"
    assert len(otro.repositorio.atenciones) == 1


def test_el_guardado_atomico_no_deja_archivos_temporales(tmp_path):
    ruta = tmp_path / "datos.json"
    servicio, _ = crear_servicio(ruta)
    servicio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    assert [p.name for p in tmp_path.iterdir()] == ["datos.json"]


def test_un_fallo_al_guardar_no_impide_registrar(tmp_path):
    servicio, _ = crear_servicio(tmp_path / "carpeta_inexistente" / "datos.json")
    servicio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    assert len(servicio.repositorio.pacientes) == 1       # el registro se hizo
    assert "No such file" in servicio.bus.errores[0] or "FileNotFoundError" in servicio.bus.errores[0]


def test_sin_ruta_trabaja_solo_en_memoria(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    servicio, _ = crear_servicio()
    servicio.registrar_paciente("12345678", "Juana Ramos", 34, "Cochabamba")
    assert list(tmp_path.iterdir()) == []
