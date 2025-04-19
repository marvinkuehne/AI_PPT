# gpt_service.py

import os
import base64
import re
import openai
from dotenv import load_dotenv

# Environment-Variablen laden
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
# Dein Modell-Name – hier als Fallback, lässt sich aber auch per ENV überschreiben
MODEL = os.getenv("OPENAI_MODEL", "o4-mini-2025-04-16")

openai.api_key = OPENAI_KEY

def run_gpt_and_build_vb(image_path):
    """
    Ruft die Analyse-Routine auf und gibt reinen VBA-Code zurück.
    """
    return analyze_with_openai_vb(image_path)


def analyze_with_openai_vb(image_path):
    """
    Fordert von OpenAI validen VBA-Code an, der in PowerPoint
    ohne Compile-Error ausgeführt werden kann.
    """
    # Bild als Base64 für Prompt
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")

    system_prompt = (
        "You are a PowerPoint VBA generator specialized in clean, consulting‑grade slides (think McKinsey). "
        "Whenever I provide a slide image, you must:\n"
        "  • Reconstruct **exactly** every drawn element (shapes, lines, curves, text, icons) with fixed coordinates, matching fill‑colors, line‑colors, line‑weights, arrowheads and fonts.\n"
        "  • Then apply a consistent, professional consulting style:\n"
        "      – Use **Calibri** font for all text (titles 28pt bold, body text 16pt regular).\n"
        "      – Apply a two‑tone gray bucket background for each row or section (alternating RGB(245,245,245) and RGB(230,230,230)).\n"
        "      – Use a single accent color for key shapes and numbers (e.g. RGB(0,70,127)), and neutral dark gray for text (RGB(60,60,60)).\n"
        "      – All shapes get subtle rounded corners (radius 6) and a light drop shadow (OffsetX=2, OffsetY=2, Transparency=0.4).\n"
        "      – Lines/arrows: weight 1pt, accent color for arrows, neutral gray for connectors.\n"
        "  • Group composite elements (braces, multi‑part icons, house) and label each bucket clearly on the right side with a big circle and number in accent color.\n"
        "  • Ignore built‑in placeholders (\"Click to add subtitle\"); only draw what’s actually in the sketch.\n"
        "Generate exactly one `Sub CreatePresentation()`…`End Sub`, using only:\n"
        "  - PowerPoint.Application, Presentations.Add, Slides.Add\n"
        "  - Shapes.AddShape, Shapes.AddLine, Shapes.AddCurve/BuildFreeform, Shapes.AddTextbox, Range().Group\n"
        "  - For every shape/text: set `.Fill.ForeColor.RGB`, `.Line.ForeColor.RGB`, `.Line.Weight`, `.TextFrame.TextRange.Font.*` as needed\n"
        "Output **only** the VBA code in a ```vb\n…``` block—no comments or extra text."

    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [
            {"type": "text", "text": "Please reconstruct this slide from the image below:"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
        ]}
    ]

    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,

        max_completion_tokens=5000
    )

    raw = response.choices[0].message.content
    return extract_vb_code(raw)


def extract_vb_code(raw_code):
    """
    Extrahiert den reinen VBA-Code aus dem ```vb ... ``` Block.
    """
    match = re.search(r'```vb\n(.*?)```', raw_code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_code.strip()
