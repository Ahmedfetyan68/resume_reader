import re
from utils import clean_text



def extract_experience(experience_section):
    """Extract structured experience data with position, company, and description."""
    experiences = []
    current_experience = {}

    for line in experience_section:
        line = clean_text(line)  # Clean text
        
        # Detect Job Title (Capitalized & contains job-related words)
        if re.match(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s(?:Intern|Engineer|Manager|Analyst|Consultant|Developer|Specialist)", line):
            # If a new job is found, save the previous one
            if current_experience:
                experiences.append(current_experience)
                current_experience = {}

            current_experience["Position"] = line
        
        # Detect Company Name (Usually follows job title)
        elif current_experience and "Company" not in current_experience:
            current_experience["Company"] = line
        
        # Detect Responsibilities / Description
        else:
            if "Responsibilities" not in current_experience:
                current_experience["Responsibilities"] = []
            current_experience["Responsibilities"].append(line)
    
    # Append last job entry
    if current_experience:
        experiences.append(current_experience)
    
    return experiences if experiences else ["No experience data found"]

def extract_education(education_section):
    """Extract structured education data with university, degree, field, and dates."""
    education_list = []
    current_edu = {}

    for line in education_section:
        line = clean_text(line)  # Clean text

        # Detect University Name (Capitalized Words + Common University Terms)
        if re.match(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s(?:University|Academy|College|Institute|School)", line):
            if current_edu:
                education_list.append(current_edu)
                current_edu = {}

            current_edu["University"] = line

        # Detect Degree
        elif "Bachelor" in line or "Master" in line or "PhD" in line:
            current_edu["Degree"] = line

        # Detect Field of Study
        elif "Computer Science" in line or "Engineering" in line or "Business" in line:
            current_edu["Field"] = line

        # Detect Years
        elif re.search(r"\d{4} – \d{4}", line):
            years = re.findall(r"\d{4}", line)
            current_edu["Start Year"] = years[0]
            current_edu["End Year"] = years[1] if len(years) > 1 else "Present"

    # Append last education entry
    if current_edu:
        education_list.append(current_edu)

    return education_list if education_list else ["No education data found"]

def extract_skills(skills_section):
    """Extracts a clean list of skills."""
    skills = []

    for line in skills_section:
        line = clean_text(line)
        if "Skills:" not in line and "Technical:" not in line:
            skills.extend(line.split(","))  # Split by commas

    return [skill.strip() for skill in skills if skill] or ["No skills found"]
