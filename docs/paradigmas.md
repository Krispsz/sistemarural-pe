# Comparación de paradigmas (4, superando el mínimo de 3)

| Paradigma | Ventaja | Desventaja | Caso de uso |
|---|---|---|---|
| Estructurado | Simple para lógica secuencial | No escala con entidades relacionadas | Validaciones puntuales |
| Orientado a objetos | Modela Paciente/Cita/Atención | Excesivo para datos simples | Núcleo del sistema (RF1, RF3) |
| Funcional | Filtra/transforma colecciones | Poco intuitivo para estado persistente | Reportes y filtros (RF4, RF5) |
| Orientado a eventos | Responde a acciones del usuario | Complica el flujo si no está estructurado | Interfaz gráfica (RNF3) |

## Selección justificada

POO como columna vertebral (RF1, RF3), funcional para reportes (RF4, RF5),
orientado a eventos para la interfaz (RNF3). Se descarta el estructurado como
enfoque principal por su baja escalabilidad. Decisión trazada a 5 requisitos.
