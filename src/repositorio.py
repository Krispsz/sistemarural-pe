"""Patrón Singleton: una única fuente de verdad para los datos del puesto."""

import json
import os
from datetime import date, datetime
from pathlib import Path

from src.atencion import Atencion
from src.cita import AgendaCitas, Cita
from src.excepciones import DatosInvalidosError, PacienteNoEncontradoError
from src.fabrica import FabricaAtenciones
from src.paciente import Paciente
from src.seguridad import huella_dni


class RepositorioClinico:
    """Guarda pacientes, atenciones y agenda en memoria (y en un archivo JSON local).

    Es Singleton porque el problema original era el cuaderno duplicado: si
    existieran dos repositorios, habría dos "verdades" y registros repetidos.
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            instancia = super().__new__(cls)
            instancia._inicializar()
            cls._instancia = instancia
        return cls._instancia

    def _inicializar(self):
        self.__pacientes = {}      # huella del DNI -> Paciente
        self.__atenciones = []
        self.__agenda = AgendaCitas()

    @classmethod
    def reiniciar(cls):
        """Descarta la instancia actual (se usa en las pruebas automatizadas)."""
        cls._instancia = None

    # ---- consulta -------------------------------------------------------
    @property
    def pacientes(self):
        return tuple(self.__pacientes.values())

    @property
    def atenciones(self):
        return tuple(self.__atenciones)

    @property
    def agenda(self):
        return self.__agenda

    def buscar_por_dni(self, dni):
        paciente = self.__pacientes.get(huella_dni(dni))
        if paciente is None:
            raise PacienteNoEncontradoError("No hay un paciente registrado con ese DNI.")
        return paciente

    # ---- modificación ---------------------------------------------------
    def agregar_paciente(self, paciente):
        if paciente.huella_dni in self.__pacientes:
            raise DatosInvalidosError("Ya existe un paciente registrado con ese DNI.")
        self.__pacientes[paciente.huella_dni] = paciente

    def registrar_atencion(self, atencion):
        self.__atenciones.append(atencion)

    # ---- persistencia local (RNF1: funciona sin internet) ----------------
    def guardar(self, ruta):
        datos = {
            "pacientes": [
                {
                    "huella_dni": p.huella_dni,
                    "dni_enmascarado": p.get_dni_enmascarado(),
                    "nombre": p.nombre,
                    "edad": p.edad,
                    "centro_poblado": p.centro_poblado,
                }
                for p in self.__pacientes.values()
            ],
            "atenciones": [
                {
                    "huella_dni": a.paciente.huella_dni,
                    "tipo": a.tipo,
                    "fecha": a.fecha.isoformat(),
                    "campana": a.campana,
                }
                for a in self.__atenciones
            ],
            "citas": [
                {
                    "huella_dni": c.paciente.huella_dni,
                    "fecha_hora": c.fecha_hora.isoformat(),
                    "motivo": c.motivo,
                }
                for c in self.__agenda.citas
            ],
        }
        # Escritura atómica: primero a un temporal y luego se reemplaza. Si la luz se
        # corta a mitad de guardado, el archivo anterior queda intacto (nunca a medias).
        # JSON compacto: archivo más pequeño y rápido de escribir en discos lentos.
        ruta = Path(ruta)
        temporal = ruta.with_name(ruta.name + ".tmp")
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, separators=(",", ":"))
        os.replace(temporal, ruta)

    def cargar(self, ruta):
        try:
            with open(ruta, encoding="utf-8") as archivo:
                datos = json.load(archivo)
            self._inicializar()
            for d in datos["pacientes"]:
                self.agregar_paciente(Paciente.restaurar(
                    d["huella_dni"], d["dni_enmascarado"], d["nombre"], d["edad"], d["centro_poblado"]))
            for d in datos["atenciones"]:
                paciente = self.__pacientes[d["huella_dni"]]
                atencion = FabricaAtenciones.crear(
                    paciente, d["tipo"], date.fromisoformat(d["fecha"]), d["campana"])
                paciente.historial.agregar(atencion)
                self.registrar_atencion(atencion)
            for d in datos["citas"]:
                paciente = self.__pacientes[d["huella_dni"]]
                self.__agenda.agendar(Cita(paciente, datetime.fromisoformat(d["fecha_hora"]), d["motivo"]))
        except (OSError, ValueError, KeyError) as error:
            raise DatosInvalidosError(f"No se pudo cargar el archivo de datos: {error}") from error
