import os
from utils import clean_text  # Import clean_text
import json
import re  # ✅ For extracting email, phone, etc.
import pandas as pd
from extract_text import extract_text_from_pdf, extract_text_from_docx
from section_identifier import identify_sections
from extract_information import (
    extract_experience,
    extract_education,
    extract_skills,
    postprocess_experience_dates,  # <-- NEW import
    postprocess_education_dates,  # <-- NEW import
)

def extract_personal_info(general_section):
    """Extracts name, email, and phone number from the general information section."""
    name, email, phone = None, None, None

    for line in general_section:
        line = line.strip()
        # ✅ Skip empty lines
        if not line:
            continue

        # ✅ Detect Email
        if not email:
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line)
            if email_match:
                email = email_match.group(0)

        # ✅ Detect Phone Number
        if not phone:
            phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}", line)
            if phone_match:
                phone = phone_match.group(0)

        # ✅ Detect Name (first line, avoiding links)
        if not name and "@" not in line and "linkedin.com" not in line and "github.com" not in line:
            name = line.strip()

    return {
        "Name": name or "Unknown",
        "Email": email or "Unknown",
        "Phone": phone or "Unknown",
    }


def parse_resume(file_path):
    """Parse a resume and extract structured information."""
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        resume_text = extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        resume_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

    # Identify sections
    sections = identify_sections(resume_text)

    # Extract personal info
    personal_info = extract_personal_info(sections.get("General", []))

    # Extract Experience
    experience_list = extract_experience(sections.get("Experience", []))
    # <-- NEW: Post-process to remove date ranges from Position
    experience_list = postprocess_experience_dates(experience_list)

    # Extract Education
    education_list = extract_education(sections.get("Education", []))
    education_list = postprocess_education_dates(education_list)       # <--- new call


    # Merge languages into skills if desired (or keep them separate)
    skills_data = [clean_text(skill) for skill in sections.get("Skills", [])]
    languages_data = [clean_text(lang) for lang in sections.get("Languages", [])]
    # Combine them
    skills_data += languages_data

    # Build structured data
    structured_data = {
        "Name": personal_info["Name"],
        "Email": personal_info["Email"],
        "Phone": personal_info["Phone"],
        "Experience": [
            {
                key: clean_text(value) if isinstance(value, str) else value
                for key, value in exp.items()
            }
            for exp in experience_list
        ],
        "Education": [
            {
                key: clean_text(value) if isinstance(value, str) else value
                for key, value in edu.items()
            }
            for edu in education_list
        ],
        "Skills": skills_data or ["No skills data available"],
        "Projects": [
            clean_text(proj)
            for proj in sections.get("Projects", ["No project data available"])
        ],
        # Keep extracurricular separate if you want
        "Extracurricular Activities": [
            clean_text(activity)
            for activity in sections.get(
                "Extracurricular Activities", ["No extracurricular data available"]
            )
        ],
    }

    return structured_data, sections


def save_to_csv(parsed_data, output_csv="parsed_resumes.csv"):
    df = pd.DataFrame([parsed_data])  # ✅ Wrap parsed_data in a list
    df.to_csv(output_csv, index=False)
    print("✅ Resume data saved to", output_csv)


# ✅ Run the Parser if needed
if __name__ == "__main__":
    resume_path = "sample_resume.pdf"  # Change to your actual resume file
    parsed_data, sections = parse_resume(resume_path)
    save_to_csv(parsed_data)
