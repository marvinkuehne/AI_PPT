# utils.py: Base64-Validation and Picture extraction

import base64

def validate_image_data(image_data):
    if not image_data:
        return False
    if isinstance(image_data, str):
        if image_data.startswith('data:image'):
            return True
        try:
            base64.b64decode(image_data)
            return True
        except:
            return False
    return False

def extract_image_bytes(image_data):
    if image_data.startswith('data:image'):
        return base64.b64decode(image_data.split(',')[1])
    return base64.b64decode(image_data)
