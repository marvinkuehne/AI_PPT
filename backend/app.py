import os
import tempfile
from io import BytesIO
import pythoncom
import win32com.client as com
import logging

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image

from utils import validate_image_data, extract_image_bytes
from gpt_service import run_gpt_and_build_vb

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        # 1) Decode incoming image
        data = request.get_json()
        img_b64 = data.get("image")
        if not validate_image_data(img_b64):
            return jsonify({"error": "Invalid image format"}), 400

        img = Image.open(BytesIO(extract_image_bytes(img_b64)))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            img.save(tmp_img.name)
            img_path = tmp_img.name

        # 2) Generate the VBA macro
        vb_code = run_gpt_and_build_vb(img_path)

        # 3) Launch PowerPoint via COM
        pythoncom.CoInitialize()
        ppt_app = com.Dispatch("PowerPoint.Application")
        ppt_app.Visible = True
        # optional: minimize the window
        ppt_app.WindowState = 2  # ppWindowMinimized

        # 4) Create a host presentation & inject the VBA
        host_pres = ppt_app.Presentations.Add()
        vb_proj   = host_pres.VBProject
        module    = vb_proj.VBComponents.Add(1)   # 1 = vbext_ct_StdModule
        module.Name = "GPTModule"
        module.CodeModule.AddFromString(vb_code)

        # 5) Run the macro — this creates _another_ presentation inside VBA
        ppt_app.Run("GPTModule.CreatePresentation")

        # 6) Find the newly-created presentation
        count = ppt_app.Presentations.Count
        if count > 1:
            # Get the last one (1-based index)
            new_pres = ppt_app.Presentations(count)
        else:
            # fallback
            new_pres = ppt_app.ActivePresentation

        # 7) Save that new presentation
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_pptx:
            out_path = tmp_pptx.name
        new_pres.SaveAs(out_path)

        # 8) Clean up: close both presentations and quit
        new_pres.Close()
        host_pres.Close()
        ppt_app.Quit()
        pythoncom.CoUninitialize()

        # 9) Stream back the filled PPTX
        return send_file(
            out_path,
            as_attachment=True,
            download_name="result.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    except Exception as e:
        logging.error(f"Error in /convert: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
