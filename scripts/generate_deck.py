#!/usr/bin/env python3
"""
Deck-Craft: Generador Universal de Presentaciones de Alto Impacto
Soporta múltiples proporciones de pantalla (16:9, 4:3, 9:16, Tablet),
layouts visuales ricos y no repetitivos (Pipeline de flujo, Arquitectura de capas,
Tarjetas de KPIs/Métricas, Video con flujo lateral, Comparativas 2 columnas),
barra de navegación inferior dinámica con avatar caminante, logos institucionales (UNP / FII)
y códigos QR dinámicos.
"""

import os
import sys
import json
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import pptx
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

try:
    import qrcode
except ImportError:
    qrcode = None

ASPECT_RATIOS = {
    "16:9": (12192000, 6858000),
    "youtube": (12192000, 6858000),
    "laptop": (12192000, 6858000),
    "4:3": (9144000, 6858000),
    "escritorio": (9144000, 6858000),
    "desktop": (9144000, 6858000),
    "9:16": (6858000, 12192000),
    "celular": (6858000, 12192000),
    "mobile": (6858000, 12192000),
    "tablet": (10287000, 6858000),
    "ipad": (10287000, 6858000)
}

COLOR_BG_DARK = RGBColor(0x1A, 0x16, 0x13)
COLOR_BG_LIGHT = RGBColor(0xF8, 0xF5, 0xEE)
COLOR_TEXT_HERO = RGBColor(0x1C, 0x19, 0x17)
COLOR_TEXT_BODY = RGBColor(0x57, 0x53, 0x4E)
COLOR_TEXT_MUTED = RGBColor(0xA8, 0xA2, 0x9E)
COLOR_TEXT_LIGHT = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_TEXT_LIGHT_SUB = RGBColor(0xD6, 0xD3, 0xD1)
COLOR_ACCENT_AMBER = RGBColor(0xEA, 0x9B, 0x27)
COLOR_ACCENT_TERRA = RGBColor(0xC9, 0x4B, 0x22)
COLOR_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_CARD_BORDER = RGBColor(0xE7, 0xE5, 0xE4)
COLOR_CARD_DARK = RGBColor(0x2A, 0x24, 0x1E)

def process_custom_avatar(image_path: str, output_path: str, tolerance: int = 235) -> str:
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
        print(f"Advertencia avatar: {e}")
        return image_path

def generate_qr_image(payload: str, output_path: str):
    if not qrcode or not payload:
        return None
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
        qr.add_data(payload)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error QR: {e}")
        return None

