# Skill Pitch-Deck: Discurso Ganador y Diapositivas PPTX Unificadas

Skill todo-en-uno para agentes de IA que integra la preparación y redacción del **pitch de alto impacto** con la generación automática de la **presentación en PowerPoint (`.pptx`)** y un **simulador de ensayo web en HTML**.

## Entrevista Interactiva (Paso a Paso)
1. **Información del Proyecto y Rúbrica**: Desde archivo local o redactado por el chat.
2. **Modalidad**: Virtual (lente de cámara, encuadre, micro headset) vs. Presencial (escenario, mirada a jueces, micro de mano).
3. **Tiempo Exacto**: Calibra la cantidad estricta de palabras ($T \times 130\text{--}140$ palabras).
4. **Autodiagnóstico**: 2 preguntas para perfilar el estilo natural del orador.
5. **Formato de Pantalla**: 16:9 Panorámica (YouTube), 4:3 (Escritorio), 9:16 Vertical (Celular/Reels), Tablet.
6. **Identidad Institucional**: UNP - Ingeniería Industrial (logos oficiales con transparencia) o logos del proyecto.
7. **Avatar Caminante**: Personalizado (imagen en archivo/chat vectorizada con PIL o descrito).
8. **Código QR Final**: URLs, WhatsApp, vCard o texto libre.
9. **Videos**: Diapositivas dedicadas con contenedor dimensionado según la pantalla elegida.

## Entregables Producidos
* **`[proyecto].pptx`**: Presentación PowerPoint lista para proyectar.
* **`pitch-[proyecto].html`**: Simulador de ensayo en el navegador con **diapositivas a un lado y guion al costado**, botón para **agrandar diapos** a pantalla completa, cronómetro en vivo y acotaciones escénicas sincronizadas.

## Compilación
```bash
python scripts/build_full_pitch.py --config assets/templates/full_pitch_schema.json --out-pptx presentacion.pptx --out-html simulador_ensayo.html --assets assets
```
