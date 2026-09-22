# Restricciones de diseño

- Uso de herramientas de código abierto: Python 3.x o Java OpenJDK, VS Code.
- Cumplimiento de la Ley N.° 29733, Ley de Protección de Datos Personales
  (consentimiento, finalidad, no texto plano).
- El sistema debe funcionar en equipos de gama baja y sin conexión estable a internet.
- Los datos usados en desarrollo y demostraciones deben ser ficticios; nunca
  información real de pacientes.
- El formato de reporte debe ser compatible con lo que el puesto remite a la
  Red de Salud Sánchez Carrión.

# Criterios de éxito medibles

- Registrar un paciente en menos de 1 minuto (frente a varios minutos en el
  cuaderno físico actual).
- Cero citas duplicadas en el mismo horario.
- Generar el reporte semanal en menos de 5 segundos y sin errores de conteo manual.
- 100% de los datos personales almacenados sin texto plano, verificable
  directamente en el código fuente.
