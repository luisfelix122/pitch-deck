#!/usr/bin/env python3
"""
Deck-Craft: Generador Universal de Presentaciones de Alto Impacto
Soporta múltiples proporciones de pantalla (16:9 YouTube, 4:3 Escritorio, 9:16 Celular, Tablet),
barra de navegación inferior dinámica con mascota caminante procesada/vectorizada con PIL,
logos institucionales (UNP / FII) y de proyecto, códigos QR con cualquier contenido y diapositivas de video.
"""

import os
import sys
import json
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pptx
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

try:
    import qrcode
except ImportError:
    qrcode = None

# Dimensiones por relación de aspecto
ASPECT_RATIOS = {
    "16:9": (12192000, 6858000),      # Widescreen / YouTube / Laptop (13.33 x 7.5 in)
    "youtube": (12192000, 6858000),
    "laptop": (12192000, 6858000),
    "4:3": (9144000, 6858000),        # Estándar / Escritorio / Proyector clásico (10.0 x 7.5 in)
    "escritorio": (9144000, 6858000),
    "desktop": (9144000, 6858000),
    "9:16": (6858000, 12192000),      # Vertical / Celular / TikTok / Reels (7.5 x 13.33 in)
    "celular": (6858000, 12192000),
    "mobile": (6858000, 12192000),
    "tablet": (10287000, 6858000),    # Tablet / iPad (3:2)
    "ipad": (10287000, 6858000)
}

# Paleta Cromática Exacta
COLOR_BG_DARK = RGBColor(0x1A, 0x16, 0x13)      # Obsidian Coffee
COLOR_BG_LIGHT = RGBColor(0xF8, 0xF5, 0xEE)     # Alabaster Cream
COLOR_TEXT_HERO = RGBColor(0x1C, 0x19, 0x17)    # Stone 900
COLOR_TEXT_BODY = RGBColor(0x57, 0x53, 0x4E)    # Stone 600
COLOR_TEXT_MUTED = RGBColor(0xA8, 0xA2, 0x9E)   # Stone 400
COLOR_TEXT_LIGHT = RGBColor(0xFF, 0xFF, 0xFF)   # Pure White
COLOR_TEXT_LIGHT_SUB = RGBColor(0xD6, 0xD3, 0xD1)# Stone 300
COLOR_ACCENT_AMBER = RGBColor(0xEA, 0x9B, 0x27) # Ámbar Cálido
COLOR_ACCENT_TERRA = RGBColor(0xC9, 0x4B, 0x22) # Terracota Piura
COLOR_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)      # Blanco tarjeta
COLOR_CARD_BORDER = RGBColor(0xE7, 0xE5, 0xE4)  # Borde suave

def process_custom_avatar(image_path: str, output_path: str, tolerance: int = 235) -> str:
    """
    Procesa un avatar o imagen dada por el usuario:
    Elimina fondo blanco/claro convirtiéndolo a canal alfa transparente y recorta bordes vacíos.
    """
    if not os.path.exists(image_path):
        return image_path
    try:
        img = Image.open(image_path).convert("RGBA")
        data = img.getdata()
        new_data = []
        for item in data:
            if item[0] >= tolerance and item[1] >= tolerance and item[2] >= tolerance:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"Advertencia al procesar avatar: {e}")
        return image_path

def generate_qr_image(payload: str, output_path: str):
    """Genera una imagen PNG del código QR para cualquier cadena de datos (URL, vCard, texto, etc.)."""
    if not qrcode or not payload:
        return None
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error generando código QR: {e}")
        return None

def set_slide_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_progress_bar(slide, current_idx, total_slides, is_dark, runner_img_path, slide_w, slide_h):
    """Calcula y dibuja la barra de navegación proporcional al tamaño de diapositiva."""
    bar_margin = int(slide_w * 0.045)
    bar_end = int(slide_w * 0.90)
    available_width = bar_end - bar_margin
    bar_top = int(slide_h - 182880)
    bar_height = 45720
    gap = int(slide_w * 0.003)
    seg_width = int((available_width - (total_slides - 1) * gap) / total_slides)

    color_active = COLOR_ACCENT_AMBER if is_dark else COLOR_ACCENT_TERRA
    color_inactive = RGBColor(0x3A, 0x33, 0x2C) if is_dark else RGBColor(0xE7, 0xDC, 0xC8)

    current_seg_left = bar_margin
    for i in range(total_slides):
        x = bar_margin + i * (seg_width + gap)
        seg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, bar_top, seg_width, bar_height)
        seg.fill.solid()
        seg.line.fill.background()
        if i <= current_idx:
            seg.fill.fore_color.rgb = color_active
        else:
            seg.fill.fore_color.rgb = color_inactive

        if i == current_idx:
            current_seg_left = x

    # Mascota caminante
    runner_w = int(slide_w * 0.023)
    runner_h = int(runner_w * 1.1)
    runner_top = bar_top - runner_h - 10000

    if runner_img_path and os.path.exists(runner_img_path):
        runner_left = int(current_seg_left + (seg_width - runner_w) / 2)
        slide.shapes.add_picture(runner_img_path, runner_left, runner_top, runner_w, runner_h)

    # Contador textual a la derecha
    counter_w = int(slide_w * 0.08)
    counter_box = slide.shapes.add_textbox(bar_end + 50000, bar_top - 60000, counter_w, 228600)
    tf = counter_box.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"{current_idx + 1} / {total_slides}"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_LIGHT_SUB if is_dark else COLOR_TEXT_MUTED

