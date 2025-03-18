import pdfplumber
import spacy
from keybert import KeyBERT
import re

# Load models
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_skills_with_ner(text):
    """Extracts skills using spaCy's Named Entity Recognition (NER)."""
    doc = nlp(text)
    skills = set()
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "SKILL"]:
            skills.add(ent.text)
    return list(skills)

def extract_skills_with_keybert(text):
    """Extracts skills using KeyBERT."""
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)
    return [kw[0] for kw in keywords]

def extract_projects(text):
    """Extracts projects from resume using regex."""
    PROJECT_PATTERN = r"(Project:|Worked on|Developed)(.*?)(\n|$)"
    projects = re.findall(PROJECT_PATTERN, text)
    return [project[1].strip() for project in projects]

def process_resume(file):
    """Processes resume to extract skills and projects."""
    text = ""
    # Open file-like object directly with pdfplumber
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    text = text.replace("\n", " ").strip()

    skills_ner = extract_skills_with_ner(text)
    skills_keybert = extract_skills_with_keybert(text)
    skills = list(set(skills_ner + skills_keybert))

    projects = extract_projects(text)

    return {
        "skills": skills,
        "projects": projects
    }


if __name__ == "__main__":
    resume_file = input("Enter resume file path: ")
    extracted_data = process_resume(resume_file)
    print("\nExtracted Skills and Projects:")
    print(extracted_data)
