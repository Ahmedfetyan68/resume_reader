from extract_text import extract_text_from_pdf, extract_text_from_docx
from section_identifier import identify_sections
from extract_information import extract_experience, extract_education, extract_skills
from save_to_csv import save_to_csv

import os
import json

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

    # ✅ Print extracted sections (Debugging)
    print("\n==== Extracted Sections ====")
    for section, content in sections.items():
        print(f"\n{section} (First 5 lines):")
        print("\n".join(content[:5]))  # Print first 5 lines of each section
        print("-" * 40)

    # Extract structured information
    structured_data = {
        "Experience": extract_experience(sections.get("Experience", [])),
        "Education": extract_education(sections.get("Education", [])),
        "Skills": extract_skills(sections.get("Skills", [])),
        "Projects": sections.get("Projects", ["No project data available"]),
        "Extracurricular Activities": sections.get("Extracurricular Activities", ["No extracurricular data available"]),
        "Languages": sections.get("Languages", ["No language data available"])
    }

    return structured_data, sections  # ✅ Return both parsed data and sections

# Test the parser
if __name__ == "__main__":
    resume_path = "sample_resume.pdf"  # Change this to the actual resume file path
    parsed_data, sections = parse_resume(resume_path)  # ✅ Capture returned sections

    # ✅ Print parsed data
    print("\n==== Structured Parsed Data ====")
    print(json.dumps(parsed_data, indent=4))

    # Ensure all fields have the same length before saving to CSV
    structured_list = []
    max_length = max(len(parsed_data[key]) for key in parsed_data)

    # Normalize all sections to have the same length
    for i in range(max_length):
        structured_list.append({
            key: parsed_data[key][i] if i < len(parsed_data[key]) else "No data available"
            for key in parsed_data
        })

    # Save to CSV
    save_to_csv(structured_list)
    print("Resume data saved to parsed_resumes.csv")
