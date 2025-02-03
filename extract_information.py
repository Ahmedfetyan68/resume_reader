import re

def extract_personal_info(general_section):
    """Extracts name, email, and phone number from the general information section."""
    name, email, phone = None, None, None

    for line in general_section:
        line = line.strip()

        # Skip empty lines
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


def extract_experience(experience_section):
    """Extracts work experience details."""
    jobs = []
    current_job = {}

    for i, line in enumerate(experience_section):
        line = line.strip()
        if not line or line.startswith("•") or line.startswith("-"):
            continue

        # ✅ Various job formats (Title | Company | Year)
        match = re.match(r"(?P<title>.+?) at (?P<company>.+?) \((?P<start>\d{4})-(?P<end>\d{4}|Present)\)", line)
        if match:
            jobs.append({
                "Position": match.group("title"),
                "Company": match.group("company"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Handle missing company names
        if current_job and current_job.get("Company") == "Unknown":
            current_job["Company"] = line.strip()
            jobs.append(current_job)
            current_job = {}

    if current_job:
        jobs.append(current_job)

    return jobs if jobs else ["No experience data found"]


def extract_education(education_section):
    """Extracts education details."""
    degrees = []
    current_education = {}

    for line in education_section:
        line = line.strip()
        if not line or line.startswith("•") or line.startswith("-"):
            continue

        # ✅ Education formats
        match = re.match(r"(?P<university>.+?) (?P<start>\d{4})\s?[–|-]?\s?(?P<end>\d{4}|Present)?", line)
        if match:
            if current_education:
                degrees.append(current_education)
            current_education = {
                "University": match.group("university"),
                "Degree": "Unknown",
                "Field": "Unknown",
                "Start Year": match.group("start"),
                "End Year": match.group("end") or "Present"
            }
            continue

    if current_education:
        degrees.append(current_education)

    return degrees if degrees else ["No education data found"]
    """Extract education details with multiple fallback formats."""
    degrees = []
    current_education = {}

    print("\n==== Debugging Education Extraction ====")
    print(f"Education Section Received: {education_section}")

    for line in education_section:
        line = line.strip()

        # Skip empty lines and bullet points
        if not line or line.startswith("•") or line.startswith("-"):
            continue

        # ✅ Pattern 1: "B.Sc in Computer Science, MIT (2019-2023)"
        match = re.match(r"(?P<degree>.+?) in (?P<field>.+?), (?P<university>.+?) \((?P<start>\d{4})-(?P<end>\d{4}|Present)\)", line)
        if match:
            degrees.append({
                "University": match.group("university"),
                "Degree": match.group("degree"),
                "Field": match.group("field"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 2: "MIT, Bachelor of Science in Computer Science (2019-2023)"
        match = re.match(r"(?P<university>.+?), (?P<degree>.+?) (?P<field>.+?) \((?P<start>\d{4})-(?P<end>\d{4}|Present)\)", line)
        if match:
            degrees.append({
                "University": match.group("university"),
                "Degree": match.group("degree"),
                "Field": match.group("field"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 3: "Arab Academy for Science, Technology & Maritime Transport 2019 – 2023"
        match = re.match(r"(?P<university>.+?) (?P<start>\d{4})\s?[–|-]?\s?(?P<end>\d{4}|Present)?", line)
        if match:
            if current_education:
                degrees.append(current_education)  # Save previous entry before adding a new one
            current_education = {
                "University": match.group("university"),
                "Degree": "Unknown",
                "Field": "Unknown",
                "Start Year": match.group("start"),
                "End Year": match.group("end") or "Present"
            }
            continue

        # ✅ If a degree is detected, associate it with the last detected university
        if current_education and "Degree" in current_education and current_education["Degree"] == "Unknown":
            current_education["Degree"] = line.strip()
            continue

    if current_education:
        degrees.append(current_education)

    print("Extracted Education:", degrees)
    return degrees if degrees else ["No education data found"]

    """Extract education details with multiple fallback formats."""
    degrees = []
    current_education = {}

    print("\n==== Debugging Education Extraction ====")
    print(f"Education Section Received: {education_section}")

    for line in education_section:
        line = line.strip()

        # Skip empty lines and bullet points
        if not line or line.startswith("•") or line.startswith("-"):
            continue

        # ✅ Pattern 1: "B.Sc in Computer Science, MIT (2019-2023)"
        match = re.match(r"(?P<degree>.+?) in (?P<field>.+?), (?P<university>.+?) \((?P<start>\d{4})-(?P<end>\d{4}|Present)\)", line)
        if match:
            degrees.append({
                "University": match.group("university"),
                "Degree": match.group("degree"),
                "Field": match.group("field"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 2: "MIT, Bachelor of Science in Computer Science (2019-2023)"
        match = re.match(r"(?P<university>.+?), (?P<degree>.+?) (?P<field>.+?) \((?P<start>\d{4})-(?P<end>\d{4}|Present)\)", line)
        if match:
            degrees.append({
                "University": match.group("university"),
                "Degree": match.group("degree"),
                "Field": match.group("field"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 3: "Arab Academy for Science, Technology & Maritime Transport 2019 – 2023"
        match = re.match(r"(?P<university>.+?) (?P<start>\d{4})\s?[–|-]?\s?(?P<end>\d{4}|Present)?", line)
        if match:
            if current_education:
                degrees.append(current_education)  # Save previous entry before adding a new one
            current_education = {
                "University": match.group("university"),
                "Degree": "Unknown",
                "Field": "Unknown",
                "Start Year": match.group("start"),
                "End Year": match.group("end") or "Present"
            }
            continue

        # ✅ If a degree is detected, associate it with the last detected university
        if current_education and "Degree" in current_education and current_education["Degree"] == "Unknown":
            current_education["Degree"] = line.strip()
            continue

    if current_education:
        degrees.append(current_education)

    print("Extracted Education:", degrees)
    return degrees if degrees else ["No education data found"]

def extract_skills(skills_section):
    """Extract skills as a list."""
    skills = [skill.strip() for skill in ", ".join(skills_section).split(",") if skill]
    return skills or ["No skills data found"]
