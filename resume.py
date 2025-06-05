from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import os
from werkzeug.utils import secure_filename
from PIL import Image
import google.generativeai as genai
import io

resume = Blueprint('resume', __name__)

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume.route('/resume')
def home_page():
    if 'user_id' in session:
        ai_feedback = session.pop('ai_feedback', None) if 'ai_feedback' in session else None
        return render_template('resume.html', name=session['name'], ai_feedback=ai_feedback)
    return redirect(url_for('auth.index'))

@resume.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('resume.home_page'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('resume.home_page'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        # Process the resume using Gemini API
        try:
            # Initialize Gemini API client
            client = genai.GenerativeModel(model_name='gemini-1.5-flash',
                                   generation_config=None,
                                   safety_settings=None,
                                   tools=None,
                                   api_key="AIzaSyBMa2hRCbDsdqw-Vm7WhJ8xsRgEtrjrRLs")

            # Read the image file
            with open(file_path, "rb") as image_file:
                image_data = image_file.read()

            img = Image.open(io.BytesIO(image_data))

            # Generate content with the model
            response = client.generate_content([img, "Analyze this resume and provide feedback."])
            ai_feedback = response.text

            # Store the AI feedback in the session
            
            flash('Resume analyzed successfully!', 'success')
            session['ai_feedback'] = ai_feedback

        except Exception as e:
            flash(f'Error analyzing resume: {str(e)}', 'error')

        return redirect(url_for('resume.home_page'))

    flash('Invalid file type. Please upload a PDF, DOC, DOCX, TXT, JPG, or PNG file.', 'error')
    return redirect(url_for('resume.home_page'))