def build_presentation(data: dict, output_file: str, assets_dir: str):
    prs = pptx.Presentation()
    settings = data.get("settings", {})
    aspect_key = str(settings.get("aspect_ratio", "16:9")).lower()
    slide_w, slide_h = ASPECT_RATIOS.get(aspect_key, ASPECT_RATIOS["16:9"])
    prs.slide_width = slide_w
    prs.slide_height = slide_h
    blank_layout = prs.slide_layouts[6]

    meta = data.get("meta", {})
    slides_data = data.get("slides", [])
    total_slides = len(slides_data)

    # Logos institucionales
    unp_logo = os.path.join(assets_dir, "logos", "unp_logo_transparent.png")
    fii_logo = os.path.join(assets_dir, "logos", "fii_logo_transparent.png")
    if not os.path.exists(unp_logo):
        unp_logo = os.path.join(assets_dir, "logos", "unp_logo.png")
    if not os.path.exists(fii_logo):
        fii_logo = os.path.join(assets_dir, "logos", "fii_logo.png")

    # Avatar / Runner
    runner_logo = os.path.join(assets_dir, "logos", "chasqui_runner.png")
    custom_avatar = settings.get("custom_avatar_path")
    if custom_avatar and os.path.exists(custom_avatar):
        processed_path = os.path.join(assets_dir, "logos", "processed_avatar.png")
        runner_logo = process_custom_avatar(custom_avatar, processed_path)

    for idx, sdata in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)
        stype = sdata.get("type", "content_light")
        is_dark = "dark" in stype

        if is_dark:
            set_slide_background(slide, COLOR_BG_DARK)
        else:
            set_slide_background(slide, COLOR_BG_LIGHT)

        margin_x = int(slide_w * 0.045)
        content_w = int(slide_w * 0.91)

        # 1. RENDERIZADO POR TIPO DE DIAPOSITIVA
        if stype == "hero_dark":
            # Logos
            logo_x = margin_x
            logo_size = int(slide_h * 0.12)
            logo_y = int(slide_h * 0.07)
            if settings.get("include_unp_logo", True) and os.path.exists(unp_logo):
                slide.shapes.add_picture(unp_logo, logo_x, logo_y, logo_size, logo_size)
                logo_x += int(logo_size * 1.15)
            if settings.get("include_fii_logo", True) and os.path.exists(fii_logo):
                slide.shapes.add_picture(fii_logo, logo_x, logo_y, logo_size, logo_size)
                logo_x += int(logo_size * 1.15)

            # Título principal
            title_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.28), int(content_w * 0.58), int(slide_h * 0.30))
            tf = title_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = sdata.get("title", meta.get("title", "Título del Proyecto"))
            p.font.name = "Calibri"
            p.font.size = Pt(36 if aspect_key != "9:16" else 28)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_LIGHT

            # Subtítulo
            sub_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.59), int(content_w * 0.55), int(slide_h * 0.15))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = sdata.get("subtitle", meta.get("subtitle", ""))
            p_sub.font.name = "Calibri"
            p_sub.font.size = Pt(17 if aspect_key != "9:16" else 14)
            p_sub.font.color.rgb = COLOR_TEXT_LIGHT_SUB

            # Autor
            author_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.81), int(content_w * 0.55), 365760)
            tf_auth = author_box.text_frame
            p_auth = tf_auth.paragraphs[0]
            p_auth.text = sdata.get("author_line", f"{meta.get('author', '')}  ·  {meta.get('event', '')}")
            p_auth.font.name = "Calibri"
            p_auth.font.size = Pt(12)
            p_auth.font.bold = True
            p_auth.font.color.rgb = COLOR_ACCENT_AMBER

            # Tarjeta Hero lateral
            if aspect_key != "9:16":
                hero_x = int(slide_w * 0.61)
                hero_w = int(slide_w * 0.34)
                hero_h = int(slide_h * 0.67)
                hero_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, hero_x, int(slide_h * 0.16), hero_w, hero_h)
                hero_card.fill.solid()
                hero_card.fill.fore_color.rgb = RGBColor(0x2A, 0x24, 0x1E)
                hero_card.line.color.rgb = COLOR_ACCENT_AMBER
                hero_card.line.width = Pt(1.5)

        elif stype == "act_divider_dark":
            badge = slide.shapes.add_textbox(margin_x, int(slide_h * 0.29), int(content_w * 0.5), 365760)
            p = badge.text_frame.paragraphs[0]
            p.text = sdata.get("act_number", "ACTO")
            p.font.name = "Calibri"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = COLOR_ACCENT_AMBER

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.36), int(content_w * 0.6), int(slide_h * 0.2))
            p = tbox.text_frame.paragraphs[0]
            p.text = sdata.get("title", "")
            p.font.name = "Calibri"
            p.font.size = Pt(34 if aspect_key != "9:16" else 26)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_LIGHT

            dbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.54), int(content_w * 0.6), int(slide_h * 0.2))
            tf_d = dbox.text_frame
            tf_d.word_wrap = True
            p = tf_d.paragraphs[0]
            p.text = sdata.get("description", "")
            p.font.name = "Calibri"
            p.font.size = Pt(16)
            p.font.color.rgb = COLOR_TEXT_LIGHT_SUB

        elif stype == "content_light":
            cat_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.056), int(content_w * 0.5), 292608)
            p_cat = cat_box.text_frame.paragraphs[0]
            p_cat.text = sdata.get("category", "SISTEMA")
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_TEXT_MUTED

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.11), content_w, int(slide_h * 0.13))
            tf = tbox.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            p_t.text = sdata.get("title", "")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(25 if aspect_key != "9:16" else 20)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_HERO

            points = sdata.get("points", [])
            card_top = int(slide_h * 0.27)
            card_h = int(slide_h * 0.16)
            gap_c = int(slide_h * 0.035)
            for p_idx, pt_text in enumerate(points[:3]):
                y = card_top + p_idx * (card_h + gap_c)
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, margin_x, y, content_w, card_h)
                card.fill.solid()
                card.fill.fore_color.rgb = COLOR_CARD_BG
                card.line.color.rgb = COLOR_CARD_BORDER
                card.line.width = Pt(1)

                ctext = slide.shapes.add_textbox(margin_x + int(slide_w * 0.02), y + int(card_h * 0.15), content_w - int(slide_w * 0.04), card_h)
                tf_c = ctext.text_frame
                tf_c.word_wrap = True
                p_c = tf_c.paragraphs[0]
                p_c.text = f"•  {pt_text}"
                p_c.font.name = "Calibri"
                p_c.font.size = Pt(16 if aspect_key != "9:16" else 13)
                p_c.font.color.rgb = COLOR_TEXT_BODY

        elif stype == "video_slide":
            cat_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.056), int(content_w * 0.5), 292608)
            p_cat = cat_box.text_frame.paragraphs[0]
            p_cat.text = sdata.get("category", "DEMOSTRACIÓN EN VIDEO")
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_ACCENT_TERRA

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.10), content_w, int(slide_h * 0.1))
            tf = tbox.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            p_t.text = sdata.get("title", "Demostración de Producto")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(25 if aspect_key != "9:16" else 20)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_HERO

            # Contenedor de Video
            vw = int(content_w * 0.85)
            vh = int(slide_h * 0.62)
            vx = int((slide_w - vw) / 2)
            vy = int(slide_h * 0.23)

            vcard = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vx, vy, vw, vh)
            vcard.fill.solid()
            vcard.fill.fore_color.rgb = COLOR_BG_DARK
            vcard.line.color.rgb = COLOR_ACCENT_TERRA
            vcard.line.width = Pt(2)

            vtext = slide.shapes.add_textbox(vx, vy + int(vh * 0.35), vw, int(vh * 0.3))
            tf_v = vtext.text_frame
            p_v = tf_v.paragraphs[0]
            p_v.alignment = PP_ALIGN.CENTER
            p_v.text = f"▶  [CONTENEDOR DE VIDEO]\n{sdata.get('video_filename', 'demo.mp4')}"
            p_v.font.name = "Calibri"
            p_v.font.size = Pt(20 if aspect_key != "9:16" else 15)
            p_v.font.bold = True
            p_v.font.color.rgb = COLOR_TEXT_LIGHT

            p_v2 = tf_v.add_paragraph()
            p_v2.alignment = PP_ALIGN.CENTER
            p_v2.text = "Incruste el video en PowerPoint (Insertar > Multimedia > Video)"
            p_v2.font.name = "Calibri"
            p_v2.font.size = Pt(12)
            p_v2.font.color.rgb = COLOR_TEXT_LIGHT_SUB

        elif stype == "closing_qr_dark":
            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.26), int(content_w * 0.55), int(slide_h * 0.16))
            p_t = tbox.text_frame.paragraphs[0]
            p_t.text = sdata.get("title", "¡Muchas Gracias!")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(40 if aspect_key != "9:16" else 28)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_LIGHT

            sub_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.44), int(content_w * 0.55), int(slide_h * 0.15))
            tf_s = sub_box.text_frame
            tf_s.word_wrap = True
            p_s = tf_s.paragraphs[0]
            p_s.text = sdata.get("subtitle", "Conversemos sobre innovación y alianzas.")
            p_s.font.name = "Calibri"
            p_s.font.size = Pt(17 if aspect_key != "9:16" else 13)
            p_s.font.color.rgb = COLOR_TEXT_LIGHT_SUB

            cbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.63), int(content_w * 0.55), int(slide_h * 0.25))
            tf_c = cbox.text_frame
            lines = sdata.get("contact_lines", [meta.get("contact_web", ""), meta.get("contact_github", ""), meta.get("contact_email", "")])
            for l_idx, line in enumerate(lines):
                if l_idx == 0:
                    p_l = tf_c.paragraphs[0]
                else:
                    p_l = tf_c.add_paragraph()
                p_l.text = line
                p_l.font.name = "Calibri"
                p_l.font.size = Pt(14)
                p_l.font.color.rgb = COLOR_ACCENT_AMBER

            # Códigos QR dinámicos (cualquier contenido o texto)
            qr_cfg = settings.get("qr_config", {})
            if qr_cfg.get("enabled", True):
                os.makedirs("temp_qr", exist_ok=True)
                primary = qr_cfg.get("primary", {})
                qr_content = primary.get("payload") or primary.get("url") or "https://chasqui.chat"
                qr_img = generate_qr_image(qr_content, "temp_qr/qr_primary.png")

                qr_card_w = int(slide_w * 0.18) if aspect_key != "9:16" else int(slide_w * 0.35)
                qr_card_x = int(slide_w * 0.60) if aspect_key != "9:16" else int(slide_w * 0.55)
                qr_card_y = int(slide_h * 0.29)

                card1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qr_card_x, qr_card_y, qr_card_w, qr_card_w)
                card1.fill.solid()
                card1.fill.fore_color.rgb = COLOR_CARD_BG
                card1.line.fill.background()

                if qr_img and os.path.exists(qr_img):
                    pad = int(qr_card_w * 0.06)
                    slide.shapes.add_picture(qr_img, qr_card_x + pad, qr_card_y + pad, qr_card_w - 2*pad, qr_card_w - 2*pad)

                label_box = slide.shapes.add_textbox(qr_card_x, qr_card_y + qr_card_w + 100000, qr_card_w, 640080)
                tf_lbl = label_box.text_frame
                tf_lbl.word_wrap = True
                p_lbl = tf_lbl.paragraphs[0]
                p_lbl.text = primary.get("label", "Escanea aquí")
                p_lbl.font.name = "Calibri"
                p_lbl.font.size = Pt(11)
                p_lbl.font.bold = True
                p_lbl.font.color.rgb = COLOR_TEXT_LIGHT

                p_desc = tf_lbl.add_paragraph()
                p_desc.text = primary.get("description", "")
                p_desc.font.name = "Calibri"
                p_desc.font.size = Pt(9.5)
                p_desc.font.color.rgb = COLOR_TEXT_LIGHT_SUB

        # 2. BARRA DE PROGRESO INFERIOR DINÁMICA
        add_progress_bar(slide, idx, total_slides, is_dark, runner_logo, slide_w, slide_h)

    prs.save(output_file)
    print(f"✅ Presentación generada exitosamente: {output_file}")
    print(f"   Total diapositivas: {total_slides} | Formato: {aspect_key.upper()} ({slide_w}x{slide_h} EMU)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deck-Craft: Generador de presentaciones")
    parser.add_argument("--config", "-c", required=True, help="Ruta al archivo JSON de configuración")
    parser.add_argument("--output", "-o", default="presentacion_generada.pptx", help="Archivo PPTX de salida")
    parser.add_argument("--assets", "-a", default="assets", help="Directorio de assets")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    build_presentation(config_data, args.output, args.assets)
