"""Prueba de viabilidad: integracion POO + Funcional (avance EP, semana 4)."""

from src.datos_prueba import atenciones
from src.reportes import contar_atenciones, filtrar_atenciones_campana, generar_reporte

atenciones_campana = filtrar_atenciones_campana(atenciones)
reporte = generar_reporte(atenciones_campana)
total_campana = contar_atenciones(atenciones_campana)

print("=== PRUEBA DE VIABILIDAD: integracion POO + Funcional ===")
print(f"Total de atenciones registradas: {len(atenciones)}")
print(f"Atenciones ligadas a brigadas itinerantes (filter): {total_campana}")
print("Reporte generado con map() sobre la coleccion de Atencion:")
for linea in reporte:
    print(" -", linea)
print()
print("Verificacion de dato protegido (RNF - Ley 29733):")
print(" DNI real (interno, nunca expuesto): [privado]")
print(f" DNI mostrado en reporte: {atenciones[0].paciente.get_dni_enmascarado()}")
