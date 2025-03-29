from flask import Flask, request, render_template, jsonify
import os
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import uuid

app = Flask(__name__)

# 폴더 설정
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# 필요 시 Windows 사용자용 poppler 경로 설정
# 아래 경로는 본인의 poppler 경로로 바꿔주세요
POPPLER_PATH = r'C:\poppler-xx\bin'  # 예: C:\poppler-23.11.0\Library\bin

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdf']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_images = []

        try:
            # 👉 Poppler 경로는 OS에 맞게 설정 필요
            images = convert_from_path(filepath, dpi=200, poppler_path=POPPLER_PATH)

            for i, img in enumerate(images):
                unique_name = f"{uuid.uuid4().hex[:8]}_page_{i + 1}.png"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], unique_name)
                img.save(output_path, 'PNG')
                output_images.append(f"/static/outputs/{unique_name}")

            return jsonify({'images': output_images})

        except Exception as e:
            return jsonify({'error': f'PDF 변환 중 오류: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
