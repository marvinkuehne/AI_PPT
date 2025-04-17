# app.py: Main file that starts the Flask app, handles all routes and orchestrates logic

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import tempfile

from utils import validate_image_data, extract_image_bytes
from gpt_service import run_gpt_and_build_vb  # Achtung: Hier wird nun der VB-Code generiert!

app = Flask(__name__)
CORS(app)

# Hier wird ausschließlich der GPT/VB-Modus genutzt,
# sodass keine PowerPoint-Datei erzeugt wird.
MODE = "gpt"

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        img_b64 = data.get("image")
        if not validate_image_data(img_b64):
            return jsonify({"error": "Invalid image format"}), 400

        # Bild aus den Base64-Daten laden
        img = Image.open(BytesIO(extract_image_bytes(img_b64)))

        # Bild temporär speichern, um es an den GPT-Service weiterzugeben.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            img.save(tmp.name)
            vb_code = run_gpt_and_build_vb(tmp.name)

        # Den generierten VBA-Code als Textdatei (z.B. result.bas) zurücksenden.
        vb_stream = BytesIO(vb_code.encode("utf-8"))
        vb_stream.seek(0)
        return send_file(vb_stream,
                         as_attachment=True,
                         download_name="result.bas",
                         mimetype="text/plain")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)