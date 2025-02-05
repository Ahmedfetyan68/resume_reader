import re
from utils import clean_text

# ------------------------------
# Existing Extraction Functions
# ------------------------------

def extract_experience(experience_section):
    """Extract structured experience data with position, company, and description."""
    experiences = []
    current_experience = {}

    # Example job title pattern
    JOB_TITLE_PATTERN = (
        r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*"
        r"(?:\s(Senior|Lead|Intern|Engineer|Manager|Analyst|Consultant|Developer|"
        r"Specialist|Director|Scientist|Owner|Sales|Software|Data|Product)){1,}"
    )

    for line in experience_section:
        line = clean_text(line)
        if re.match(JOB_TITLE_PATTERN, line):
            if current_experience:
                experiences.append(current_experience)
                current_experience = {}
            current_experience["Position"] = line
        elif current_experience and "Company" not in current_experience:
            current_experience["Company"] = line
        else:
            if "Responsibilities" not in current_experience:
                current_experience["Responsibilities"] = []
            current_experience["Responsibilities"].append(line)

    if current_experience:
        experiences.append(current_experience)
    return experiences if experiences else ["No experience data found"]


def extract_education(education_section):
    """Extract structured education data with university, degree, field, and basic year ranges."""
    education_list = []
    current_edu = {}

    for line in education_section:
        line = clean_text(line)
        # Detect university/institution lines
        if re.match(
            r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*(?:\s(University|Academy|College|Institute|School|Polytechnic|Institute of Technology))",
            line,
        ):
            if current_edu:
                education_list.append(current_edu)
                current_edu = {}
            current_edu["University"] = line
        # Detect degree
        elif re.search(r"(Bachelor|Master|PhD|B\.Sc|BA|MA|MS|M\.Sc|MBA)", line, re.IGNORECASE):
            current_edu["Degree"] = line
        # Detect field
        elif re.search(
            r"(Computer Science|Engineering|Business|Information Technology|Marketing|Finance|Accounting|Economics|Data Science)",
            line,
            re.IGNORECASE,
        ):
            current_edu["Field"] = line
        # Detect year range (this may be further refined via postprocessing)
        elif re.search(r"\d{4}\s*[–-]\s*\d{4}", line):
            years = re.findall(r"\d{4}", line)
            if len(years) >= 1:
                current_edu["Start Year"] = years[0]
            if len(years) >= 2:
                current_edu["End Year"] = years[1]
            else:
                current_edu["End Year"] = "Present"

    if current_edu:
        education_list.append(current_edu)
    return education_list if education_list else ["No education data found"]


def extract_skills(skills_section):
    """
    Extracts a raw list of skills.
    (Postprocessing will remove headings and unwanted prefixes.)
    """
    skills = []
    for line in skills_section:
        line = clean_text(line)
        # Split by comma or semicolon
        parts = re.split(r"[,;]", line)
        for p in parts:
            p = p.strip()
            if p:
                skills.append(p)
    return skills if skills else ["No skills found"]


# ------------------------------
# Post-Processing Functions
# ------------------------------

# (A) Postprocess Dates for Experience
DATE_PATTERN_EXPERIENCE = re.compile(
    r"("  # Group(1): month-year, year-only, or Present
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?\d{4}|\d{4}|Present"
    r")\s?[–-]\s?("  # Group(2)
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?\d{4}|\d{4}|Present"
    r")",
    re.IGNORECASE,
)

def postprocess_experience_dates(experiences):
    """
    For each experience entry, if a date range is found in the 'Position' string,
    extract and remove it, storing in 'Start Date' and 'End Date'.
    """
    for exp in experiences:
        position = exp.get("Position", "")
        if position:
            match = DATE_PATTERN_EXPERIENCE.search(position)
            if match:
                exp["Start Date"] = match.group(1).strip()
                exp["End Date"] = match.group(2).strip()
                # Remove the matched date range from the position text
                exp["Position"] = DATE_PATTERN_EXPERIENCE.sub("", position).strip()
    return experiences


# (B) Postprocess Dates for Education
def postprocess_education_dates(education_list):
    # Using the same combined DATE_RANGE_PATTERN as for experience.
    DATE_PATTERN_EDU = re.compile(
        r"("  
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?\d{4}|\d{4}|Present"
        r")\s?[–-]\s?("
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?\d{4}|\d{4}|Present"
        r")",
        re.IGNORECASE,
    )
    for edu in education_list:
        uni_text = edu.get("University", "")
        if uni_text:
            match = DATE_PATTERN_EDU.search(uni_text)
            if match:
                edu["Start Date"] = match.group(1).strip()
                edu["End Date"] = match.group(2).strip()
                edu["University"] = DATE_PATTERN_EDU.sub("", uni_text).strip()
    return education_list


# (C) Postprocess Skills
def postprocess_skills(raw_skills):
    """
    Remove unwanted headings and prefixes from skills.
    For example, remove lines that are exactly 'Skills'
    and strip out prefixes like 'Languages:' or 'Technical:'.
    """
    cleaned = []
    unwanted_headings = {"skills"}  # case-insensitive

    for skill in raw_skills:
        skill_clean = skill.strip()
        if not skill_clean:
            continue
        if skill_clean.lower() in unwanted_headings:
            continue
        for prefix in ["Languages:", "Technical:", "Skills:"]:
            if prefix.lower() in skill_clean.lower():
                skill_clean = skill_clean.replace(prefix, "", 1).strip()
        cleaned.append(skill_clean)
    return cleaned


# (D) Postprocess Projects using Combined Heuristics
def postprocess_projects(raw_projects):
    """
    Convert a raw list of project lines into a structured list of dictionaries with Title and Description.
    This implementation uses combined heuristics:
      - Capitalization/Formatting: if most words are title-cased, it is likely a title.
      - Punctuation: lines ending with a period are more likely descriptions.
      - Keyword matching: lines starting with keywords like 'built', 'developed', etc., are treated as descriptions.
      - Also, it can accumulate consecutive description lines.
    """
    # Remove unwanted headings like 'Projects'
    unwanted_headings = {"projects"}
    filtered = [line.strip() for line in raw_projects if line.strip() and line.strip().lower() not in unwanted_headings]

    projects = []
    current_project = None

    # Define keywords often found at the beginning of a description
    description_keywords = {"built", "developed", "designed", "implemented", "created", "proposed", "managed", "coordinated"}

    for line in filtered:
        line_clean = line.strip()
        words = line_clean.split()
        # Heuristic: if the line is short or mostly title case, assume it is a title.
        is_title = False
        if len(words) < 5:
            is_title = True
        else:
            # Calculate the ratio of title-cased words
            title_cased = sum(1 for w in words if w.istitle())
            if title_cased / len(words) > 0.5:
                is_title = True

        # Heuristic: if the line ends with a period, treat it as description.
        if line_clean.endswith("."):
            is_title = False

        # Heuristic: if the first word (lowercased) is a known description keyword, mark as description.
        if words and words[0].lower() in description_keywords:
            is_title = False

        if is_title:
            # If there's an existing project, push it to the list.
            if current_project:
                projects.append(current_project)
            # Start a new project entry with this title.
            current_project = {"Title": line_clean, "Description": ""}
        else:
            # Otherwise, treat it as a description line.
            if current_project:
                # If there's already a description, append with newline.
                if current_project["Description"]:
                    current_project["Description"] += "\n" + line_clean
                else:
                    current_project["Description"] = line_clean
            else:
                # No title yet, so create a project with an empty title.
                current_project = {"Title": "", "Description": line_clean}

    if current_project:
        projects.append(current_project)

    return projects
