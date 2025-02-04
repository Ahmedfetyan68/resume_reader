import re

def identify_sections(resume_text):
    """Identify sections like Experience, Education, Skills, Projects, and optionally Languages."""
    sections = {
        "Experience": [],
        "Education": [],
        "Skills": [],
        "Projects": [],
        "Extracurricular Activities": [],
        "Languages": [],
        "General": []
    }

    # Updated regex patterns for section headers
    section_patterns = {
        "Experience": re.compile(r"(?i)\b(experience|work history|employment|professional background)\b"),
        "Education": re.compile(r"(?i)\b(education|academic background|certifications|degrees|studies)\b"),
        "Skills": re.compile(r"(?i)\b(skills|technologies|competencies|expertise|technical skills)\b"),
        "Projects": re.compile(r"(?i)\b(projects|portfolio|work samples|case studies)\b"),
        "Extracurricular Activities": re.compile(r"(?i)\b(activities|clubs|volunteering|organizations|leadership)\b"),
        "Languages": re.compile(r"(?i)\b(languages|spoken languages|fluency|proficiency)\b")
    }

    current_section = "General"
    for line in resume_text.split("\n"):
        line = line.strip()
        for section, pattern in section_patterns.items():
            if pattern.search(line):
                print(f"Detected Section: {section}")  # Debug print
                current_section = section
                break
        sections[current_section].append(line)

    # Debugging: Print first 5 lines of each section
    print("\n==== Debugging Extracted Sections ====")
    for sec, content in sections.items():
        print(f"\n{sec} (First 5 lines):")
        print("\n".join(content[:5]))
        print("-" * 40)

    return sections
