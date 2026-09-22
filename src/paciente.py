class Paciente:
    """Representa a un paciente del Puesto de Salud Mushit (RF1, RNF2)."""

    def __init__(self, dni, nombre, edad, centro_poblado):
        self.__dni = dni  # encapsulamiento: atributo privado
        self.nombre = nombre
        self.edad = edad
        self.centro_poblado = centro_poblado

    def get_dni_enmascarado(self):
        # Tratamiento de datos personales (Ley N.29733): nunca texto plano
        return self.__dni[:2] + "***" + self.__dni[-2:]
