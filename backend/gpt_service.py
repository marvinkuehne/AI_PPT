import os
import base64
import re
import openai
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Environment-Variablen laden
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
# Dein Modell-Name – hier als Fallback, lässt sich aber auch per ENV überschreiben
MODEL = os.getenv("OPENAI_MODEL", "o4-mini-2025-04-16")

openai.api_key = OPENAI_KEY


def run_gpt_and_build_vb(image_path):
    """
    Calls the analysis routine and returns raw VBA code.
    Retries once with an explicit retry prompt if the initial output is empty.
    """
    # First attempt
    vb_code = analyze_with_openai_vb(image_path)
    # Retry with clarification if empty
    if not vb_code.strip():
        vb_code = analyze_with_openai_vb(
            image_path,
            reminder="I didn't receive any VBA code. Please output only the VBA code in a single fenced block, without any extra text."
        )
    return vb_code


def analyze_with_openai_vb(image_path: str, reminder: str = None) -> str:
    """
    Requests valid VBA code from OpenAI that compiles in PowerPoint.
    Optionally includes a reminder message for retries.
    """
    # Read and encode the image for the prompt
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")

    system_prompt = (
        "You are a PowerPoint VBA generator specialized in clean, consulting‑grade slides (think McKinsey). "
        "Whenever I provide a slide image, you must:\n"
        "  • Reconstruct **exactly** every drawn element (shapes, lines, curves, text, icons) with fixed coordinates, matching fill‑colors, line‑colors, line‑weights, arrowheads and fonts.\n"
        "  • Then apply a consistent, professional consulting style:\n"
        "      – Use **Calibri** font …\n"
        "      – Apply a two-tone gray bucket background …\n"
        "      – Use a single accent color …\n"
        "      – All shapes get a light drop shadow (use msoShadowStyleOuterShadow for `.Shadow.Type`, with OffsetX=2, OffsetY=2, Transparency=0.4).\n"
        "      – For rounded rectangles, do **not** use `.RoundedCorners`. Instead:\n"
        "          1. Add with `msoShapeRoundedRectangle`\n"
        "          2. Set corner radius: `.Adjustments(1)=0.06`\n"
        "      – Lines/arrows: weight 1pt, accent color …\n"
        "  • Group composite elements (braces, multi‑part icons, house) and label each bucket clearly on the right side with a big circle and number in accent color.\n"
        "  • Ignore built‑in placeholders (\"Click to add subtitle\"); only draw what’s actually in the sketch.\n"
        "Generate exactly one `Sub CreatePresentation()`…`End Sub`, using only:\n"
        "  - PowerPoint.Application, Presentations.Add, Slides.Add\n"
        "  - Shapes.AddShape, Shapes.AddLine, Shapes.AddCurve, Shapes.AddTextbox, Range().Group (use a Variant array of point Arrays for AddCurve)"
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

    # If this is a retry, append a clarifying message
    if reminder:
        messages.append({"role": "assistant", "content": reminder})
    

    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_completion_tokens=5000
    )

    raw = response.choices[0].message.content
    # Log the raw LLM response for debugging
    logging.info(f"Raw GPT response: {raw}")
    return extract_vb_code(raw)



def extract_vb_code(raw_code):
    """
    Extracts VBA code from fenced code blocks (```vb, ```vba, or untagged),
    or falls back to capturing a Sub...End Sub macro if fences are missing.
    """
    # Try fenced blocks with vb or vba tag
    match = re.search(r'```(?:vb|vba)(.*?)```', raw_code, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Try untagged fenced block
    match2 = re.search(r'```(.*?)```', raw_code, re.DOTALL)
    if match2:
        return match2.group(1).strip()
    # Fallback: capture Sub CreatePresentation()...End Sub
    fallback = re.search(r'(Sub CreatePresentation\(.*?End Sub)', raw_code, re.DOTALL)
    if fallback:
        return fallback.group(1).strip()
    # As last resort, return entire raw
    return raw_code.strip()