def set_slide_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_progress_bar(slide, current_idx, total_slides, is_dark, runner_img_path, slide_w, slide_h):
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

    runner_w = int(slide_w * 0.024)
    runner_h = int(runner_w * 1.1)
    runner_top = bar_top - runner_h - 8000

    if runner_img_path and os.path.exists(runner_img_path):
        runner_left = int(current_seg_left + (seg_width - runner_w) / 2)
        slide.shapes.add_picture(runner_img_path, runner_left, runner_top, runner_w, runner_h)

    counter_w = int(slide_w * 0.08)
    counter_box = slide.shapes.add_textbox(bar_end + 40000, bar_top - 60000, counter_w, 228600)
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

    unp_logo = os.path.join(assets_dir, "logos", "unp_logo_transparent.png")
    fii_logo = os.path.join(assets_dir, "logos", "fii_logo_transparent.png")
    if not os.path.exists(unp_logo):
        unp_logo = os.path.join(assets_dir, "logos", "unp_logo.png")
    if not os.path.exists(fii_logo):
        fii_logo = os.path.join(assets_dir, "logos", "fii_logo.png")

    runner_logo = os.path.join(assets_dir, "logos", "runner_indicator.png")
    custom_avatar = settings.get("custom_avatar_path")
    if custom_avatar and os.path.exists(custom_avatar):
        processed_path = os.path.join(assets_dir, "logos", "processed_avatar.png")
        runner_logo = process_custom_avatar(custom_avatar, processed_path)

    for idx, sdata in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)
        stype = sdata.get("type", "content_light")
        is_dark = "dark" in stype

        set_slide_background(slide, COLOR_BG_DARK if is_dark else COLOR_BG_LIGHT)

        margin_x = int(slide_w * 0.045)
        content_w = int(slide_w * 0.91)

        # -------------------------------------------------------------
        # 1. PORTADA HERO (HERO_DARK)
        # -------------------------------------------------------------
        if stype == "hero_dark":
            logo_x = margin_x
            logo_size = int(slide_h * 0.12)
            logo_y = int(slide_h * 0.07)
            if settings.get("include_unp_logo", True) and os.path.exists(unp_logo):
                slide.shapes.add_picture(unp_logo, logo_x, logo_y, logo_size, logo_size)
                logo_x += int(logo_size * 1.15)
            if settings.get("include_fii_logo", True) and os.path.exists(fii_logo):
                slide.shapes.add_picture(fii_logo, logo_x, logo_y, logo_size, logo_size)
                logo_x += int(logo_size * 1.15)

            title_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.28), int(content_w * 0.58), int(slide_h * 0.30))
            tf = title_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = sdata.get("title", meta.get("title", "Título del Proyecto"))
            p.font.name = "Calibri"
            p.font.size = Pt(36 if aspect_key != "9:16" else 28)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_LIGHT

            sub_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.59), int(content_w * 0.55), int(slide_h * 0.15))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = sdata.get("subtitle", meta.get("subtitle", ""))
            p_sub.font.name = "Calibri"
            p_sub.font.size = Pt(17 if aspect_key != "9:16" else 14)
            p_sub.font.color.rgb = COLOR_TEXT_LIGHT_SUB

            author_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.81), int(content_w * 0.55), 365760)
            tf_auth = author_box.text_frame
            p_auth = tf_auth.paragraphs[0]
            p_auth.text = sdata.get("author_line", f"{meta.get('author', '')}  ·  {meta.get('event', '')}")
            p_auth.font.name = "Calibri"
            p_auth.font.size = Pt(12)
            p_auth.font.bold = True
            p_auth.font.color.rgb = COLOR_ACCENT_AMBER

            # Tarjeta Hero con métricas/destacados para que NO quede vacía
            if aspect_key != "9:16":
                hero_x = int(slide_w * 0.61)
                hero_w = int(slide_w * 0.34)
                hero_h = int(slide_h * 0.67)
                hero_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, hero_x, int(slide_h * 0.16), hero_w, hero_h)
                hero_card.fill.solid()
                hero_card.fill.fore_color.rgb = COLOR_CARD_DARK
                hero_card.line.color.rgb = COLOR_ACCENT_AMBER
                hero_card.line.width = Pt(1.5)

                hero_tf = hero_card.text_frame
                hero_tf.word_wrap = True
                hp1 = hero_tf.paragraphs[0]
                hp1.text = "PROPUESTA DE VALOR"
                hp1.font.name = "Calibri"
                hp1.font.size = Pt(12)
                hp1.font.bold = True
                hp1.font.color.rgb = COLOR_ACCENT_AMBER

                hp2 = hero_tf.add_paragraph()
                hp2.text = sdata.get("highlight", "Innovación validada para resolver el problema de raíz con alto impacto regional.")
                hp2.font.name = "Calibri"
                hp2.font.size = Pt(14)
                hp2.font.color.rgb = COLOR_TEXT_LIGHT_SUB

        # -------------------------------------------------------------
        # 2. DIVISOR DE ACTO (ACT_DIVIDER_DARK)
        # -------------------------------------------------------------
        elif stype == "act_divider_dark":
            badge = slide.shapes.add_textbox(margin_x, int(slide_h * 0.28), int(content_w * 0.5), 365760)
            p = badge.text_frame.paragraphs[0]
            p.text = sdata.get("act_number", "ACTO")
            p.font.name = "Calibri"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = COLOR_ACCENT_AMBER

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.35), int(content_w * 0.55), int(slide_h * 0.2))
            p = tbox.text_frame.paragraphs[0]
            p.text = sdata.get("title", "")
            p.font.name = "Calibri"
            p.font.size = Pt(34 if aspect_key != "9:16" else 26)
            p.font.bold = True
            p.font.color.rgb = COLOR_TEXT_LIGHT

            dbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.55), int(content_w * 0.55), int(slide_h * 0.2))
            tf_d = dbox.text_frame
            tf_d.word_wrap = True
            p = tf_d.paragraphs[0]
            p.text = sdata.get("description", "")
            p.font.name = "Calibri"
            p.font.size = Pt(16)
            p.font.color.rgb = COLOR_TEXT_LIGHT_SUB

            # Tarjeta de roadmap / pasos en el lado derecho
            if aspect_key != "9:16":
                rx = int(slide_w * 0.60)
                rw = int(slide_w * 0.35)
                rh = int(slide_h * 0.60)
                rcard = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, int(slide_h * 0.20), rw, rh)
                rcard.fill.solid()
                rcard.fill.fore_color.rgb = COLOR_CARD_DARK
                rcard.line.color.rgb = RGBColor(0x3A, 0x33, 0x2C)
                rtf = rcard.text_frame
                rtf.word_wrap = True
                rp1 = rtf.paragraphs[0]
                rp1.text = "EN ESTA ETAPA:"
                rp1.font.name = "Calibri"
                rp1.font.size = Pt(12)
                rp1.font.bold = True
                rp1.font.color.rgb = COLOR_ACCENT_AMBER

                steps = sdata.get("preview_steps", ["1. Diagnóstico del Dolor", "2. Quiebre Tecnológico", "3. Demostración Empírica"])
                for st in steps:
                    rp = rtf.add_paragraph()
                    rp.text = f"• {st}"
                    rp.font.name = "Calibri"
                    rp.font.size = Pt(14)
                    rp.font.color.rgb = COLOR_TEXT_LIGHT_SUB

        # -------------------------------------------------------------
        # 3. DIAGRAMA DE FLUJO / PIPELINE / ROADMAP (FLOW_PIPELINE)
        # -------------------------------------------------------------
        elif stype in ["flow_pipeline", "pipeline", "roadmap"]:
            # Header
            cat_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.056), int(content_w * 0.5), 292608)
            p_cat = cat_box.text_frame.paragraphs[0]
            p_cat.text = sdata.get("category", "EL CAMINO DE LA SOLUCIÓN")
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_ACCENT_TERRA

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.10), content_w, int(slide_h * 0.12))
            tf = tbox.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            p_t.text = sdata.get("title", "Flujo Secuencial de Operación")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(25 if aspect_key != "9:16" else 20)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_HERO

            # 4 o 3 pasos en horizontal conectados con flechas
            steps = sdata.get("steps", sdata.get("points", ["Paso 1: Entrada", "Paso 2: Procesamiento", "Paso 3: Validación", "Paso 4: Impacto"]))
            n_steps = min(len(steps), 4)
            step_w = int((content_w - (n_steps - 1) * int(slide_w * 0.025)) / n_steps)
            step_h = int(slide_h * 0.52)
            step_y = int(slide_h * 0.26)

            for s_i in range(n_steps):
                sx = margin_x + s_i * (step_w + int(slide_w * 0.025))
                scard = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, step_y, step_w, step_h)
                scard.fill.solid()
                scard.fill.fore_color.rgb = COLOR_CARD_BG
                scard.line.color.rgb = COLOR_ACCENT_TERRA if s_i == 0 else COLOR_CARD_BORDER
                scard.line.width = Pt(1.5 if s_i == 0 else 1)

                stf = scard.text_frame
                stf.word_wrap = True
                sp1 = stf.paragraphs[0]
                sp1.text = f"PASO 0{s_i+1}"
                sp1.font.name = "Calibri"
                sp1.font.size = Pt(11)
                sp1.font.bold = True
                sp1.font.color.rgb = COLOR_ACCENT_TERRA

                step_data = steps[s_i]
                if isinstance(step_data, dict):
                    stitle = step_data.get("title", f"Fase {s_i+1}")
                    sdesc = step_data.get("desc", "")
                else:
                    parts = str(step_data).split(":", 1)
                    stitle = parts[0]
                    sdesc = parts[1].strip() if len(parts) > 1 else ""

                sp2 = stf.add_paragraph()
                sp2.text = stitle
                sp2.font.name = "Calibri"
                sp2.font.size = Pt(15)
                sp2.font.bold = True
                sp2.font.color.rgb = COLOR_TEXT_HERO

                sp3 = stf.add_paragraph()
                sp3.text = sdesc
                sp3.font.name = "Calibri"
                sp3.font.size = Pt(12)
                sp3.font.color.rgb = COLOR_TEXT_BODY

                # Flecha conectora entre pasos (excepto el último)
                if s_i < n_steps - 1 and aspect_key != "9:16":
                    arr_x = sx + step_w + int(slide_w * 0.005)
                    arr_box = slide.shapes.add_textbox(arr_x, step_y + int(step_h/2) - 150000, int(slide_w * 0.02), 300000)
                    atf = arr_box.text_frame
                    atf.margin_left = atf.margin_top = atf.margin_right = atf.margin_bottom = 0
                    ap = atf.paragraphs[0]
                    ap.text = "➔"
                    ap.font.name = "Calibri"
                    ap.font.size = Pt(16)
                    ap.font.bold = True
                    ap.font.color.rgb = COLOR_ACCENT_AMBER

        # -------------------------------------------------------------
        # 4. TARJETAS DE MÉTRICAS Y KPIS GIGANTES (METRIC_KPIS)
        # -------------------------------------------------------------
        elif stype in ["metric_kpis", "metrics", "kpis"]:
            cat_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.056), int(content_w * 0.5), 292608)
            p_cat = cat_box.text_frame.paragraphs[0]
            p_cat.text = sdata.get("category", "VALIDACIÓN Y TRACCIÓN EMPÍRICA")
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_ACCENT_TERRA

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.10), content_w, int(slide_h * 0.12))
            tf = tbox.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            p_t.text = sdata.get("title", "Resultados Medibles que Respaldan la Solución")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(25 if aspect_key != "9:16" else 20)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_HERO

            kpis = sdata.get("kpis", [
                {"number": "94.2%", "label": "Precisión del Modelo", "desc": "Validado en entorno de pruebas con datos regionales."},
                {"number": "<1.2s", "label": "Tiempo de Respuesta", "desc": "Velocidad de procesamiento de consultas en WhatsApp."},
                {"number": "400+", "label": "Usuarios / Familias", "desc": "Impacto proyectado en la primera fase del piloto."}
            ])
            n_kpis = min(len(kpis), 3)
            kw = int((content_w - (n_kpis - 1) * int(slide_w * 0.03)) / n_kpis)
            kh = int(slide_h * 0.54)
            ky = int(slide_h * 0.25)

            for ki in range(n_kpis):
                kx = margin_x + ki * (kw + int(slide_w * 0.03))
                kcard = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, kx, ky, kw, kh)
                kcard.fill.solid()
                kcard.fill.fore_color.rgb = COLOR_CARD_BG
                kcard.line.color.rgb = COLOR_CARD_BORDER
                kcard.line.width = Pt(1)

                ktf = kcard.text_frame
                ktf.word_wrap = True
                kp1 = ktf.paragraphs[0]
                kp1.text = kpis[ki].get("number", "100%")
                kp1.font.name = "Calibri"
                kp1.font.size = Pt(44)
                kp1.font.bold = True
                kp1.font.color.rgb = COLOR_ACCENT_TERRA if ki % 2 == 0 else COLOR_ACCENT_AMBER

                kp2 = ktf.add_paragraph()
                kp2.text = kpis[ki].get("label", "Métrica Clave")
                kp2.font.name = "Calibri"
                kp2.font.size = Pt(15)
                kp2.font.bold = True
                kp2.font.color.rgb = COLOR_TEXT_HERO

                kp3 = ktf.add_paragraph()
                kp3.text = kpis[ki].get("desc", "")
                kp3.font.name = "Calibri"
                kp3.font.size = Pt(12)
                kp3.font.color.rgb = COLOR_TEXT_BODY

        # -------------------------------------------------------------
        # 5. VIDEO CON FLUJO EXPLICATIVO AL COSTADO (VIDEO_WITH_FLOW)
        # -------------------------------------------------------------
        elif stype in ["video_slide", "video_with_flow", "video"]:
            cat_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.056), int(content_w * 0.5), 292608)
            p_cat = cat_box.text_frame.paragraphs[0]
            p_cat.text = sdata.get("category", "DEMOSTRACIÓN EN VIDEO & FLUJO EN VIVO")
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_ACCENT_TERRA

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.10), content_w, int(slide_h * 0.10))
            tf = tbox.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            p_t.text = sdata.get("title", "Demostración de Producto en Acción")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(25 if aspect_key != "9:16" else 20)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_HERO

            # Layout 2 Columnas: Izquierda Video (58%), Derecha Flujo de Pasos (38%)
            if aspect_key != "9:16":
                vw = int(content_w * 0.58)
                vh = int(slide_h * 0.62)
                vx = margin_x
                vy = int(slide_h * 0.22)

                # Contenedor de Video
                vcard = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vx, vy, vw, vh)
                vcard.fill.solid()
                vcard.fill.fore_color.rgb = COLOR_BG_DARK
                vcard.line.color.rgb = COLOR_ACCENT_TERRA
                vcard.line.width = Pt(2)

                vtext = slide.shapes.add_textbox(vx, vy + int(vh * 0.35), vw, int(vh * 0.3))
                tf_v = vtext.text_frame
                p_v = tf_v.paragraphs[0]
                p_v.alignment = PP_ALIGN.CENTER
                video_name = sdata.get("video_filename", "demo.mp4")
                p_v.text = f"▶  [VIDEO: videos/{video_name}]"
                p_v.font.name = "Calibri"
                p_v.font.size = Pt(18)
                p_v.font.bold = True
                p_v.font.color.rgb = COLOR_TEXT_LIGHT

                p_v2 = tf_v.add_paragraph()
                p_v2.alignment = PP_ALIGN.CENTER
                p_v2.text = "Incruste el video desde la carpeta 'videos/' (Insertar > Multimedia > Video)"
                p_v2.font.name = "Calibri"
                p_v2.font.size = Pt(11)
                p_v2.font.color.rgb = COLOR_TEXT_LIGHT_SUB

                # Columna Derecha: Flujo de 3 pasos que explica el video
                fx = margin_x + vw + int(slide_w * 0.03)
                fw = content_w - vw - int(slide_w * 0.03)
                flow_steps = sdata.get("flow_steps", [
                    {"step": "1. Entrada", "desc": "El usuario envía su consulta por WhatsApp o Web."},
                    {"step": "2. Procesamiento", "desc": "El agente analiza la intención y ejecuta herramientas."},
                    {"step": "3. Respuesta", "desc": "Entrega una respuesta fundamentada en <1.2s."}
                ])

                f_card_h = int((vh - (len(flow_steps) - 1) * int(slide_h * 0.02)) / len(flow_steps))
                for f_idx, f_step in enumerate(flow_steps):
                    fy = vy + f_idx * (f_card_h + int(slide_h * 0.02))
                    f_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fx, fy, fw, f_card_h)
                    f_card.fill.solid()
                    f_card.fill.fore_color.rgb = COLOR_CARD_BG
                    f_card.line.color.rgb = COLOR_CARD_BORDER
                    f_card.line.width = Pt(1)

                    ftf = f_card.text_frame
                    ftf.word_wrap = True
                    fp1 = ftf.paragraphs[0]
                    fp1.text = f_step.get("step", f"Paso {f_idx+1}")
                    fp1.font.name = "Calibri"
                    fp1.font.size = Pt(13)
                    fp1.font.bold = True
                    fp1.font.color.rgb = COLOR_ACCENT_TERRA

                    fp2 = ftf.add_paragraph()
                    fp2.text = f_step.get("desc", "")
                    fp2.font.name = "Calibri"
                    fp2.font.size = Pt(11)
                    fp2.font.color.rgb = COLOR_TEXT_BODY
            else:
                # Vertical layout for mobile
                vw = content_w
                vh = int(slide_h * 0.45)
                vx = margin_x
                vy = int(slide_h * 0.22)
                vcard = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, vx, vy, vw, vh)
                vcard.fill.solid()
                vcard.fill.fore_color.rgb = COLOR_BG_DARK
                vcard.line.color.rgb = COLOR_ACCENT_TERRA
                vcard.line.width = Pt(2)

        # -------------------------------------------------------------
        # 6. COMPARATIVA O ARQUITECTURA (SPLIT_COMPARISON)
        # -------------------------------------------------------------
        elif stype in ["split_comparison", "comparison", "two_col"]:
            cat_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.056), int(content_w * 0.5), 292608)
            p_cat = cat_box.text_frame.paragraphs[0]
            p_cat.text = sdata.get("category", "COMPARATIVA DE VALOR")
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_TEXT_MUTED

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.10), content_w, int(slide_h * 0.12))
            tf = tbox.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            p_t.text = sdata.get("title", "El Problema Actual vs. Nuestra Solución")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(25 if aspect_key != "9:16" else 20)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_HERO

            col_w = int((content_w - int(slide_w * 0.03)) / 2)
            col_h = int(slide_h * 0.56)
            col_y = int(slide_h * 0.24)

            # Columna Izquierda: Dolor / Problema actual
            left_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, margin_x, col_y, col_w, col_h)
            left_card.fill.solid()
            left_card.fill.fore_color.rgb = RGBColor(0xFA, 0xF5, 0xF5) # sutil tinte
            left_card.line.color.rgb = RGBColor(0xEA, 0xD4, 0xD4)
            ltf = left_card.text_frame
            ltf.word_wrap = True
            lp1 = ltf.paragraphs[0]
            lp1.text = sdata.get("left_title", "❌ SITUACIÓN ACTUAL")
            lp1.font.name = "Calibri"
            lp1.font.size = Pt(13)
            lp1.font.bold = True
            lp1.font.color.rgb = RGBColor(0xDC, 0x26, 0x26)

            left_points = sdata.get("left_points", ["Procesos manuales propensos a error.", "Tiempos de espera de hasta 48 horas.", "Cero visibilidad de datos para decisiones."])
            for lp in left_points:
                p = ltf.add_paragraph()
                p.text = f"• {lp}"
                p.font.name = "Calibri"
                p.font.size = Pt(13)
                p.font.color.rgb = COLOR_TEXT_BODY

            # Columna Derecha: Nuestra solución
            rx = margin_x + col_w + int(slide_w * 0.03)
            right_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, col_y, col_w, col_h)
            right_card.fill.solid()
            right_card.fill.fore_color.rgb = COLOR_CARD_BG
            right_card.line.color.rgb = COLOR_ACCENT_TERRA
            right_card.line.width = Pt(1.5)
            rtf = right_card.text_frame
            rtf.word_wrap = True
            rp1 = rtf.paragraphs[0]
            rp1.text = sdata.get("right_title", "✅ NUESTRA PROPUESTA")
            rp1.font.name = "Calibri"
            rp1.font.size = Pt(13)
            rp1.font.bold = True
            rp1.font.color.rgb = COLOR_ACCENT_TERRA

            right_points = sdata.get("right_points", ["Automatización total con IA conversacional.", "Respuestas inmediatas en segundos.", "Métricas y trazabilidad en tiempo real."])
            for rp in right_points:
                p = rtf.add_paragraph()
                p.text = f"• {rp}"
                p.font.name = "Calibri"
                p.font.size = Pt(13)
                p.font.color.rgb = COLOR_TEXT_HERO

        # -------------------------------------------------------------
        # 7. CONTENIDO ESTÁNDAR LIMPIO (CONTENT_LIGHT / TARJETAS DINÁMICAS)
        # -------------------------------------------------------------
        elif stype == "content_light":
            cat_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.056), int(content_w * 0.5), 292608)
            p_cat = cat_box.text_frame.paragraphs[0]
            p_cat.text = sdata.get("category", "SISTEMA")
            p_cat.font.name = "Calibri"
            p_cat.font.size = Pt(12)
            p_cat.font.bold = True
            p_cat.font.color.rgb = COLOR_TEXT_MUTED

            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.10), content_w, int(slide_h * 0.12))
            tf = tbox.text_frame
            tf.word_wrap = True
            p_t = tf.paragraphs[0]
            p_t.text = sdata.get("title", "")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(25 if aspect_key != "9:16" else 20)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_HERO

            points = sdata.get("points", [])
            n_pts = min(len(points), 3)
            card_top = int(slide_h * 0.25)
            card_h = int(slide_h * 0.16)
            gap_c = int(slide_h * 0.03)

            for p_idx, pt_text in enumerate(points[:n_pts]):
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
                p_c.font.size = Pt(15 if aspect_key != "9:16" else 13)
                p_c.font.color.rgb = COLOR_TEXT_BODY

        # -------------------------------------------------------------
        # 8. CIERRE Y QR (CLOSING_QR_DARK)
        # -------------------------------------------------------------
        elif stype == "closing_qr_dark":
            tbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.25), int(content_w * 0.55), int(slide_h * 0.16))
            p_t = tbox.text_frame.paragraphs[0]
            p_t.text = sdata.get("title", "¡Muchas Gracias!")
            p_t.font.name = "Calibri"
            p_t.font.size = Pt(40 if aspect_key != "9:16" else 28)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_TEXT_LIGHT

            sub_box = slide.shapes.add_textbox(margin_x, int(slide_h * 0.43), int(content_w * 0.55), int(slide_h * 0.15))
            tf_s = sub_box.text_frame
            tf_s.word_wrap = True
            p_s = tf_s.paragraphs[0]
            p_s.text = sdata.get("subtitle", "Conversemos sobre innovación, pilotos y desarrollo.")
            p_s.font.name = "Calibri"
            p_s.font.size = Pt(16 if aspect_key != "9:16" else 13)
            p_s.font.color.rgb = COLOR_TEXT_LIGHT_SUB

            cbox = slide.shapes.add_textbox(margin_x, int(slide_h * 0.62), int(content_w * 0.55), int(slide_h * 0.25))
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

            qr_cfg = settings.get("qr_config", {})
            if qr_cfg.get("enabled", True):
                os.makedirs("temp_qr", exist_ok=True)
                primary = qr_cfg.get("primary", {})
                qr_content = primary.get("payload") or primary.get("url") or "https://tu-proyecto.pe"
                qr_img = generate_qr_image(qr_content, "temp_qr/qr_primary.png")

                qr_card_w = int(slide_w * 0.20) if aspect_key != "9:16" else int(slide_w * 0.35)
                qr_card_x = int(slide_w * 0.64) if aspect_key != "9:16" else int(slide_w * 0.55)
                qr_card_y = int(slide_h * 0.25)

                card1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qr_card_x, qr_card_y, qr_card_w, qr_card_w)
                card1.fill.solid()
                card1.fill.fore_color.rgb = COLOR_CARD_BG
                card1.line.fill.background()

                if qr_img and os.path.exists(qr_img):
                    pad = int(qr_card_w * 0.06)
                    slide.shapes.add_picture(qr_img, qr_card_x + pad, qr_card_y + pad, qr_card_w - 2*pad, qr_card_w - 2*pad)

                label_box = slide.shapes.add_textbox(qr_card_x, qr_card_y + qr_card_w + 80000, qr_card_w, 640080)
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

        # -------------------------------------------------------------
        # BARRA DE PROGRESO INFERIOR DINÁMICA
        # -------------------------------------------------------------
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
