#!/usr/bin/env python3
"""
Pitch Calibrator - Pitch-Pro Skill
Analiza guiones de pitch con tiempo dinámico (1 min, 2 min, 3 min, 5 min, etc.),
midiendo palabras, velocidad (wpm), balance de actos, presencia del Puente e indicaciones escénicas.
"""

import sys
import re
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TARGET_WPM_MIN = 130
TARGET_WPM_MAX = 140

FORBIDDEN_OPENINGS = [
    r"\b(perd[oó]n|disculp\w+)\b",
    r"\b(buenos d[ií]as distinguido jurado|buenas tardes miembros del jurado)\b",
    r"\b(no hemos preparado mucho|disculpen la demora|disculpen si me equivoco)\b",
    r"\b(les voy a contar un chiste|para romper el hielo)\b"
]

def clean_speech_text(text: str) -> str:
    """Elimina etiquetas de indicaciones escénicas [...] o (...) para contar solo palabras habladas."""
    cleaned = re.sub(r"\[.*?\]", " ", text)
    cleaned = re.sub(r"\(.*?\)", " ", text)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned) # Quitar HTML si lo hay
    cleaned = re.sub(r"#+.*", " ", cleaned)    # Quitar cabeceras markdown
    return cleaned.strip()

def analyze_pitch(content: str, total_minutes: float = 3.0):
    speech = clean_speech_text(content)
    words = [w for w in re.split(r"\s+", speech) if w and any(c.isalnum() for c in w)]
    word_count = len(words)
    wpm = word_count / total_minutes

    target_min_words = int(total_minutes * TARGET_WPM_MIN)
    target_max_words = int(total_minutes * TARGET_WPM_MAX)

    total_secs = int(total_minutes * 60)
    mins = total_secs // 60
    secs = total_secs % 60
    time_str = f"{mins}:{secs:02d}"

    print("=" * 65)
    print(f"      INFORME DE CALIBRACIÓN DE PITCH ({time_str} MINUTOS)")
    print("=" * 65)
    print(f"Tiempo total asignado:       {time_str} ({total_minutes:.2f} min)")
    print(f"Total de palabras habladas:  {word_count} palabras")
    print(f"Rango objetivo calibrado:    {target_min_words} a {target_max_words} palabras")
    print(f"Velocidad de habla estimada: {wpm:.1f} palabras por minuto (wpm)")
    print(f"Rango óptimo wpm:            {TARGET_WPM_MIN} a {TARGET_WPM_MAX} wpm")
    print("-" * 65)

    # Evaluación de Presupuesto de Palabras
    if word_count < target_min_words:
        diff = target_min_words - word_count
        print(f"⚠️  ALERTA: Faltan {diff} palabras para aprovechar el tiempo completo.")
        print(f"   Riesgo: Dejar tiempo muerto al final o hablar por debajo de {TARGET_WPM_MIN} wpm.")
    elif word_count > target_max_words:
        diff = word_count - target_max_words
        print(f"🚨 ALERTA: Sobran {diff} palabras. El orador corre riesgo de atropellarse (>{TARGET_WPM_MAX} wpm)")
        print("   o ser cortado por el cronómetro del jurado.")
    else:
        print(f"✅ PRESUPUESTO PERFECTO: Calibrado para exactamente {time_str} a ritmo profesional.")

    # Detección de Inicios Prohibidos
    first_paragraph = content.strip().split("\n\n")[0].lower() if content.strip() else ""
    violations = []
    for pattern in FORBIDDEN_OPENINGS:
        if re.search(pattern, first_paragraph, re.IGNORECASE):
            violations.append(pattern)
    
    if violations:
        print("\n❌ INICIOS QUE DEBILITAN AUTORIDAD:")
        print("   Se detectaron disculpas, saludos burocráticos o chiste forzado en el inicio.")
        print("   RECOMENDACIÓN: Entra directo con una de las 6 aperturas de alto impacto.")
    else:
        print("\n✅ APERTURA LIMPIA: Sin saludos burocráticos ni disculpas.")

    # Detección de Indicaciones Escénicas
    stage_dirs = re.findall(r"\[(.*?)\]", content)
    tone_dirs = [d for d in stage_dirs if any(k in d.lower() for k in ["tono", "intenci", "emoci"])]
    gaze_dirs = [d for d in stage_dirs if any(k in d.lower() for k in ["mirada", "ojos", "contacto"])]
    hands_dirs = [d for d in stage_dirs if any(k in d.lower() for k in ["mano", "gesto", "brazo"])]
    pause_dirs = [d for d in stage_dirs if any(k in d.lower() for k in ["pausa", "silencio", "respira"])]
    slide_cues = [d for d in stage_dirs if any(k in d.lower() for k in ["slide", "diapositiva", "l[aá]mina"])]

    print("-" * 65)
    print("INDICACIONES ESCÉNICAS Y SINCRONIZACIÓN:")
    print(f"  • Total acotaciones:   {len(stage_dirs)}")
    print(f"  • Modulación de tono:  {len(tone_dirs)}")
    print(f"  • Contacto visual:     {len(gaze_dirs)}")
    print(f"  • Gestos y manos:      {len(hands_dirs)}")
    print(f"  • Pausas y silencios:  {len(pause_dirs)}")
    print(f"  • Cues de diapositiva: {len(slide_cues)} (Sincronización con slides)")

    if len(stage_dirs) < 4:
        print("⚠️  SUGERENCIA: Agrega más indicaciones escénicas [Tono], [Mirada], [Manos], [Pausa]")
    else:
        print("✅ DOMINIO ESCÉNICO: Indicaciones físicas bien estructuradas.")

    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calibrador dinámico de pitch")
    parser.add_argument("file", help="Ruta al archivo del pitch (.txt o .md)")
    parser.add_argument("--time", "-t", type=float, default=3.0, help="Tiempo asignado en minutos (ej. 1, 2, 3, 5)")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        analyze_pitch(f.read(), total_minutes=args.time)
