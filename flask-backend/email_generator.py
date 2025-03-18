import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# Configure API Key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_email_content(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")  # Use "gemini-1.5-pro" or "gemini-1.5-flash"
    
    response = model.generate_content(prompt)
    
    return response.text


def formal_professional_email(title, abstract, skills, projects, researcher):
    prompt = f"""
    Generate a formal and professional internship request email for Dr. {researcher} based on the following details:

    Title of the paper: {title}
    Abstract: {abstract}
    Skills: {skills}
    Projects: {projects}

    The email should address Dr. {researcher}, express interest in their research, highlight relevant skills and projects, and politely request an internship opportunity. 
    Keep the tone professional and to the point.
    """
    return generate_email_content(prompt)



def enthusiastic_email(title, abstract, skills, projects, researcher):
    prompt = f"""
    Generate an enthusiastic and engaging internship request email for Dr. {researcher} based on the following details:

    Title of the paper: {title}
    Abstract: {abstract}
    Skills: {skills}
    Projects: {projects}

    The email should address Dr. {researcher}, express excitement about their research, highlight how the candidate's skills and projects align with their work, and request an internship opportunity.
    Keep the tone energetic and professional.
    """
    return generate_email_content(prompt)


def technical_email(title, abstract, skills, projects, researcher):
    prompt = f"""
    Generate a detailed and technically accurate internship request email for Dr. {researcher} based on the following details:

    Title of the paper: {title}
    Abstract: {abstract}
    Skills: {skills}
    Projects: {projects}

    The email should address Dr. {researcher}, focus on technical alignment with the research paper, highlight the candidate's relevant technical expertise, and request an internship opportunity.
    Keep the tone technical and research-focused.
    """
    return generate_email_content(prompt)

if __name__ == "__main__":
    # Example data
    title = "Deep Learning for Image Recognition"
    abstract = "This paper explores the use of convolutional neural networks for image classification tasks."
    skills = "Python, TensorFlow, Computer Vision"
    projects = "Image Classification using CNNs, Transfer Learning"

    print("=== Formal & Professional ===")
    print(formal_professional_email(title, abstract, skills, projects,researcher="John Doe"))
    print("\n=== Enthusiastic ===")
    print(enthusiastic_email(title, abstract, skills, projects,researcher="John Doe"))
    print("\n=== Technical ===")
    print(technical_email(title, abstract, skills, projects,researcher="John Doe"))