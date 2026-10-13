# Sistema de Diseño para Presentaciones de Alto Impacto

Este documento especifica la arquitectura visual, medidas exactas y tokens de diseño para crear diapositivas de máximo contraste y legibilidad.

---

## 1. Dimensiones y Lienzo (Canvas)

| Parámetro | Valor en EMU | Proporción |
|---|---|---|
| **16:9 Panorámica (YouTube / Laptop)** | `12192000` x `6858000` | 13.33 x 7.50 pulg. |
| **4:3 Estándar (Escritorio / Proyector)** | `9144000` x `6858000` | 10.00 x 7.50 pulg. |
| **9:16 Vertical (Celular / Reels / Mobile)** | `6858000` x `12192000` | 7.50 x 13.33 pulg. |
| **Tablet / iPad (3:2)** | `10287000` x `6858000` | 11.25 x 7.50 pulg. |

---

## 2. Paleta Cromática y Tokens

```
FONDOS:
  --bg-dark:        #1A1613  (Obsidian Coffee / Fondo de Portada, Actos y Cierre)
  --bg-light:       #F8F5EE  (Alabaster Cream / Fondo de Diapositivas de Contenido)

ACENTOS:
  --accent-terra:   #C94B22  (Terracota / Acento en diapositivas claras)
  --accent-amber:   #EA9B27  (Ámbar Cálido / Acento en diapositivas oscuras)
  --accent-soft:    #EFDEC4  (Crema Suave / Fondos de tarjetas secundarias)

TIPOGRAFÍA:
  --text-dark-hero: #1C1917  (Stone 900 / Títulos principales oscuros)
  --text-dark-body: #57534E  (Stone 600 / Subtítulos y descripciones)
  --text-dark-mute: #A8A29E  (Stone 400 / Categorías y etiquetas superiores)
  --text-light:     #FFFFFF  (Blanco Puro / Títulos en diapositivas oscuras)
  --text-light-sub: #D6D3D1  (Stone 300 / Textos secundarios claros)

BARRA DE NAVEGACIÓN INFERIOR:
  --bar-active-dark:    #EA9B27
  --bar-inactive-dark:  #3A332C
  --bar-active-light:   #C94B22
  --bar-inactive-light: #E7DCC8
```

---

## 3. Barra de Navegación Dinámica con Indicador / Avatar

En la parte inferior de cada diapositiva se ubica un indicador de avance:
- **Eje Y de la barra**: `y = slide_height - 182880` EMU.
- **Segmentación**: $N$ rectángulos proporcionales al total de diapositivas.
- **Indicador / Avatar Caminante**: Ubicado sobre el segmento activo de la diapositiva actual (`i / N`).

---

## 4. Tipos de Diapositivas

1. **`hero_dark`**: Portada con logos institucionales, título principal y tarjeta de propuesta de valor.
2. **`split_comparison`**: Comparativa de 2 columnas (Dolor actual vs. Propuesta de valor).
3. **`flow_pipeline`**: Diagrama de 4 pasos secuenciales conectados con flechas (`1 ➔ 2 ➔ 3 ➔ 4`).
4. **`video_with_flow`**: Video de demostración a la izquierda y flujo de 3 pasos a la derecha.
5. **`metric_kpis`**: 3 tarjetas de métricas gigantes para respaldo empírico.
6. **`act_divider_dark`**: Divisor de acto con vista previa de fases.
7. **`closing_qr_dark`**: Cierre con canales de contacto y código QR dinámico.
