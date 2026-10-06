# SistemaRural-PE

Diseño de software multiparadigma para la gestión de establecimientos de salud
en zonas rurales del Perú.

**Curso:** Lenguajes de Programación (UAIN1288P) — Universidad Privada del Norte
**Caso aplicado:** Puesto de Salud Mushit, distrito de Chugay, provincia Sánchez Carrión, La Libertad.

## Equipo
- Erik Yumer Sevillano Loayza — Requisitos y redacción
- Eros Jorge Antonio Valladares Campos — Arquitectura y UML
- Angel Fabrizio Aurora Bazán — Desarrollo backend
- Juan Ventura Aguilar — Eventos e integración
- Sergio Aguirre Argomedo — Control de versiones y calidad

## Paradigmas integrados
- **Orientado a objetos:** herencia (`Persona`), encapsulamiento (atributos privados con `@property`), polimorfismo (`Atencion`).
- **Funcional:** `filter`, `map`, `reduce` y funciones puras en `src/reportes.py`.
- **Orientado a eventos:** bus de eventos con manejadores (`src/eventos.py`, `src/auditoria.py`).

## Patrones de diseño
- **Singleton:** `RepositorioClinico` (una única fuente de verdad).
- **Factory:** `FabricaAtenciones` (crea atenciones en puesto o en brigada).
- **Observer:** `BusEventos` y sus manejadores.

## Protección de datos (Ley N.° 29733)
El DNI no se conserva en texto plano: solo su huella HMAC-SHA256 y una versión enmascarada (`12***78`).
Los datos de prueba son 100% ficticios.

## Estructura
```
src/         Código fuente (dominio, patrones, reportes funcionales, servicio, arranque)
tests/       Pruebas automatizadas (pytest)
benchmarks/  Mediciones de tiempo y memoria (equipos de bajos recursos)
docs/        Documentos de diseño, informes y diagrama UML (docs/uml)
evidencia/   Salidas de ejecución (demo, pytest y benchmarks)
main.py              El sistema: parte vacío y pide los datos a quien lo usa
demo_automatica.py   Demostración con datos ficticios (evidencia)
```

## Ejecutar
```bash
python3 main.py                  # el sistema (guarda solo en datos_local.json)
python3 main.py --demo           # datos ficticios en memoria, sin guardar (para exponer)
python3 demo_automatica.py       # recorrido automático con datos ficticios
python3 -m pytest -v             # pruebas automatizadas (requiere: pip install pytest)
python3 benchmarks/benchmark_recursos.py          # tiempo y memoria con 20 000 atenciones
python3 benchmarks/comparar_optimizaciones.py     # comparación A/B de cada optimización
python3 docs/uml/generar_uml.py  # regenera el UML (requiere Graphviz)
```

## Pensado para equipos de bajos recursos
- Solo biblioteca estándar de Python: sin instalaciones ni internet.
- Interfaz de consola: sin dependencias gráficas.
- `__slots__`, `Counter` y JSON compacto (ver `evidencia/benchmark_comparacion.txt`).
- Guardado automático y atómico tras cada registro: un corte de luz no corrompe ni pierde datos.
