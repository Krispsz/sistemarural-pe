"""Protección de datos personales (Ley N.° 29733, RNF2).

El DNI nunca se guarda en texto plano: solo se conservan su huella HMAC-SHA256
(para identificar al paciente) y una versión enmascarada (para mostrarla).
"""

import hashlib
import hmac
import os

from src.excepciones import DatosInvalidosError

_CLAVE_DESARROLLO = "clave-solo-para-desarrollo"
LARGO_DNI = 8


def _clave_secreta():
    # En producción la clave se define en la variable de entorno SISTEMARURAL_CLAVE.
    return os.environ.get("SISTEMARURAL_CLAVE", _CLAVE_DESARROLLO).encode("utf-8")


def validar_dni(dni):
    """Acepta solo DNI de 8 dígitos; de lo contrario lanza DatosInvalidosError."""
    if not isinstance(dni, str) or len(dni) != LARGO_DNI or not dni.isdigit():
        raise DatosInvalidosError("El DNI debe tener exactamente 8 dígitos numéricos.")


def huella_dni(dni):
    """Huella irreversible del DNI (HMAC-SHA256 con clave secreta)."""
    validar_dni(dni)
    return hmac.new(_clave_secreta(), dni.encode("utf-8"), hashlib.sha256).hexdigest()


def enmascarar_dni(dni):
    """Muestra solo los 2 primeros y los 2 últimos dígitos: 12***78."""
    validar_dni(dni)
    return dni[:2] + "***" + dni[-2:]
