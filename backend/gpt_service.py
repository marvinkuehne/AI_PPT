# gpt_service.py:

import os
import base64
import re
import requests
import openai  # for openai
from dotenv import load_dotenv  # Load .env support
from pptx_service import create_ppt_from_gpt_code

# Load environment variables from .env file
load_dotenv()

# Configuration
PROVIDER = "deepseek"  # Alternatives: "openai" "gemini", "deepseek"
MODEL = "deepseek-chat"     # Model name: "gpt-4o",

# API-Keys
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

# Entry point from app.py
def run_gpt_and_build_pptx(image_path):
    code = analyze_slide_with_ai(image_path)
    return create_ppt_from_gpt_code(code)

# Selection logic
def analyze_slide_with_ai(image_path):
    if PROVIDER == "openai":
        return analyze_with_openai(image_path)
    elif PROVIDER == "gemini":
        return analyze_with_gemini(image_path)
    elif PROVIDER == "deepseek":
        return analyze_with_deepseek(image_path)
    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")

# OpenAI GPT models
def analyze_with_openai(image_path):
    openai.api_key = OPENAI_KEY

    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a PowerPoint reconstruction AI. Your task is to extract layout, shapes and texts "
                    "from the provided slide image and generate **valid Python code** using python-pptx.\n\n"
                    "IMPORTANT RULES:\n"
                    "1. Output must contain exactly one Python function named `create_slide()`.\n"
                    "2. This function must return a `Presentation` object.\n"
                    "3. Only use: add_shape, add_textbox, add_picture – NO `add_freeform()`.\n"
                    "4. Use `Inches()` for all positioning.\n"
                    "5. Do NOT explain anything. Only return pure code inside a ```python block.\n\n"
                    "Start the response like this:\n"
                    "```python\n"
                    "def create_slide():\n"
                    "    prs = Presentation()\n"
                    "    slide = prs.slides.add_slide(prs.slide_layouts[6])\n"
                    "    # ... elements here ...\n"
                    "    return prs\n"
                    "```"
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please reconstruct this slide from the image:"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded}"}}
                ]
            }
        ],
        max_tokens=4000,
        temperature=0.1,
        top_p=0.95
    )
    return response.choices[0].message.content

# Gemini API via HTTP, prompt in user message
def analyze_with_gemini(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode("utf-8")

    body = {
        "contents": [
            {
                "parts": [
                    {"text": (
                        "Please analyze this slide image and respond with ONLY a python function named `create_slide()` that builds the layout using python-pptx.\n"
                        "Do not include any explanation or commentary. The function must return a `Presentation` object.\n"
                        "Avoid using unsupported methods like `add_freeform()`. Use only `add_shape`, `add_textbox`, `add_picture`.\n"
                        "Use Inches() for all positioning. Start your response in a ```python block."
                    )},
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": encoded_image
                        }
                    }
                ]
            }
        ]
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_KEY}"
    response = requests.post(url, json=body)
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

# DeepSeek prompt via HTTP with strict code-only instruction
def analyze_with_deepseek(image_path):
    if not DEEPSEEK_KEY:
        raise ValueError("DEEPSEEK_API_KEY is missing! Check .env file")

    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a PowerPoint AI. Generate python-pptx code with:\n"
                    "1. One function create_slide() returning Presentation\n"
                    "2. Use add_shape/add_textbox/add_picture only\n"
                    "3. Use Inches() for positioning\n"
                    "4. Output ONLY code in ```python block"
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Reconstruct this slide:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded}",
                            "detail": "auto"  # Required for image processing
                        }
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        gpt_code = result["choices"][0]["message"]["content"]

        # Extract code block
        code_match = re.search(r'```python\n(.*?)```', gpt_code, re.DOTALL)
        return code_match.group(1).strip() if code_match else gpt_code

    except Exception as e:
        print(f"DeepSeek Error: {response.text if response else str(e)}")
        raise