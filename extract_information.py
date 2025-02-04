import re
from utils import clean_text

# Expand job title pattern to capture more roles 
JOB_TITLE_PATTERN = (
    r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*"
    r"(?:\s(Senior|Lead|Intern|Engineer|Manager|Analyst|Consultant|Developer|"
    r"Specialist|Director|Scientist|Owner|Sales|Software|Data|Product)){1,}"
)

def extract_experience(experience_section):
    """Extract structured experience data with position, company, and description."""
    experiences = []
    current_experience = {}

    for line in experience_section:
        line = clean_text(line)

        # Detect job title
        if re.match(JOB_TITLE_PATTERN, line):
            # If we've already been tracking an experience, finalize it
            if current_experience:
                experiences.append(current_experience)
                current_experience = {}
            current_experience["Position"] = line

        # Detect company name (usually follows job title)
        elif current_experience and "Company" not in current_experience:
            current_experience["Company"] = line

        # Otherwise, treat as responsibilities/description
        else:
            if "Responsibilities" not in current_experience:
                current_experience["Responsibilities"] = []
            current_experience["Responsibilities"].append(line)

    # Append last experience if present
    if current_experience:
        experiences.append(current_experience)

    return experiences if experiences else ["No experience data found"]


def extract_education(education_section):
    """Extract structured education data with university, degree, field, and dates."""
    education_list = []
    current_edu = {}

    for line in education_section:
        line = clean_text(line)

        # Detect a university or similar institution name
        if re.match(
            r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*(?:\s(University|Academy|College|Institute|School|Polytechnic|"
            r"Institute of Technology))", line
        ):
            # If we were already collecting an education block, store it and start a new one
            if current_edu:
                education_list.append(current_edu)
                current_edu = {}
            current_edu["University"] = line

        # Detect degree (e.g., Bachelor, Master, PhD, B.Sc, etc.)
        elif re.search(r"(Bachelor|Master|PhD|B\.Sc|BA|MA|MS|M\.Sc|MBA)", line, re.IGNORECASE):
            current_edu["Degree"] = line

        # Detect field of study (expanding beyond the original 3)
        elif re.search(r"(Computer Science|Engineering|Business|Information Technology|Marketing|Finance|"
                       r"Accounting|Economics|Data Science)", line, re.IGNORECASE):
            current_edu["Field"] = line

        # Detect years like 2018–2022 or 2018-2022
        elif re.search(r"\d{4}\s*[–-]\s*\d{4}", line):
            years = re.findall(r"\d{4}", line)
            if len(years) >= 1:
                current_edu["Start Year"] = years[0]
            if len(years) >= 2:
                current_edu["End Year"] = years[1]
            else:
                current_edu["End Year"] = "Present"

    # Append last education entry if present
    if current_edu:
        education_list.append(current_edu)

    return education_list if education_list else ["No education data found"]


def extract_skills(skills_section):
    """
    Extracts a clean list of skills, merging lines by commas or semicolons.
    Also strips out lines explicitly labeled as "Skills:" or "Technical:".
    """
    skills = []

    for line in skills_section:
        line = clean_text(line)

        # Remove explicit headings
        if "Skills:" in line or "Technical:" in line:
            line = line.replace("Skills:", "").replace("Technical:", "")

        # Split by comma or semicolon
        parts = re.split(r"[,;]", line)
        for p in parts:
            p = p.strip()
            if p:
                skills.append(p)

    return skills if skills else ["No skills found"]
