import os
from utils import clean_text  # Import clean_text
import json
import re  # ✅ Import regex module for extracting email, phone, etc.
import pandas as pd
from extract_text import extract_text_from_pdf, extract_text_from_docx
from section_identifier import identify_sections
from extract_information import extract_experience, extract_education, extract_skills


# ✅ Function to Extract Personal Info (Name, Email, Phone)

# Function to clean text by replacing special bullet points


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

        # ✅ Detect Name (First line, avoiding links)
        if not name and "@" not in line and "linkedin.com" not in line and "github.com" not in line:
            name = line.strip()

    return {
        "Name": name or "Unknown",
        "Email": email or "Unknown",
        "Phone": phone or "Unknown"
    }

# ✅ Function to Parse Resume
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

    # Extract structured information
    structured_data = {
        "Name": extract_personal_info(sections.get("General", []))["Name"],
        "Email": extract_personal_info(sections.get("General", []))["Email"],
        "Phone": extract_personal_info(sections.get("General", []))["Phone"],
        "Experience": [
            {key: clean_text(value) if isinstance(value, str) else value for key, value in exp.items()}
            for exp in extract_experience(sections.get("Experience", []))
        ],
        "Education": [
            {key: clean_text(value) if isinstance(value, str) else value for key, value in edu.items()}
            for edu in extract_education(sections.get("Education", []))
        ],
        "Skills": [clean_text(skill) for skill in sections.get("Skills", ["No skills data available"])],
        "Projects": [clean_text(proj) for proj in sections.get("Projects", ["No project data available"])],
        "Extracurricular Activities": [
            clean_text(activity) for activity in sections.get("Extracurricular Activities", ["No extracurricular data available"])
        ],
        "Languages": [clean_text(lang) for lang in sections.get("Languages", ["No language data available"])],
    }

    return structured_data, sections

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

    # Extract personal information
    personal_info = extract_personal_info(sections.get("General", []))

    # Extract structured information
    structured_data = {
    "Name": personal_info["Name"],
    "Email": personal_info["Email"],
    "Phone": personal_info["Phone"],
    "Experience": [
    {key: clean_text(value) if isinstance(value, str) else value for key, value in exp.items()}
    for exp in extract_experience(sections.get("Experience", []))
],
    "Education": [
        {key: clean_text(value) for key, value in edu.items()}
        for edu in extract_education(sections.get("Education", []))
    ],
    "Skills": [clean_text(skill) for skill in extract_skills(sections.get("Skills", []))],
    "Projects": [clean_text(proj) for proj in sections.get("Projects", ["No project data available"])],
    "Extracurricular Activities": [
        clean_text(activity) for activity in sections.get("Extracurricular Activities", ["No extracurricular data available"])
    ],
    "Languages": [clean_text(lang) for lang in sections.get("Languages", ["No language data available"])]
}


    return structured_data, sections  # ✅ Fix: Ensure both values are returned

# ✅ Function to Save to CSV
def save_to_csv(parsed_data, output_csv="parsed_resumes.csv"):
    df = pd.DataFrame([parsed_data])  # ✅ Wrap parsed_data in a list to avoid structure issues
    df.to_csv(output_csv, index=False)

# ✅ Run the Parser
if __name__ == "__main__":
    resume_path = "sample_resume.pdf"  # Change to actual resume file
    parsed_data, sections = parse_resume(resume_path)  # ✅ Fix: Correctly capture two return values

    # Save to CSV
    save_to_csv(parsed_data)
    print("✅ Resume data saved to parsed_resumes.csv")
