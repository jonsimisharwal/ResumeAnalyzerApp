import re
import fitz  # PyMuPDF
import spacy
import streamlit as st


nlp = spacy.load("en_core_web_sm")

# Extract raw text from PDF
def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Extract clean project titles from resume
def extract_projects(text):
    lines = text.split('\n')
    project_titles = []
    seen = set()

    for line in lines:
       line = line.strip()
       if not line or len(line.split()) > 10:
          continue

       lower_line = line.lower()
       if any(x in lower_line for x in [
            "developed", "implemented", "designed", "engineer", 
            "university", "bachelor", "expected", "achievement"
        ]):
            continue
       if (
            re.search(r'\b(project|clone|system|app|tool|game|engine)\b', lower_line)
            or re.search(r'\(.+\)', line)
        ):
            if line not in seen:
                seen.add(line)
                project_titles.append(line)

    return project_titles

# Score the resume based on extracted data
def calculate_resume_score(parsed_data, raw_text):
    score = 0
    
    if parsed_data.get("name"): score += 5
    if parsed_data.get("email"): score += 5
    if parsed_data.get("phone"): score += 5

    if parsed_data.get("college"): score += 10

    skills = parsed_data.get("skills", [])
    if len(skills) >= 5:
        score += 20
    elif len(skills) >= 3:
        score += 10

    projects = parsed_data.get("projects", [])
    if len(projects) >= 3:
        score += 20
    elif len(projects) >= 1:
        score += 10

    if len(raw_text.split()) > 200:
        score += 10

    return score

def generate_suggestions(parsed_data, raw_text,score):
    suggestions = []
   
    if not parsed_data.get("name"):
        suggestions.append("Add your name or ensure it appears near your email.")

    if not parsed_data.get("email"):
        suggestions.append("Include a professional email address.")

    if not parsed_data.get("phone"):
        suggestions.append("Include a valid phone number.")

    if not parsed_data.get("college"):
        suggestions.append("Mention your college or university name.")

    skills = parsed_data.get("skills", [])
    if len(skills) < 5:
        suggestions.append(f"You have {len(skills)} skills. Add more to reach at least 5.")

    projects = parsed_data.get("projects", [])
    if len(projects) < 4:
        suggestions.append(f"You have {len(projects)} projects. Add at least 3 project titles.")

    if len(raw_text.split()) <= 200:
        suggestions.append("Increase your resume length beyond 200 words to add depth.")
    if score < 90 and not suggestions:
        suggestions.append("To boost your resume score, consider adding certifications, achievements, or more projects.")
    
    return suggestions





# Main extractor function
def extract_info(text):
    name = ""
    email = ""
    phone = ""
    skills = []
    college = ""
    projects = []

    # Email & name
    email_match = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', text)
    if email_match:
        email = email_match.group(0)
        name = email.split("@")[0]

    # Phone
    phone_match = re.search(r'(\+91[-\s]?)?\d{10}', text)
    if phone_match:
        phone = phone_match.group(0)

    # College
    college_match = re.search(r'(?i)(?:at|from)?\s*(.*?)\s*(University|College|Institute|NIT|IIT|IIIT)[^\n]*', text)
    if college_match:
        college = f"{college_match.group(1).strip()} {college_match.group(2).strip()}"

    # Skills
    skill_keywords = set([
        "Python", "Java", "C++", "C", "JavaScript", "React", "Node.js", "Django", "Flask",
        "MongoDB", "MySQL", "HTML", "CSS", "Kotlin", "Swift", "PHP", "TensorFlow",
        "Pandas", "NumPy", "Matplotlib", "SQL", "Git", "Linux", "Excel", "Power BI",
        "AWS", "Firebase", "Tailwind", "Bootstrap", "TypeScript"
    ])
    found_skills = [word.strip(",.():") for word in text.split() if word.strip(",.():") in skill_keywords]
    skills = list(set(found_skills))

    # Projects
    projects = extract_projects(text)

    # Package data
    parsed_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "college": college,
        "skills": skills,
        "projects": projects
    }

    # Resume score
    score = calculate_resume_score(parsed_data, text)
    parsed_data["score"] = score

    

# Only generate suggestions if score is below 90
    st.write("🧪 Resume word count:", len(text.split()))

    suggestions = generate_suggestions(parsed_data, text,score)
    parsed_data["suggestions"] = suggestions

    if parsed_data["suggestions"]:
           st.subheader("📈 Suggestions to Improve Your Resume Score")
           for s in parsed_data["suggestions"]:
                st.write("🔸", s)
    else:
        st.success("🎉 Great job! Your resume is already well-optimized.")
        



    return parsed_data
