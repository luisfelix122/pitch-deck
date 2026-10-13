---
name: pitch-deck
description: End-to-end generator of winning pitches, non-repetitive visual slide decks (.pptx), and interactive split-screen rehearsal tools (.html). Includes automated video tools (trimming, retiming, generating demo clips via FFmpeg and HyperFrames), side-by-side video with step-by-step workflow diagrams, rich diagram layouts (pipelines, 2-column comparisons, big metric KPIs), dynamic walking avatar progress bar, UNP/FII logos, and custom QR codes. Delivers synchronized speech script, PPTX presentation, and HTML rehearsal simulator with expandable fullscreen mode. Trigger whenever the user asks for a pitch, pitch deck, hackathon presentation, startup speech, video slides, or competition deck.
---

# Pitch-Deck: Sistema Integral de Pitch, Diapositivas Visuales y Videos

Esta skill unificada guía al usuario a través de una **entrevista interactiva paso a paso**, evitando plantillas monótonas o repetitivas, y genera tres herramientas coordinadas:
1. **La Presentación en PowerPoint (`.pptx`)**: Con videos incrustados directamente listos para reproducir al abrir la lámina, layouts variados (pipelines de flujo, comparativas de 2 columnas, tarjetas de métricas gigantes, video con flujo lateral paso a paso, y cierre con QR).
2. **Los Videos de Demostración (`videos/`)**: Recortados, retemporizados y ajustados en velocidad con `scripts/video_tools.py` (FFmpeg) o generados con `heygen-com/hyperframes`.
3. **El Simulador de Ensayo HTML (`.html`)**: Con el **guion a la izquierda** y las **diapositivas a la derecha**, botón **"⛶ Agrandar Diapos"** para pantalla completa, cronómetro y acotaciones escénicas (virtual o presencial).

---

## 1. El Flujo Interactivo de la Skill (Entrevista Paso a Paso)

Al activar esta skill, **debes guiar al usuario mediante estas preguntas consecutivas una por una**:

### Pregunta 1: Información del Proyecto y Rúbrica
> *"¿La información, problema o propuesta de tu proyecto (y las bases o rúbrica de calificación del jurado si las tienes) ya se encuentran en algún documento dentro de la carpeta (ej. notas, PDF, Word, txt), o la vamos a definir / escribir juntos por aquí en el chat?"*
- Si ya existe en la carpeta: Lee el documento para extraer la propuesta de valor y los criterios de evaluación.
- Si se escribe por chat: Recopila la información esencial del proyecto.

### Pregunta 2: Modalidad de la Presentación (Virtual o Presencial)
> *"¿La presentación será en modalidad **virtual** (vía Zoom, Meet, Teams) o **presencial** (en escenario o auditorio físico)?"*
- **Si es Virtual**: Las acotaciones indicarán mirar fijamente al lente de la cámara (no a las caras en la pantalla), encuadre en plano medio, distancia constante al micrófono de headset e iluminación frontal.
- **Si es Presencial**: Las acotaciones indicarán postura física de poder, recorrido visual por los jueces, proyección diafragmática de voz y manejo de micrófono de mano (a 2-3 dedos).

### Pregunta 3: Tiempo Asignado al Pitch
> *"¿De cuánto tiempo dispones exactamente para tu pitch ante el jurado? (ej. 1 minuto 'elevator pitch', 2 minutos, 3 minutos estándar, 5 minutos o el tiempo que indique tu concurso)"*
- **Matemática estricta** (130 a 140 palabras por minuto):
  * 1 min: 130 a 140 palabras.
  * 2 min: 260 a 280 palabras.
  * 3 min: 390 a 420 palabras.
  * 5 min: 650 a 700 palabras.
  * $T$ min: $\text{Palabras} = T \times [130, 140]$.

