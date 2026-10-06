# Cronograma (8 hitos, superando el mínimo de 6)

| Semana | Hito | Responsable |
|---|---|---|
| S1–S2 | Institución, requisitos y criterios de éxito | Erik Yumer Sevillano Loayza |
| S3 | Cronograma, roles y comparación de paradigmas | Todo el equipo |
| S4 | Prototipo de viabilidad ejecutado, con veredicto | Angel Fabrizio Aurora Bazán |
| S5 | Diagnóstico de riesgos y primer ciclo de retroalimentación | Sergio Aguirre Argomedo |
| S6 | Entrega EP (este avance) | Todo el equipo |
| S6–S7 | Diagrama UML y patrones de diseño | Eros Jorge Antonio Valladares Campos |
| S7 | Implementación completa y pruebas | Fabrizio y Juan |
| S8 | Informe final y sustentación | Todo el equipo |

# Roles diferenciados con responsabilidades explícitas

- Integrante 1 (Erik): Levantamiento de requisitos y redacción del informe.
- Integrante 2 (Eros): Arquitectura del sistema y modelado UML.
- Integrante 3 (Fabrizio): Desarrollo backend (POO + funcional).
- Integrante 4 (Juan): Desarrollo de la interfaz orientada a eventos.
- Integrante 5 (Sergio): Control de versiones, pruebas y calidad de código.

# Ruta crítica identificada (camino crítico)

S1–S2 -> S3 -> S4 -> S6-S7 -> S7 -> S8

Dependencias explícitas (2, superando el mínimo de 1):
1. El UML (S6-S7) depende de que los requisitos y paradigmas (S1-S3) estén cerrados.
2. La implementación completa (S7) depende del UML aprobado y del veredicto del prototipo (S4).

# Contingencia para el riesgo principal (R1)

Si la interfaz orientada a eventos resulta muy costosa en tiempo, se reemplaza
por un menú de consola simple, documentando el cambio como riesgo mitigado.

# Actualización v1.1 (Ciclo de retroalimentación 1)

Tras el veredicto positivo del prototipo de viabilidad (ver evidencia/salida_prueba_viabilidad.txt),
se decide posponer el desarrollo de la interfaz orientada a eventos (GUI) hasta
asegurar completamente el núcleo POO-Funcional y la persistencia local.
