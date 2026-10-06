# Restricciones de diseño (con justificación técnica)

1. Uso de herramientas de código abierto: Python 3.x, VS Code / Apache NetBeans.
   Justificación técnica: Python ofrece soporte nativo para los tres paradigmas
   requeridos (POO, funcional y orientado a eventos) sin licencias de pago.

2. Cumplimiento de la Ley N.° 29733, Ley de Protección de Datos Personales.
   Justificación técnica: el DNI se almacena como atributo privado y solo se
   expone enmascarado, evitando fuga de datos en reportes o logs.

3. El sistema debe funcionar en equipos de gama baja y sin conexión estable a internet.
   Justificación técnica: el distrito de Chugay tiene conectividad limitada
   (12.5% de municipalidades con computadoras funcionales en 2019).

4. Los datos usados en desarrollo y demostraciones deben ser ficticios.
   Justificación técnica: minimiza el riesgo legal y ético antes de contar con
   los controles de seguridad de la versión final.

5. El formato de reporte debe ser compatible con lo que el puesto remite a la
   Red de Salud Sánchez Carrión.
   Justificación técnica: garantiza interoperabilidad sin exigir cambios en el
   proceso administrativo existente.

Total: 5 restricciones de diseño, superando el mínimo de 4.

# Criterios de éxito medibles y verificables

- Registrar un paciente en menos de 1 minuto.
- Cero citas duplicadas en el mismo horario.
- Generar el reporte semanal en menos de 5 segundos.
- 100% de los datos personales almacenados sin texto plano.

Total: 4 criterios, superando el mínimo de 3.