### Pregunta 4: Autodiagnóstico de Estilo Comunicativo
Para asegurar autenticidad y no imponer personajes ajenos ([references/communicator-styles.md](references/communicator-styles.md)):
> 1. *"Cuando defiendes tu proyecto con pasión, ¿con cuál de estos perfiles te sientes más tú?:*
>    *(a) Cercano y cálido, (b) Serio y formal, (c) Divertido con humor ágil, (d) Directo al grano sin rodeos, (e) Metódico con números y orden, (f) Enérgico y apasionado, (g) Reflexivo y pausado, o (h) Reservado y conciso."*
> 2. *"¿Qué recurso fluye más natural en ti?: Historias de personas reales, datos duros demoledores, silencios y pausas de impacto, o demostraciones en vivo."*

### Pregunta 5: Proporción y Formato de Pantalla (Aspect Ratio)
> *"¿En qué formato o tamaño de pantalla vas a proyectar las diapositivas?:*
> *(a) 16:9 Panorámica ('tipo video de YouTube', laptop o proyector moderno)*
> *(b) 4:3 Clásico (escritorio tradicional, proyector estándar, documentos)*
> *(c) 9:16 Vertical ('tipo celular / smartphone', TikTok, Reels o historias)*
> *(d) 3:2 / Tablet (iPad o pantallas táctiles)"*
- El lienzo del PPTX, las tarjetas y los contenedores de video se dimensionan exactamente en la proporción elegida.

### Pregunta 6: Identidad y Logos Institucionales (UNP - Industrial vs Carpeta)
> *"¿Los logos o imágenes de identidad ya están en algún archivo de la carpeta, o el proyecto pertenece a la **UNP - Ingeniería Industrial** (para cargar automáticamente los escudos oficiales de la Universidad Nacional de Piura y de la Facultad de Ingeniería Industrial con transparencia), o me los vas a pasar por aquí por el chat?"*

### Pregunta 7: Avatar o Icono Caminante de la Barra de Progreso
En la parte inferior de las diapositivas habrá una barra segmentada donde una mascota va **caminando paso a paso** a medida que avanzan las láminas (`1 / N`, `2 / N`, ..., `N / N`):
> *"¿Cómo te gustaría que sea el avatar o icono que camine sobre la barra de avance?:*
> *(a) ¿Tienes una imagen o logo en la carpeta (o en un doc/chat)? Indícame la ruta o pásamela para procesarla con Python, quitarle el fondo blanco y dejarla con transparencia.*
> *(b) O descríbeme qué personaje, figura o símbolo representativo de tu proyecto te gustaría que usemos."*

### Pregunta 8: Videos de Demostración (Creación, Incrustación en PPTX y Flujo Lateral)
Para los videos de la presentación, la skill realizará tres preguntas clave:
> 1. *"¿Deseas incluir videos o demostraciones en movimiento dentro de la presentación?"*
> 2. *(Si la respuesta es sí)*: *"¿Ya tienes grabaciones o archivos de video listos en tu carpeta, o prefieres que la skill los cree/genere automáticamente (usando herramientas como HyperFrames o clips de prueba con FFmpeg ajustados a la velocidad del pitch)?"*
> 3. *"¿Deseas que la skill incruste el video directamente dentro de la diapositiva de PowerPoint (.pptx) final para que esté listo al abrirlo, o prefieres que quede enlazado desde la carpeta `videos/`?"*
> 4. *"Al costado del video colocaremos un **diagrama de flujo de 3 pasos** que explica lo que ocurre en pantalla en tiempo real. ¿Cuáles son esos 3 pasos clave de la demostración?"*
- **Generación e Incrustación Automática en PPTX**: Si el usuario elige que la skill cree e incruste el video, la herramienta genera el clip en `videos/<nombre>.mp4`, extrae automáticamente el fotograma de portada (*poster frame*) con FFmpeg e incrusta el reproductor directamente en la diapositiva PPTX utilizando `slide.shapes.add_movie()`. En caso de que elija no incrustarlo en el PPTX, genera un contenedor estilizado con instrucciones claras para enlazarlo desde la carpeta `videos/`.

