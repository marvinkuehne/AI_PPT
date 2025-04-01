# Business logic for pptx operations

import io
import sys
import logging
from pptx import Presentation
from pptx.util import Inches, Pt  # Provide common utilities
from config import AI_CONFIG
import uuid

# API AI model
openai.api_key = AI_CONFIG["openai"]["api_key"]
MODEL = AI_CONFIG["openai"]["model"]


@app.route('/convert', methods=['POST'])
def convert():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "No image provided"}), 400

        if not validate_image_data(data['image']):
            return jsonify({"error": "Invalid image format"}), 400  # what is a valid image???

        img_bytes = extract_image_bytes(data['image'])  # why decoding image happens as part of the route process

        try:
            Image.open(io.BytesIO(img_bytes)).verify()
        except:
            return jsonify({"error": "Invalid image data"}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(img_bytes)
            img_path = tmp.name

        analysis = analyze_image(img_path)
        if not analysis:
            return jsonify({"error": "AI analysis failed"}), 400

        code_match = re.search(r'```python(.*?)```', analysis, re.DOTALL)
        if not code_match:
            return jsonify({"error": "No valid Python code generated"}), 400

        ppt_code = code_match.group(1).strip()

        if 'add_freeform' in ppt_code:
            return jsonify({"error": "Generated code uses unsupported method: add_freeform()"}), 400

        # Add shape-related imports if missing
        required_imports = [
            'MSO_SHAPE', 'MSO_CONNECTOR', 'MSO_LINE', 'MSO_FILL'
        ]
        if not all(imp in ppt_code for imp in required_imports):
            ppt_code = (
                    "from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR\n"
                    "from pptx.enum.dml import MSO_LINE, MSO_FILL\n" + ppt_code
            )

        exec_globals = {
            'Presentation': Presentation,
            'Inches': Inches,
            'Pt': Pt,
            'RGBColor': RGBColor,
            'PP_ALIGN': PP_ALIGN,
            'MSO_SHAPE': MSO_SHAPE,
            'MSO_CONNECTOR': MSO_CONNECTOR,
            'MSO_LINE': MSO_LINE,
            'MSO_FILL': MSO_FILL
        }

        try:
            exec(ppt_code, exec_globals)
            if 'create_slide' not in exec_globals:
                return jsonify({"error": "Missing create_slide function"}), 400

            prs = exec_globals['create_slide']()

            if not hasattr(prs, 'save'):
                return jsonify({"error": "Invalid presentation object"}), 400

            ppt_stream = io.BytesIO()
            prs.save(ppt_stream)
            ppt_stream.seek(0)

            return send_file(
                ppt_stream,
                as_attachment=True,
                download_name='output.pptx',
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )

        except Exception as e:
            return jsonify({"error": f"Execution error: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    finally:
        if 'img_path' in locals() and os.path.exists(img_path):
            try:
                os.unlink(img_path)
            except:
                pass
