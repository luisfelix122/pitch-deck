#!/usr/bin/env python3
"""
Pitch-Deck Master Orchestrator
Compila la presentación en PowerPoint (.pptx) y el entregable interactivo HTML de ensayo
(con visor de diapositivas y guion sincrónico al costado, botón de agrandar, tiempo, tono y acotaciones).
"""

import os
import sys
import json
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from generate_deck import build_presentation
from calibrate_pitch import analyze_pitch

def generate_html_deliverable(data: dict, template_path: str, output_path: str, assets_dir: str):
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    meta = data.get("meta", {})
    settings = data.get("settings", {})
    slides = data.get("slides", [])
    time_min = float(meta.get("allocated_time_minutes", 3.0))
    time_sec = int(time_min * 60)
    pres_mode = settings.get("presentation_mode", "Presencial").capitalize()
    aspect = settings.get("aspect_ratio", "16:9")

    aspect_css = "16 / 9"
    if aspect in ["4:3", "desktop", "escritorio"]:
        aspect_css = "4 / 3"
    elif aspect in ["9:16", "mobile", "celular"]:
        aspect_css = "9 / 16"
    elif aspect in ["tablet", "ipad", "3:2"]:
        aspect_css = "3 / 2"

    gaze_default = "Clavar mirada en el lente de la cámara (no en la pantalla)" if pres_mode == "Virtual" else "Contacto visual directo con el jurado"

    html = html.replace("{{PITCH_TITLE}}", meta.get("title", "Pitch de Alto Impacto"))
    html = html.replace("{{PITCH_DURATION_LABEL}}", f"{time_min:.1f} MIN ({time_sec}s)")
    html = html.replace("{{PITCH_DURATION_SECONDS}}", str(time_sec))
    html = html.replace("{{PRESENTATION_MODE}}", pres_mode)
    html = html.replace("{{ASPECT_RATIO}}", str(aspect).upper())
    html = html.replace("{{ASPECT_RATIO_CSS}}", aspect_css)
    html = html.replace("{{PRIMARY_COLOR}}", "#C94B22")
    html = html.replace("{{GAZE_MODE_DEFAULT}}", gaze_default)

    # Avatar path (relativo al HTML o data URI si es local)
    avatar_path = settings.get("custom_avatar_path")
    if not avatar_path or not os.path.exists(avatar_path):
        avatar_path = os.path.join(assets_dir, "logos", "runner_indicator.png")
    # Convertir a ruta relativa limpia
    rel_avatar = os.path.relpath(avatar_path, os.path.dirname(output_path) if os.path.dirname(output_path) else ".").replace("\\", "/")
    html = html.replace("{{AVATAR_PATH}}", rel_avatar)

    # Logos HTML
    logos_html = []
    if settings.get("include_unp_logo", True):
        unp_p = os.path.join(assets_dir, "logos", "unp_logo_transparent.png")
        if os.path.exists(unp_p):
            r_unp = os.path.relpath(unp_p, os.path.dirname(output_path) if os.path.dirname(output_path) else ".").replace("\\", "/")
            logos_html.append(f'<img src="{r_unp}" class="slide-logo-img" alt="UNP">')
    if settings.get("include_fii_logo", True):
        fii_p = os.path.join(assets_dir, "logos", "fii_logo_transparent.png")
        if os.path.exists(fii_p):
            r_fii = os.path.relpath(fii_p, os.path.dirname(output_path) if os.path.dirname(output_path) else ".").replace("\\", "/")
            logos_html.append(f'<img src="{r_fii}" class="slide-logo-img" alt="FII">')
    html = html.replace("{{LOGOS_HTML}}", " ".join(logos_html))

    # Preparar JSON de slides para inyección directa
    slides_client_data = []
    for s_idx, s in enumerate(slides):
        stype = s.get("type", "content_light")
        theme = "dark" if "dark" in stype else "light"
        slides_client_data.append({
            "idx": s_idx,
            "type": stype,
            "theme": theme,
            "category": s.get("category", s.get("act_number", "SECCIÓN")),
            "title": s.get("title", ""),
            "subtitle": s.get("subtitle", s.get("description", "")),
            "points": s.get("points", []),
            "speech": s.get("speech", s.get("script", "Expón el contenido de esta diapositiva conectando con la audiencia.")),
            "bridge": s.get("bridge", None),
            "target_time": s.get("target_time", f"~{int(time_sec / max(len(slides), 1))}s"),
            "tone": s.get("tone", "Certeza absoluta y calidez"),
            "gaze": s.get("gaze", gaze_default),
            "hands": s.get("hands", "Manos visibles en caja escénica"),
            "pause": s.get("pause", "Pausa de 1 segundo tras el dato principal")
        })

    html = html.replace("{{SLIDES_JSON_DATA}}", json.dumps(slides_client_data, ensure_ascii=False, indent=2))

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Entregable HTML interactivo de ensayo generado: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Compilador integral de Pitch y Diapositivas")
    parser.add_argument("--config", "-c", required=True, help="Ruta al JSON unificado")
    parser.add_argument("--out-pptx", default="presentacion.pptx", help="Ruta de salida del archivo PPTX")
    parser.add_argument("--out-html", default="pitch_ensayo.html", help="Ruta de salida del archivo HTML")
    parser.add_argument("--assets", "-a", default="assets", help="Directorio de assets")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Generar Presentación PPTX
    build_presentation(data, args.out_pptx, args.assets)

    # 2. Generar Entregable HTML con cronómetro, vista dividida y diapos agrandables
    tpl_path = os.path.join(args.assets, "template-pitch-pro.html")
    if os.path.exists(tpl_path):
        generate_html_deliverable(data, tpl_path, args.out_html, args.assets)

    # 3. Calibrar Guion
    slides = data.get("slides", [])
    full_speech = "\n\n".join([s.get("speech", "") for s in slides if s.get("speech")])
    time_min = float(data.get("meta", {}).get("allocated_time_minutes", 3.0))
    if full_speech.strip():
        print("\nCalibración del discurso:")
        analyze_pitch(full_speech, total_minutes=time_min)

if __name__ == "__main__":
    main()
