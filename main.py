from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import uuid

# Import your existing parse_resume function (adjust the import path as needed)
from resume_parser import parse_resume

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Resume Parser API is running!"}

@app.post("/parse-resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Upload a resume (PDF or DOCX) and get back JSON with parsed details.
    """
    # 1) Generate a temporary file path
    file_extension = os.path.splitext(file.filename)[1].lower() or ".pdf"
    temp_filename = f"temp_{uuid.uuid4()}{file_extension}"
    temp_path = os.path.join("temp_files", temp_filename)

    # 2) Save the uploaded file to a temp folder
    #    (Create 'temp_files/' folder if it doesn't exist)
    os.makedirs("temp_files", exist_ok=True)
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        # 3) Parse the resume with your existing function
        structured_data, sections = parse_resume(temp_path)

        # 4) Return the parsed data as JSON
        return JSONResponse(content=structured_data)

    finally:
        # 5) Optionally clean up (delete) the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
