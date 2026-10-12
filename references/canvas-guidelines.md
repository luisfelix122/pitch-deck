# Guía de Diseño de Diapositivas Minimalistas: Slide Canvas para 3 Minutos

En un pitch de 3 minutos para hackatón o concurso, el jurado **nunca debe leer diapositivas mientras el expositor habla**. Si el jurado lee un párrafo en pantalla, deja de escuchar la voz del expositor.

---

## 1. Principios del Canvas Minimalista

1. **Fondo Blanco (`#FFFFFF` / `#FAFAFA`)**:
   - Da máxima luminosidad al auditorio, genera sensación de orden, modernidad y pulcritud técnica.
2. **Tipografía Oscura de Alto Contraste (`#0F172A` / `#1E293B`)**:
   - Tipografías sans-serif limpias (Inter, Montserrat, Plus Jakarta Sans o System Sans).
   - Jerarquía visual nítida: Títulos grandes (44px - 64px) y texto secundario breve (20px - 28px).
3. **Regla de Oro: Máximo 6 Palabras por Diapositiva**:
   - Prohibidos los bloques de texto, viñetas interminables o diagramas ilegibles.
   - Cada slide debe ser comprensible en menos de 1.5 segundos.
4. **Paleta de Colores de la Solución (Accento Único)**:
   - Mantener un único color primario de acento que represente la marca de la solución:
     - Sostenibilidad/Eco: Verde esmeralda (`#059669` / `#10B981`)
     - Tecnología/SIG/IA: Azul índigo (`#2563EB` / `#4F46E5`)
     - Alerta/Problema: Coral o ámbar tenue para resaltar una cifra crítica.
5. **Espacio Negativo (Aire Visual)**:
   - Mínimo 40% de la diapositiva debe ser espacio en blanco sin elementos.

---

## 2. Estructura de 5 Diapositivas para 3 Minutos

| # | Diapositiva | Tiempo | Contenido en Pantalla | Función Escénica |
|---|---|---|---|---|
| **1** | **El Gancho / La Pregunta** | 0:00 - 0:35 | Una cifra gigante o una pregunta de impacto (ej. *"¿Y si el 90% se pudiera salvar?"*). | Detener la distracción del jurado y fijar la atención. |
| **2** | **El Dolor Regional** | 0:35 - 1:10 | Una imagen real o dato crudo local (ej. *"Piura: 600 toneladas al día sin clasificar"*). | Validar la urgencia y el tamaño del problema. |
| **3** | **La Solución (El Héroe)** | 1:10 - 2:00 | Nombre del producto + Mockup minimalista o diagrama conceptual de 3 pasos (IA + SIG + Recompensas). | Revelar la propuesta de valor con orgullo. |
| **4** | **Validación & Tracción** | 2:00 - 2:35 | 2 a 3 métricas gigantes (ej. *"400 encuestados \| 94% precisión YOLO \| -35% costos"*). | Destruir el escepticismo técnico y de mercado del jurado. |
| **5** | **El Cierre & Visión** | 2:35 - 3:00 | Frase lema memorable + Nombres del equipo + Logo de la solución. | Dejar el mensaje final grabado en la memoria del tribunal. |

---

## 3. Especificación del Canvas en HTML / CSS

El canvas generado dentro del entregable HTML debe representarse mediante tarjetas interactivas de previsualización que simulen el formato 16:9 de las diapositivas de presentación, permitiendo al usuario exportarlas o usarlas como guía directa en Canva, Figma o PowerPoint.
