# Guía de Inserción y Optimización de Videos en PowerPoint

Esta guía detalla cómo integrar videos de demostración (demos técnicas, prototipos de software, testimonios) dentro de las diapositivas generadas con la skill **Chasqui-Slides**.

---

## 1. Dónde colocar los videos

Cuando el generador crea diapositivas con contenedor de video, reserva el marco central exacto:
- Guarda tus archivos de video en la carpeta `assets/videos/` de tu proyecto.
- Formato recomendado: **`.mp4` (Códec de video H.264, audio AAC)**.
- Resolución óptima: **1080p (1920x1080)** a 30 o 60 fps.

---

## 2. Inserción en PowerPoint (Paso a Paso)

1. Abre el archivo `.pptx` generado en PowerPoint.
2. Ve a la diapositiva marcada con **`[CONTENEDOR DE VIDEO]`**.
3. En la barra superior, haz clic en **Insertar** > **Multimedia** > **Video** > **Este dispositivo...**.
4. Selecciona tu archivo `.mp4`.
5. Arrastra el video para que calce exactamente sobre el marco gris diseñado en la diapositiva.

---

## 3. Configuración de Reproducción Profesional

Con el video seleccionado, ve a la pestaña **Reproducción (Playback)** en PowerPoint:

- **Inicio**:
  - Si es una demo que debes explicar mientras corre: Elige **Automáticamente**.
  - Si vas a hablar antes de mostrarlo: Elige **Al hacer clic en él**.
- **Volumen**: Si el video tiene música de fondo alta, ajústalo en **Bajo** o **Silenciar** para que tu voz con el micrófono no compita.
- **Loop**: Si es un video corto de 5-10 segundos mostrando una interfaz en acción, marca **Repetir la reproducción hasta su interrupción**.

---

## 4. Recorte de Video dentro de PowerPoint

Si tu grabación de pantalla tiene segundos muertos al inicio o al final:
1. En la pestaña **Reproducción**, haz clic en **Recortar video**.
2. Mueve el marcador verde al segundo exacto donde comienza la acción.
3. Mueve el marcador rojo donde termina la demostración.
4. Haz clic en **Aceptar**. PowerPoint guarda el recorte sin necesidad de editores externos.

---

## 5. Recorte Previo con FFmpeg (Opcional por CLI)

Si deseas recortar tu video antes de insertarlo en la presentación:
```bash
# Recortar desde el segundo 5 hasta el segundo 25 sin pérdida de calidad:
ffmpeg -i input_video.mp4 -ss 00:00:05 -to 00:00:25 -c copy assets/videos/demo_recortada.mp4
```
