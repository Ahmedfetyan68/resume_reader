import os
from utils import clean_text  # Import clean_text
import json
import re  # For extracting email, phone, etc.
import pandas as pd
from extract_text import extract_text_from_pdf, extract_text_from_docx
from section_identifier import identify_sections
from extract_information import (
    extract_experience,
    extract_education,
    extract_skills,
    postprocess_experience_dates,   # Already exists
    postprocess_education_dates,      # Already exists
    postprocess_skills,               # Already exists
    postprocess_projects              # Already exists
)

def extract_personal_info(general_section):
    """Extracts name, email, and phone number from the general information section."""
    name, email, phone = None, None, None

    for line in general_section:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue

        # Detect Email
        if not email:
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line)
            if email_match:
                email = email_match.group(0)

        # Detect Phone Number
        if not phone:
            phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}", line)
            if phone_match:
                phone = phone_match.group(0)

        # Detect Name (first non-empty line that isn't a link/email)
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

    # Extract Experience and post-process dates
    experience_list = extract_experience(sections.get("Experience", []))
    experience_list = postprocess_experience_dates(experience_list)

    # Extract Education and post-process dates
    education_list = extract_education(sections.get("Education", []))
    education_list = postprocess_education_dates(education_list)

    # Extract Skills (merge languages into skills) and post-process skills
    raw_skills = [clean_text(skill) for skill in sections.get("Skills", [])]
    raw_languages = [clean_text(lang) for lang in sections.get("Languages", [])]
    merged_skills = raw_skills + raw_languages
    cleaned_skills = postprocess_skills(merged_skills)

    # Extract Projects and post-process into title/description structure
    raw_projects = [clean_text(proj) for proj in sections.get("Projects", ["No project data available"])]
    structured_projects = postprocess_projects(raw_projects)

    # Extract Extracurricular Activities (if you want to keep them separate)
    extracurricular = [
        clean_text(activity)
        for activity in sections.get("Extracurricular Activities", ["No extracurricular data available"])
    ]

    # Build final structured data
    structured_data = {
        "Name": personal_info["Name"],
        "Email": personal_info["Email"],
        "Phone": personal_info["Phone"],
        "Experience": [
            {key: clean_text(value) if isinstance(value, str) else value for key, value in exp.items()}
            for exp in experience_list if isinstance(exp, dict)  # Ensures exp is a dictionary
        ],


        "Education": [
            {key: clean_text(value) if isinstance(value, str) else value for key, value in edu.items()}
            for edu in education_list if isinstance(edu, dict)  # ✅ Skips invalid entries
        ]
,
        "Skills": cleaned_skills or ["No skills data available"],
        "Projects": structured_projects,
        "Extracurricular Activities": extracurricular,
    }

    return structured_data, sections


def save_to_csv(parsed_data, output_csv="parsed_resumes.csv"):
    """Save structured resume data to a CSV file."""
    df = pd.DataFrame([parsed_data])
    df.to_csv(output_csv, index=False)
    print("✅ Resume data saved to", output_csv)


# Run the Parser if needed
if __name__ == "__main__":
    resume_path = "AhmedEssamCV 1.pdf"  # Change to your actual resume file
    parsed_data, sections = parse_resume(resume_path)
    save_to_csv(parsed_data)
    print(json.dumps(parsed_data, indent=2))
