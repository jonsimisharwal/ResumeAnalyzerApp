import re
import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def extract_projects(text):
    lines = text.split('\n')
    project_titles = []
    seen = set()

    for line in lines:
        line = line.strip()

        # Skip blank lines or long sentences (likely descriptions)
        if not line or len(line.split()) > 10:
            continue

        # Filter out lines that are not project names
        lower_line = line.lower()
        if any(x in lower_line for x in [
            "developed", "implemented", "designed", "engineer","university", "bachelor", "expected", "achievement"
        ]):
            continue

        # Select lines that look like project titles
        if (
            re.search(r'\b(project|clone|system|app|tool|game|engine)\b', lower_line)
            or re.search(r'\(.+\)', line)
        ):
            if line not in seen:
                seen.add(line)
                project_titles.append(line)

    return project_titles







def extract_info(text):
    name = ""
    email = ""
    phone = ""
    skills = []
    college = ""
    projects = []

    email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', text)
    if email_match:
        email = email_match.group(0)
        name = email.split("@")[0]

    phone_match = re.search(r'(\+91[-\s]?)?\d{10}', text)
    if phone_match:
        phone = phone_match.group(0)

    college_match = re.search(r'(?i)(?:at|from)?\s*(.*?)\s*(University|College|Institute|NIT|IIT|IIIT)[^\n]*', text)
    if college_match:
        college = f"{college_match.group(1).strip()} {college_match.group(2).strip()}"

    skill_keywords = set([
        "Python", "Java", "C++", "C", "JavaScript", "React", "Node.js", "Django", "Flask",
        "MongoDB", "MySQL", "HTML", "CSS", "Kotlin", "Swift", "PHP", "TensorFlow",
        "Pandas", "NumPy", "Matplotlib", "SQL", "Git", "Linux", "Excel", "Power BI",
        "AWS", "Firebase", "Tailwind", "Bootstrap", "TypeScript"
    ])
    found_skills = [word.strip(",.():") for word in text.split() if word.strip(",.():") in skill_keywords]
    skills = list(set(found_skills))

    projects = extract_projects(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "college": college,
        "skills": skills,
        "projects": projects
    }
