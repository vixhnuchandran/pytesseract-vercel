from flask import Flask, request, jsonify
import json
import pytesseract
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'pytesseract vercel '


@app.route('/api/ocr', methods=['POST'])
def ocr():
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            # Handle JSON request
            try:
                request_body = request.get_json()
                image = base64_to_image(request_body['image'])
                result = process_image(image)

                text = construct_text(result)
                bboxes = [{'text': bbox['text'], 'data': {'confidence': bbox['confidence'], 'bbox': bbox['bbox']}} for bbox in result]

                response_body = {
                    "text": text,
                    "bboxes": bboxes
                }

                return jsonify(response_body), 200
            except KeyError:
                return 'Image data not provided', 400
            except Exception as e:
                return str(e), 500
        elif 'image' in request.files:
            try:
                image_file = request.files['image']
                image = Image.open(image_file.stream)
                result = process_image(image)

                text = construct_text(result)
                bboxes = [{'text': bbox['text'], 'data': {'confidence': bbox['confidence'], 'bbox': bbox['bbox']}} for bbox in result]

                response_body = {
                    "text": text,
                    "bboxes": bboxes
                }

                return jsonify(response_body), 200
            except Exception as e:
                return str(e), 500
        else:
            return 'Unsupported media type', 415
    else:
        return 'Only POST requests are allowed for this endpoint', 405

def base64_to_image(base64_str):
    format, imgstr =  base64_str.split(';base64,')
    ext = format.split('/')[-1]
    
    image_bytes = base64.b64decode(imgstr)
    
    image = Image.open(BytesIO(image_bytes))
    return image

def construct_text(result):
    text = ""

    for bbox in result:
        text += bbox['text'] + " "

    return text.strip()
def process_image(image):
    gray_img = image.convert('L')
    
    data = pytesseract.image_to_data(gray_img, output_type=pytesseract.Output.DICT)
    
    texts = [text for text in data['text'] if text.strip()]
    confidences = data['conf']
    lefts = data['left']
    tops = data['top']
    widths = data['width']
    heights = data['height']
    
    result = []
    for text, conf, left, top, width, height in zip(texts, confidences, lefts, tops, widths, heights):
        bbox = {
            'text': (text),
            'confidence': conf,
            'bbox': {
                'left': left,
                'top': top,
                'right': left + width,
                'bottom': top + height
            }
        }
        result.append(bbox)
    return result

if __name__ == "__main__":
    app.run(debug=True)
    
