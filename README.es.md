# Skill Pitch-Deck: Discurso Ganador, Diapositivas PPTX y Videos Integrados

Skill todo-en-uno para agentes de IA que integra la redacción del **pitch de alto impacto**, la generación de **diapositivas visualmente ricas en PowerPoint (`.pptx`)**, herramientas de **recorte y sincronización de video** y un **simulador de ensayo web en HTML**.

## Nuevas Capacidades
1. **Herramientas de Video (`scripts/video_tools.py`)**: Recorte, ajuste de velocidad al tiempo del pitch con FFmpeg, generación de demos sintéticas e integración con `heygen-com/hyperframes`.
2. **Video con Flujo al Costado**: Diapositivas con video al lado izquierdo y un diagrama de flujo en 3 pasos al lado derecho que explica la demo.
3. **Diapositivas Visualmente Ricas (Cero Repetición)**: Pipelines secuenciales conectados (`1 ➔ 2 ➔ 3 ➔ 4`), comparativas de 2 columnas (Dolor vs. Solución) y tarjetas de métricas/KPIs gigantes (`94%`, `<1.2s`).
4. **Simulador de Ensayo HTML**: Guion a la izquierda, diapositivas a la derecha, botón **"⛶ Agrandar Diapos"** para pantalla completa, cronómetro y acotaciones escénicas adaptadas a modalidad Virtual o Presencial.

## Compilación Rápida
```bash
python scripts/build_full_pitch.py --config assets/templates/full_pitch_schema.json --out-pptx presentacion.pptx --out-html simulador_ensayo.html --assets assets
```
