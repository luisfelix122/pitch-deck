#!/usr/bin/env python3
"""
Pitch-Deck Video Tools
Maneja recorte, ajuste de velocidad, conversión y generación de videos para presentaciones,
alineando la duración exacta del clip con el tiempo asignado en el pitch.
Integra comandos de FFmpeg y flujos de HeyGen HyperFrames.
"""

import os
import sys
import subprocess
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def trim_and_retime_video(input_path: str, output_path: str, start_sec: float = 0, end_sec: float = None, target_duration: float = None):
    """
    Recorta un video y ajusta su velocidad para que dure exactamente target_duration segundos.
    """
    if not os.path.exists(input_path):
        print(f"Error: No se encontró el video de entrada: {input_path}")
        return False

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    # 1. Obtener duración del video de entrada
    duration_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_path
    ]
    try:
        res = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
        orig_duration = float(res.stdout.strip())
    except Exception:
        orig_duration = 30.0 # fallback

    clip_start = max(0, start_sec)
    clip_end = min(orig_duration, end_sec) if end_sec else orig_duration
    clip_duration = clip_end - clip_start

    # Si se especificó target_duration, calcular factor de velocidad (speed factor)
    if target_duration and target_duration > 0 and clip_duration > 0:
        speed_factor = clip_duration / target_duration
        # ffmpeg setpts: PTS=PTS/speed_factor, atempo=speed_factor
        # Limitar atempo entre 0.5 y 2.0 (o encadenar si es mayor)
        video_filter = f"setpts=PTS/{speed_factor}"
        if 0.5 <= speed_factor <= 2.0:
            audio_filter = f"atempo={speed_factor}"
        else:
            audio_filter = "anull" # si es extremo, anular o no filtrar audio
        
        cmd = [
            "ffmpeg", "-y", "-ss", str(clip_start), "-to", str(clip_end),
            "-i", input_path,
            "-filter:v", video_filter,
            "-filter:a", audio_filter,
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_path
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-ss", str(clip_start),
            *(["-to", str(clip_end)] if end_sec else []),
            "-i", input_path,
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_path
        ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Video procesado exitosamente: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error procesando video con FFmpeg: {e.stderr.decode('utf-8', errors='ignore')}")
        return False

def generate_placeholder_video(output_path: str, title: str = "DEMO DEL PRODUCTO", duration_sec: int = 15):
    """
    Genera un video MP4 animado de demostración con FFmpeg si el usuario aún no tiene video grabado.
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    clean_title = title.replace("'", "").replace(":", " -")
    # Genera un fondo animado con contador de tiempo y título
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=0x1A1613:s=1280x720:d={duration_sec}",
        "-vf", f"drawtext=text='{clean_title}':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-50,"
               f"drawtext=text='Demostración en vivo sincronizada con el pitch':fontsize=24:fontcolor=0xEA9B27:x=(w-text_w)/2:y=(h-text_h)/2+20,"
               f"drawtext=text='Tiempo %{{pts\\:hms}}':fontsize=20:fontcolor=0xA8A29E:x=(w-text_w)/2:y=(h-text_h)/2+80",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Video de demostración generado: {output_path} ({duration_sec}s)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Aviso: no se pudo generar video sintético ({e})")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pitch-Deck Video Processor")
    parser.add_argument("--input", "-i", help="Video original a recortar")
    parser.add_argument("--output", "-o", default="videos/demo_pitch.mp4", help="Video de salida")
    parser.add_argument("--start", type=float, default=0, help="Segundo de inicio")
    parser.add_argument("--end", type=float, default=None, help="Segundo de fin")
    parser.add_argument("--target-duration", "-d", type=float, default=None, help="Duración deseada en segundos")
    parser.add_argument("--create-demo", action="store_true", help="Generar un video sintético de demo")
    parser.add_argument("--title", default="DEMO EN VIVO", help="Título para demo sintética")
    args = parser.parse_args()

    if args.create_demo or not args.input:
        generate_placeholder_video(args.output, title=args.title, duration_sec=int(args.target_duration or 15))
    else:
        trim_and_retime_video(args.input, args.output, start_sec=args.start, end_sec=args.end, target_duration=args.target_duration)
