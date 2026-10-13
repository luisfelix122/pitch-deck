# Guía de Inserción y Gestión Segura de Videos en PowerPoint

Esta guía detalla cómo integrar videos de demostración (demos de producto, prototipos, recorridos de interfaz) de manera segura y confiable para que la presentación nunca falle durante el pitch en vivo.

---

## 1. Reglas de Seguridad para Videos en Presentaciones en Vivo

Presentar en vivo con videos tiene riesgos típicos que se resuelven con estas precauciones:

1. **Videos 100% Locales (Cero Dependencia de Internet)**:
   - Nunca confíes en conexiones Wi-Fi del evento para reproducir videos desde YouTube o la nube.
   - Guarda los archivos directamente en la carpeta `videos/` dentro del proyecto.
2. **Formato Universal Confiable**:
   - Usa exclusivamente formato **`.mp4` (Códec de video H.264, audio AAC)**. Es el formato que PowerPoint reproduce sin exigir códecs externos en cualquier computadora.
3. **Control del Audio**:
   - Si vas a hablar encima del video mientras corre: Configura el volumen en **Silenciar** en PowerPoint para que tu voz con el micrófono sea la única protagonista.
4. **Respaldos Visuales**:
   - Cada diapositiva de video generada incluye un **diagrama de flujo paso a paso al costado**. Si por cualquier imprevisto técnico el video no reproduce, el flujo lateral te permite explicar la demo con total claridad sin perder el ritmo.

---

## 2. Inserción en PowerPoint (Paso a Paso)

1. Abre tu archivo `.pptx`.
2. Ve a la diapositiva marcada con **`[VIDEO: videos/nombre.mp4]`**.
3. Haz clic en **Insertar** > **Multimedia** > **Video** > **Este dispositivo...**.
4. Selecciona tu archivo desde la carpeta `videos/`.
5. Ajusta el tamaño al contenedor diseñado en la lámina.

---

## 3. Configuración de Reproducción

Con el video seleccionado en PowerPoint:
- **Pestaña Reproducción**:
  - **Iniciar**: Selecciona **Automáticamente** si deseas que arranque al pasar a esa diapositiva, o **Al hacer clic** si prefieres introducirlo antes.
  - Marca **Repetir la reproducción hasta su interrupción** si es un loop corto de interfaz de 5 a 10 segundos.

---

## 4. Recorte Rápido sin Programas Externos
1. En PowerPoint, ve a **Reproducción** > **Recortar video**.
2. Mueve los marcadores de inicio y fin para quedarte solo con la parte esencial del producto.
3. Haz clic en **Aceptar**.
