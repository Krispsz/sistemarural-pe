class Atencion:
    """Representa una atención médica, fija o de brigada itinerante (RF3, RF5)."""

    def __init__(self, paciente, tipo, fecha, campana=None):
        self.paciente = paciente
        self.tipo = tipo
        self.fecha = fecha
        self.campana = campana  # None = atención fija; str = nombre de la brigada
