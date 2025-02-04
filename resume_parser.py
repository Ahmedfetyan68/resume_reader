import os
import json
import re
import pandas as pd
from utils import clean_text
from extract_text import extract_text_from_pdf, extract_text_from_docx
from section_identifier import identify_sections
from extract_information import extract_experience, extract_education, extract_skills

def extract_personal_info(general_section):
    """
    Extracts name, email, and phone number from the general information section.
    Now with more robust regex patterns for email and phone numbers.
    """
    name, email, phone = None, None, None

    # More flexible email regex (supports plus-tags, multiple TLD lengths)
    email_pattern = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6}")

    # More flexible phone regex (handles country codes, parentheses, etc.)
    phone_pattern = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{3,9}")

    for line in general_section:
        line = line.strip()

        if not line:
            continue

        # Detect Email
        if not email:
            email_match = email_pattern.search(line)
            if email_match:
                email = email_match.group(0)

        # Detect Phone
        if not phone:
            phone_match = phone_pattern.search(line)
            if phone_match:
                phone = phone_match.group(0)

        # Detect Name (first non-empty line that isn't a link or email)
        if not name and "@" not in line and "linkedin.com" not in line and "github.com" not in line:
            name = line

    return {
        "Name": name or "Unknown",
        "Email": email or "Unknown",
        "Phone": phone or "Unknown"
    }

def parse_resume(file_path):
    """Parse a resume and extract structured information."""
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        resume_text = extract_text_from_pdf(file_path)
    elif file_extension == ".docx":
        resume_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please use PDF or DOCX.")

    # Identify sections
    sections = identify_sections(resume_text)

    # Personal info from general section
    personal_info = extract_personal_info(sections.get("General", []))

    # Merge 'Languages' lines under 'Skills'
    skill_lines = sections.get("Skills", [])
    language_lines = sections.get("Languages", [])
    merged_skills_section = skill_lines + language_lines
    skill_items = extract_skills(merged_skills_section)

    # Construct final structured data
    structured_data = {
        "Name": personal_info["Name"],
        "Email": personal_info["Email"],
        "Phone": personal_info["Phone"],
        "Experience": [
            {
                key: clean_text(value) if isinstance(value, str) else value
                for key, value in exp.items()
            }
            for exp in extract_experience(sections.get("Experience", []))
        ],
        "Education": [
            {
                key: clean_text(value) if isinstance(value, str) else value
                for key, value in edu.items()
            }
            for edu in extract_education(sections.get("Education", []))
        ],
        "Skills": skill_items,  # Merged languages into skills
        "Projects": [clean_text(proj) for proj in sections.get("Projects", [])],
        # Removed "Extracurricular Activities" entirely
    }

    return structured_data, sections

def save_to_csv(parsed_data, output_csv="parsed_resumes.csv"):
    """
    Saves the structured resume data to a CSV.
    Wrap `parsed_data` in a list so DataFrame interprets each key as a column.
    """
    df = pd.DataFrame([parsed_data])
    df.to_csv(output_csv, index=False)
    print(f"✅ Resume data saved to {output_csv}")


# Example usage (you can remove the __main__ block in production)
if __name__ == "__main__":
    resume_path = "sample_resume.pdf"  # Change to your actual file path
    parsed_data, sections = parse_resume(resume_path)
    save_to_csv(parsed_data)
