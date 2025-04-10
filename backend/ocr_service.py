# ocr_service.py: Improved OCR with layout reconstruction

import pytesseract
from pptx_service import create_ppt_from_structure, create_ppt_from_elements
from PIL import Image, ImageOps

def preprocess_image(image):
    gray = image.convert("L")
    enhanced = ImageOps.autocontrast(gray)
    binarized = enhanced.point(lambda x: 0 if x < 150 else 255, '1')
    return binarized

def analyze_with_ocr(image):
    cleaned = preprocess_image(image)
    data = pytesseract.image_to_data(cleaned, output_type=pytesseract.Output.DICT)

    elements = []
    SCALE = 100  # pixels per inch approximation
    FONT_SCALE = 1.3  # convert pixel height to pt (rough guess)

    for i, word in enumerate(data['text']):
        if int(data['conf'][i]) < 50 or not word.strip():
            continue

        x = data['left'][i]
        y = data['top'][i]
        w = data['width'][i]
        h = data['height'][i]

        element = {
            "text": word,
            "left": x / SCALE,
            "top": y / SCALE,
            "width": w / SCALE,
            "height": h / SCALE,
            "font_size": h * FONT_SCALE
        }
        elements.append(element)

    return elements

def run_ocr_and_build_pptx(image):
    elements = analyze_with_ocr(image)
    return create_ppt_from_elements(elements)
