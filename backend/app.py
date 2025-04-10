# app.py: Main file that starts the Flask app, handles all routes and orchestrates logic

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import tempfile

from utils import validate_image_data, extract_image_bytes
from ocr_service import run_ocr_and_build_pptx
from gpt_service import run_gpt_and_build_pptx

app = Flask(__name__)
CORS(app)

# Choose analysis mode: "ocr" or "gpt"
MODE = "ocr"

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        img_b64 = data.get("image")
        if not validate_image_data(img_b64):
            return jsonify({"error": "Invalid image format"}), 400

        img = Image.open(BytesIO(extract_image_bytes(img_b64)))

        if MODE == "ocr":
            pptx = run_ocr_and_build_pptx(img)
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                img.save(tmp.name)
                pptx = run_gpt_and_build_pptx(tmp.name)

        stream = BytesIO()
        pptx.save(stream)
        stream.seek(0)
        return send_file(stream, as_attachment=True, download_name="result.pptx")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
