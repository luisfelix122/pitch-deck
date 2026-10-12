# Pitch-Deck Skill

**Pitch-Deck** is an all-in-one AI agent skill that unifies pitch script crafting with PowerPoint presentation generation. 

It conducts an interactive interview, strictly calibrates speech duration and wpm, profiles authentic communication styles, incorporates jury evaluation rubrics, and compiles a matching PPTX presentation (supporting 16:9, 4:3, 9:16 mobile, and tablet ratios) featuring dynamic walking avatars, UNP/FII logos, customizable QR codes, and video containers.

## Deliverables Produced
1. **Verbatim Speech Script**: Calibrated to exact minutes ($T \times 130\text{--}140$ words), with stage directions and `[SLIDE X]` sync triggers.
2. **Interactive Rehearsal Tool (`.html`)**: Real-time timer, 4-6-8 breathing metronome, and jury rubric.
3. **PowerPoint Presentation (`.pptx`)**: Obsidian Dark & Warm Cream contrast, walking mascot progress bar, transparent institutional logos, dynamic QR, and video slides.

## Usage
```bash
python scripts/build_full_pitch.py --config assets/templates/full_pitch_schema.json --out-pptx deck.pptx --out-html rehearsal.html --assets assets
```
