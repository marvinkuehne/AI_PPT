# gpt_service.py

import os
import base64
import re
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"  # Deinen OpenAI-Modelnamen hier einstellen

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

    prompt = (
        "You are a PowerPoint VBA generator. Your task is to reconstruct the provided slide image "
        "as valid VBA code. Generate exactly one Sub named CreatePresentation(), closed by End Sub, that:\n"
        " 1. Starts PowerPoint (CreateObject(\"PowerPoint.Application\")), makes it visible,\n"
        " 2. Adds a new Presentation and a title slide (ppLayoutTitle), sets the title text,\n"
        " 3. Inserts all shapes and lines using only:\n"
        "    - Set shp = slide.Shapes.AddShape(Type, Left, Top, Width, Height)\n"
        "    - Set shp = slide.Shapes.AddLine(BeginX, BeginY, EndX, EndY)\n"
        "    - Set shp = slide.Shapes.AddTextbox(Orientation, Left, Top, Width, Height)\n"
        "   Never call these methods without `Set` or `Call`.\n"
        " 4. For arrowheads use `shp.Line.EndArrowheadStyle = msoArrowheadTriangle`.\n"
        " 5. Set text via `shp.TextFrame.TextRange.Text = ...`.\n"
        " 6. Use only Microsoft methods (PowerPoint.Application, Presentations.Add, Slides.Add, Shapes.AddShape, Shapes.AddLine, Shapes.AddTextbox).\n"
        " 7. Use fixed point coordinates; do not use freeform shapes.\n"
        "Output only the VBA code in a ```vb ... ``` block without any extra explanation."
    )
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please reconstruct this slide from the image below:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
                ]
            }
        ],
        temperature=0.0,
        max_tokens= 5000
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