from PIL import Image
from google import genai
from flask import Flask, request, render_template, Blueprint
import io

resume1 = Blueprint('resume1', __name__)
client = genai.Client(api_key="AIzaSyBMa2hRCbDsdqw-Vm7WhJ8xsRgEtrjrRLs")

@resume1.route('/')
def home():
    return render_template('resume1.html')

@resume1.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    # Read the uploaded image
    image_data = file.read()
    image = Image.open(io.BytesIO(image_data))

    # Process with Gemini
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[image, "Tell me about this instrument"]
    )
    
    return response.text

if __name__ == '__main__':
    app.run(debug=True)