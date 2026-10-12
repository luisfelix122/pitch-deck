---
name: pitch-deck
description: End-to-end generator of winning pitches and PowerPoint presentations. Conducts an interactive step-by-step interview covering project info/rubric, virtual vs presencial mode, allocated time (1, 2, 3, 5+ min), communicator style diagnosis (8 profiles), screen aspect ratio (16:9, 4:3, 9:16 mobile, tablet), institutional identity (UNP - Ingeniería Industrial vs folder files), custom walking avatar for the progress bar (with PIL auto-transparency), custom QR codes, and video slides. Delivers a synchronized PowerPoint deck (.pptx) and a unified interactive rehearsal tool (.html) with split-screen slides and verbatim script, expandable fullscreen slide mode, live countdown timer, and line-by-line stage directions (tone, gaze, hands, pauses). Trigger whenever the user asks for a pitch, pitch deck, hackathon presentation, startup speech, or competition slides.
---

# Pitch-Deck: Sistema Integral de Pitch y Diapositivas Ganadoras

Esta skill unificada guía al usuario a través de un **proceso interactivo de preguntas** y genera en paralelo dos entregables totalmente sincronizados:
1. **La Presentación en PowerPoint (`.pptx`)**: Adaptada a la proporción de pantalla elegida, con barra de navegación inferior, avatar caminante, logos institucionales y diapositivas de video.
2. **La Herramienta de Ensayo Interactiva (`.html`)**: Un visor web con **las diapositivas a un lado y el guion al costado**, botón para **agrandar las diapos** (ocultando el guion), cronómetro dinámico en vivo y acotaciones escénicas (tono, mirada virtual/presencial, manos y pausas).

---

## 1. El Flujo Interactivo de la Skill (Entrevista Paso a Paso)

Al activar esta skill, **debes guiar al usuario mediante estas preguntas consecutivas una por una**:

### Pregunta 1: Información del Proyecto y Rúbrica
> *"¿La información, problema o propuesta de tu proyecto (y las bases o rúbrica de calificación del jurado si las tienes) ya se encuentran en algún documento dentro de la carpeta (ej. notas, PDF, Word, txt), o la vamos a definir / escribir juntos por aquí en el chat?"*
- Si ya existe en la carpeta: Lee el documento para extraer la propuesta de valor y los criterios de evaluación.
- Si se escribe por chat: Recopila la información esencial del proyecto.

### Pregunta 2: Modalidad de la Presentación (Virtual o Presencial)
> *"¿La presentación será en modalidad **virtual** (vía Zoom, Meet, Teams) o **presencial** (en escenario o auditorio físico)?"*
- **Si es Virtual**: Las acotaciones escénicas indicarán mirar fijamente al lente de la cámara (no a las caras en la pantalla), encuadre en plano medio, distancia constante al micrófono de auriculares e iluminación frontal.
- **Si es Presencial**: Las acotaciones indicarán postura física de poder, recorrido visual por los jueces, proyección diafragmática de voz y manejo de micrófono de mano (a 2-3 dedos).

### Pregunta 3: Tiempo Asignado al Pitch
> *"¿De cuánto tiempo dispones exactamente para tu pitch ante el jurado? (ej. 1 minuto 'elevator pitch', 2 minutos, 3 minutos estándar, 5 minutos o el tiempo que indique tu competencia)"*
- **Matemática estricta** (130 a 140 palabras por minuto):
  * 1 min: 130 a 140 palabras.
  * 2 min: 260 a 280 palabras.
  * 3 min: 390 a 420 palabras.
  * 5 min: 650 a 700 palabras.
  * $T$ min: $\text{Palabras} = T \times [130, 140]$.

### Pregunta 4: Autodiagnóstico de Estilo Comunicativo
Para asegurar autenticidad y no imponer personajes ajenos:
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
En la parte inferior de las diapositivas habrá una barra de avance donde un avatar o mascota camina slide por slide:
> *"¿Cómo te gustaría que sea el avatar o icono que camine sobre la barra de avance?:*
> *(a) ¿Tienes una imagen o logo en la carpeta (o en un doc/chat)? Indícame la ruta o pásamela para procesarla con Python, quitarle el fondo blanco y dejarla con transparencia.*
> *(b) O descríbeme qué personaje, figura o símbolo representativo de tu proyecto te gustaría que usemos."*

### Pregunta 8: Código QR en la Lámina Final (Personalizable)
> *"¿Deseas incluir código QR en la diapositiva final de cierre? Si es así, ¿qué contenido o acción quieres que codifique? (Puede ser un link web/demo, mensaje directo de WhatsApp, vCard de contacto, credenciales Wi-Fi o un texto libre; o dime si prefieres sin QR)"*.

### Pregunta 9: Videos en la Presentación
> *"¿Tienes pensado incluir videos en la presentación (como una demo grabada, testimonio o recorrido de la app)? ¿Cuántos videos (1, 2 o cuántos quieras)?"*
- Se generan diapositivas dedicadas (`video_slide`) con marco adaptado al formato de pantalla seleccionado y guía de reproducción.

---

## 2. Los Dos Entregables Generados

### Entregable 1: La Presentación en PowerPoint (`[nombre_proyecto].pptx`)
* Construida mediante [`scripts/generate_deck.py`](scripts/generate_deck.py):
  - Formato de pantalla elegido (16:9, 4:3, 9:16 vertical, tablet).
  - Contraste visual de alto impacto (Obsidian Dark `#1A1613` para actos/cierre y Warm Cream `#F8F5EE` para contenido).
  - Barra de navegación inferior dinámica con el avatar caminando y contador `i / N`.
  - Logos oficiales transparentes (UNP / Industrial o de proyecto).
  - Diapositivas preparadas para video con contenedor adaptado.
  - Códigos QR nítidos generados con `qrcode`.

### Entregable 2: El Simulador de Ensayo HTML (`pitch-[nombre_proyecto].html`)
* Archivo autónomo único para ensayar y practicar:
  - **Vista Dividida (Split Screen)**: A la izquierda la diapositiva actual renderizada con su barra de progreso y avatar; a la derecha el guion verbatim sincronizado correspondiente a esa lámina.
  - **Botón "⛶ Agrandar Diapos"**: Permite ocultar el panel del guion para proyectar o ensayar con las diapositivas en grande.
  - **Cronómetro Integrado**: Cuenta regresiva en vivo calibrada al tiempo exacto ($T$ minutos) con alertas de color.
  - **Acotaciones Escénicas Sincrónicas**: Muestra el tono sugerido, el foco de la mirada (calibrado según modalidad Virtual o Presencial), la posición de manos y las pausas necesarias.
  - **Navegación Fluida**: Botones Anterior / Siguiente y control con flechas del teclado.

---

## 3. Automatización por Script

Para compilar ambos entregables de forma instantánea a partir de un JSON estructurado:
```bash
python scripts/build_full_pitch.py --config assets/templates/full_pitch_schema.json --out-pptx presentacion.pptx --out-html simulador_ensayo.html --assets assets
```
