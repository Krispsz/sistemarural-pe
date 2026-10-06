# Comparación de paradigmas

| Paradigma | Ventaja | Desventaja | Caso de uso en el sistema |
|---|---|---|---|
| Estructurado | Simple para lógica secuencial | No escala con entidades relacionadas | Validaciones puntuales (formato de DNI) |
| Orientado a objetos | Modela naturalmente Paciente/Cita/Atención con herencia y encapsulamiento | Puede ser excesivo para transformar datos simples | Núcleo del sistema (RF1, RF3) |
| Funcional | Ideal para filtrar/transformar colecciones sin efectos secundarios | Poco intuitivo para modelar estado persistente | Reportes y filtros por campaña (RF4, RF5) |
| Orientado a eventos | Responde de forma natural a acciones del usuario en la GUI | Complica el flujo si no está bien estructurado | Formularios e interacción (RNF3) |

## Selección justificada

La programación orientada a objetos se emplea como columna vertebral del
sistema para modelar las entidades del dominio (RF1, RF3); la programación
funcional se aplica en la generación de reportes y en el filtrado de
atenciones por campaña (RF4, RF5); y la programación orientada a eventos se
reserva para la interfaz gráfica que atiende el requisito de usabilidad
(RNF3). Se descarta el paradigma estructurado como enfoque principal por su
baja escalabilidad frente a un dominio con múltiples entidades relacionadas.