### Pregunta 9: Código QR en la Lámina Final (Personalizable)
> *"¿Deseas incluir código QR en la diapositiva final de cierre? Si es así, ¿qué contenido o acción quieres que codifique? (Puede ser un link web/demo, mensaje directo de WhatsApp, vCard de contacto, credenciales Wi-Fi o un texto libre; o dime si prefieres sin QR)"*.

---

## 2. Catálogo de Diapositivas Visualmente Ricas (Cero Repetición)

Para evitar plantillas aburridas con tres cajas repetidas o espacios vacíos, el generador distribuye layouts variados:

1. **`hero_dark` (Portada de Alto Impacto)**:
   - Título principal (36pt bold), subtítulo y autor.
   - Logos en la esquina superior izquierda.
   - **Tarjeta lateral derecha**: Resumen de propuesta de valor y destacados (sin espacios muertos).
2. **`split_comparison` (Comparativa de 2 Columnas)**:
   - Columna Izquierda: *❌ El Dolor / Situación Actual* (fondo sutil rojizo con problemas cuantificados).
   - Columna Derecha: *✅ Nuestra Propuesta* (fondo blanco con acento terracota y ventajas claras).
3. **`flow_pipeline` (Diagrama de Camino / Flujo Secuencial)**:
   - 4 pasos conectados horizontalmente con flechas (`PASO 01 ➔ PASO 02 ➔ PASO 03 ➔ PASO 04`).
   - Cada paso con insignia, título y descripción concisa.
4. **`video_with_flow` (Video + Flujo al Costado)**:
   - Lado izquierdo (58%): Contenedor de video estilizado apuntando a `videos/<nombre>.mp4`.
   - Lado derecho (38%): **Flujo vertical de 3 pasos** explicando qué sucede en la pantalla en tiempo real.
5. **`metric_kpis` (Tarjetas de Métricas Gigantes)**:
   - 3 tarjetas con números gigantes (`94.2%`, `<1.2s`, `400+`) en colores de acento, etiquetas y notas de validación empírica.
6. **`act_divider_dark` (Divisor de Acto)**:
   - Lado izquierdo: Número de acto y título en blanco puro.
   - Lado derecho: Tarjeta de hoja de ruta ("En esta etapa: Paso 1, Paso 2, Paso 3").
7. **`closing_qr_dark` (Cierre Balanceado)**:
   - Lado izquierdo: "¡Muchas Gracias!", llamado a la acción y canales de contacto.
   - Lado derecho: Tarjeta de código QR nítido con etiqueta de escaneo.

---

## 3. Procesamiento y Generación de Videos

La skill incluye `scripts/video_tools.py` potenciado por FFmpeg:

```bash
# Recortar y ajustar velocidad de video al tiempo del pitch:
python scripts/video_tools.py --input video_crudo.mp4 --output videos/demo.mp4 --start 5 --end 35 --target-duration 15

# Generar clip sintético de prueba si no hay video grabado:
python scripts/video_tools.py --create-demo --title "DEMO DEL SISTEMA EN VIVO" --target-duration 15 --output videos/demo.mp4
```

### Integración con HyperFrames (Generación de Videos IA)
Si el usuario desea generar videos promocionales, motion graphics o explainers desde cero:
```bash
# Instalar / usar HyperFrames desde skills.sh:
npx skills use heygen-com/hyperframes@product-launch-video
npx skills use heygen-com/hyperframes@motion-graphics
```

---

## 4. Compilación del Paquete Completo

Con un solo comando compilas el `.pptx`, los videos y el simulador `.html`:
```bash
python scripts/build_full_pitch.py --config assets/templates/full_pitch_schema.json --out-pptx presentacion.pptx --out-html simulador_ensayo.html --assets assets
```
