from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid
from paper_retrieval import get_research_papers
from resume_processor import process_resume
from similarity import compute_highest_similarity
from email_generator import formal_professional_email, enthusiastic_email, technical_email

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload-resume/', methods=['POST'])
def upload_resume():
    """Handles resume uploads and extracts skills & projects."""
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    extracted_data = process_resume(file_path)

    return jsonify({
        "success": True,
        "fileName": file.filename,
        "resumeId": filename,
        "extractedData": extracted_data
    })

@app.route('/api/search-researcher/', methods=['POST'])
def search_researcher():
    """Fetches real research papers using Semantic Scholar API."""
    data = request.json
    researcher_name = data.get('researcher', '').strip()

    if not researcher_name:
        return jsonify({"error": "Researcher name is required"}), 400

    print(f"Searching for researcher: {researcher_name}")

    papers, researcher_details = get_research_papers(researcher_name)

    print(f"Fetched researcher: {researcher_details['researcher']}")
    print(f"Fetched papers: {papers}")

    if not papers:
        return jsonify({"error": "No research papers found"}), 404

    return jsonify({
        "researcher": researcher_details["researcher"],
        "papers": papers
    })

@app.route('/api/get-email-templates/', methods=['POST'])
def get_email_templates():
    """Generates email templates using Gemini AI based on research paper data."""
    data = request.json
    researcher = data.get('researcher', 'Unknown Researcher')  # ✅ Ensure researcher name is included
    title = data.get('title', 'No Title')
    abstract = data.get('abstract', 'No Abstract')
    skills = data.get('skills', 'Not Provided')
    projects = data.get('projects', 'Not Provided')

    # Call Gemini AI email generation functions
    professional_email = formal_professional_email(title, abstract, skills, projects, researcher)
    enthusiastic_email_content = enthusiastic_email(title, abstract, skills, projects, researcher)
    technical_email_content = technical_email(title, abstract, skills, projects, researcher)

    email_templates = [
        {
            "type": "Formal & Professional",
            "content": professional_email
        },
        {
            "type": "Enthusiastic & Passionate",
            "content": enthusiastic_email_content
        },
        {
            "type": "Technical & Research-Oriented",
            "content": technical_email_content
        }
    ]

    return jsonify(email_templates)


@app.route('/api/send-email/', methods=['POST'])
def send_email():
    """Mocks sending an email."""
    data = request.json
    researcher_name = data.get('researcher', 'Unknown Researcher')
    template_type = data.get('template', {}).get('type', 'Unknown')

    print(f"Mock email sent to {researcher_name}")
    print(f"Template used: {template_type}")

    return jsonify({
        "success": True,
        "message": f"Mock email successfully sent to {researcher_name}!"
    })

if __name__ == '__main__':
    app.run(port=8000, debug=True)
