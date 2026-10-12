# Sistema de Diseño Chasqui (Chasqui Design System)

Este documento especifica la arquitectura visual, medidas exactas y tokens de diseño extraídos directamente de `chasqui-piura-ai.pptx`.

---

## 1. Dimensiones y Lienzo (Canvas)

| Parámetro | Valor en EMU | Valor en Pulgadas / cm |
|---|---|---|
| **Ancho de Diapositiva** | `12192000` | 13.33 pulg. / 33.867 cm (16:9 Widescreen) |
| **Alto de Diapositiva** | `6858000` | 7.50 pulg. / 19.050 cm |
| **Margen Izquierdo Estándar** | `548640` | 0.60 pulg. / 1.524 cm |
| **Margen Derecho Estándar** | `11643360` | 12.73 pulg. |

---

## 2. Paleta Cromática y Tokens

```
FONDOS:
  --bg-dark:        #1A1613  (Obsidian Coffee / Fondo de Portada, Actos y Cierre)
  --bg-light:       #F8F5EE  (Alabaster Cream / Fondo de Diapositivas de Contenido)

ACENTOS Y MARCAS:
  --accent-terra:   #C94B22  (Terracota Piura / Acento en diapositivas claras)
  --accent-amber:   #EA9B27  (Ámbar Cálido / Acento en diapositivas oscuras)
  --accent-soft:    #EFDEC4  (Crema Suave / Fondos de tarjetas secundarias)

TIPOGRAFÍA Y CONTRASTE:
  --text-dark-hero: #1C1917  (Stone 900 / Títulos en diapositivas claras)
  --text-dark-body: #57534E  (Stone 600 / Subtítulos y descripciones)
  --text-dark-mute: #A8A29E  (Stone 400 / Categorías y etiquetas superiores)
  --text-light:     #FFFFFF  (Blanco Puro / Títulos en diapositivas oscuras)
  --text-light-sub: #D6D3D1  (Stone 300 / Textos secundarios en diapositivas oscuras)

BARRA DE NAVEGACIÓN INFERIOR:
  --bar-active-dark:    #EA9B27
  --bar-inactive-dark:  #3A332C
  --bar-active-light:   #C94B22
  --bar-inactive-light: #E7DCC8
```

---

## 3. Tipografías

1. **`Calibri`**: Tipografía principal para títulos, subtítulos, viñetas y descripciones de negocio.
2. **`Cambria`**: Tipografía serif editorial utilizada para enunciados de gran peso o transiciones dramáticas.
3. **`Courier New`**: Tipografía monoespaciada para arquitectura de sistemas, contratos canónicos, endpoints y código.

---

## 4. Barra de Progreso Dinámica y Mascota Caminante

En la parte inferior de cada diapositiva se ubica un indicador de progreso de alta sofisticación:

- **Eje Y de la barra**: `6675120` EMU (~7.3 pulg.)
- **Grosor**: `45720` EMU (~0.05 pulg. / 3.6 pt)
- **Segmentación**: Se calcula dividiendo el ancho disponible entre el número total $N$ de diapositivas.
  - Para $N$ diapositivas, los segmentos del $1$ al $i$ se pintan con el color activo.
  - Los segmentos del $i+1$ al $N$ se pintan con el color inactivo.
- **Mascota o Icono Caminante**:
  - Tamaño: `w = 282915` EMU, `h = 310896` EMU (~0.31 x 0.34 pulg.)
  - Posición Y: `6373368` EMU (flotando exactamente sobre la barra).
  - Posición X: Centrado sobre el segmento activo de la diapositiva actual:
    $$\text{pos\_x} = \text{segmento\_left}[i] + \frac{\text{segmento\_width} - \text{mascota\_width}}{2}$$
- **Contador Numérico**:
  - Caja de texto a la derecha: `left=11000232`, `top=6583680`, texto `i / N` en Calibri 10pt.

---

## 5. Tipos de Diapositivas Estándar

1. **Portada (`hero_dark`)**:
   - Fondo `#1A1613`.
   - Bloque superior izquierdo para logos institucionales (UNP, Facultad de Ingeniería Industrial, Proyecto).
   - Título de impacto (36pt - 44pt), subtítulo explicativo (18pt - 22pt) y autor/evento (12pt).
   - Hero visual a la derecha (4114800 x 4572000 EMU).
2. **Divisor de Acto (`act_divider_dark`)**:
   - Fondo `#1A1613`.
   - Etiqueta de acto en ámbar `#EA9B27`, título en blanco grande, descripción en crema, e imagen/ilustración complementaria.
3. **Contenido Clásico (`content_light`)**:
   - Fondo `#F8F5EE`.
   - Etiqueta de sección en `#A8A29E`, Título en `#1C1917` (28pt).
   - Layout modular: 2 columnas, 3 tarjetas, o diagrama de flujo.
4. **Diapositiva de Video (`video_slide`)**:
   - Contenedor con marco limpio para incrustar 1 o más videos demostrativos.
5. **Cierre y Código QR (`closing_qr_dark`)**:
   - Fondo `#1A1613`.
   - Título "Gracias", llamado a probar la solución, datos de contacto/github, y 1 o 2 tarjetas para códigos QR generados dinámicamente.
