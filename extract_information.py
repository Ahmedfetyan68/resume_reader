import re

import re

import re

import re

import re

def extract_experience(experience_section):
    """Extract work experience details with multiple fallback formats."""
    jobs = []
    current_job = {}

    print("\n==== Debugging Experience Extraction ====")
    print(f"Experience Section Received: {experience_section}")

    for i, line in enumerate(experience_section):
        line = line.strip()

        # Skip empty lines and bullet points
        if not line or line.startswith("•") or line.startswith("-"):
            continue

        # ✅ Pattern 1: "Software Engineer at Google (2021-Present)"
        match = re.match(r"(?P<title>.+?) at (?P<company>.+?) \((?P<start>\d{4})-(?P<end>\d{4}|Present)\)", line)
        if match:
            jobs.append({
                "Position": match.group("title"),
                "Company": match.group("company"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 2: "Software Engineer, Google (2021-Present)"
        match = re.match(r"(?P<title>.+?), (?P<company>.+?) \((?P<start>\d{4})-(?P<end>\d{4}|Present)\)", line)
        if match:
            jobs.append({
                "Position": match.group("title"),
                "Company": match.group("company"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 3: "Software Engineer | Google | 2021-Present"
        match = re.match(r"(?P<title>.+?) \| (?P<company>.+?) \| (?P<start>\d{4})-(?P<end>\d{4}|Present)", line)
        if match:
            jobs.append({
                "Position": match.group("title"),
                "Company": match.group("company"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 4: "Google - Software Engineer - 2021 to Present"
        match = re.match(r"(?P<company>.+?) - (?P<title>.+?) - (?P<start>\d{4}) to (?P<end>\d{4}|Present)", line)
        if match:
            jobs.append({
                "Position": match.group("title"),
                "Company": match.group("company"),
                "Start Year": match.group("start"),
                "End Year": match.group("end")
            })
            continue

        # ✅ Pattern 5: "Application Support Engineer D365 Present" (No explicit date)
        match = re.match(r"(?P<title>.+?)\s+(?P<start>\d{4})?\s?(Present|\d{4})?", line)
        if match:
            current_job = {
                "Position": match.group("title"),
                "Company": "Unknown",
                "Start Year": match.group("start") or "Unknown",
                "End Year": match.group(3) or "Present"
            }
            continue

        # ✅ Handle case where the company appears **AFTER** the job title
        if current_job and current_job.get("Company") == "Unknown":
            current_job["Company"] = line.strip()
            jobs.append(current_job)
            current_job = {}

    if current_job:
        jobs.append(current_job)

    print("Extracted Experience:", jobs)
    return jobs if jobs else ["No experience data found"]

def extract_education(education_section):
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
