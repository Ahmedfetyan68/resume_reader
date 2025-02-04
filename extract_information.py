import re
from utils import clean_text

# Expand job title pattern to capture more roles
JOB_TITLE_PATTERN = (
    r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*"
    r"(?:\s(Senior|Lead|Intern|Engineer|Manager|Analyst|Consultant|Developer|"
    r"Specialist|Director|Scientist|Owner|Sales|Software|Data|Product)){1,}"
)

def extract_experience(experience_section):
    """
    Extract structured experience data with position, company, and description.
    Uses JOB_TITLE_PATTERN to detect new positions, then everything else goes under 'Company' or 'Responsibilities'.
    """
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
    """
    Extract structured education data with university, degree, field, and basic year ranges (e.g., 2018–2022).
    If you also want month-year detection (e.g., 'Sep 2020 – Jun 2024'), see postprocess_education_dates below.
    """
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

        # Detect field of study
        elif re.search(
            r"(Computer Science|Engineering|Business|Information Technology|Marketing|Finance|"
            r"Accounting|Economics|Data Science)",
            line,
            re.IGNORECASE
        ):
            current_edu["Field"] = line

        # Detect years like 2018–2022 or 2018-2022 (digits only).
        # If your education includes month-year, you'll handle that with postprocess_education_dates below.
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
    Also strips out lines explicitly labeled as 'Skills:' or 'Technical:'.
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


# === Post-Processing Patterns & Functions ===

# For EXPERIENCE date ranges (month-year or 'Present')
DATE_PATTERN_EXPERIENCE = re.compile(
    r"("
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?\d{4}"
    r"|\d{4}"
    r"|Present"
    r")"
    r"\s?[–-]\s?"
    r"("
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?\d{4}"
    r"|\d{4}"
    r"|Present"
    r")",
    re.IGNORECASE
)

def postprocess_experience_dates(experiences):
    """
    For each experience entry, if there's a month-year or 'Present' date range
    in 'Position' like 'August 2022 – October 2022',
    extract it, then store it in 'Start Date'/'End Date',
    and remove it from the 'Position' text.
    """
    for exp in experiences:
        position = exp.get("Position", "")
        if position:
            match = DATE_PATTERN_EXPERIENCE.search(position)
            if match:
                exp["Start Date"] = match.group(1).strip()
                exp["End Date"] = match.group(2).strip()
                # Remove the date range from the Position text
                position_cleaned = DATE_PATTERN_EXPERIENCE.sub("", position).strip()
                exp["Position"] = position_cleaned
    return experiences


# OPTIONAL: If you also want to handle month-year + 'Present' in EDUCATION



def postprocess_education_dates(education_list):
 
    
    for edu in education_list:
        uni_text = edu.get("University", "")
        match = DATE_PATTERN_EXPERIENCE.search(uni_text)
        if match:
            edu["Start Year"] = match.group(1)
            edu["End Year"] = match.group(2)
            # Remove from the University text
            cleaned_uni = DATE_PATTERN_EXPERIENCE.sub("", uni_text).strip()
            edu["University"] = cleaned_uni
    return education_list

