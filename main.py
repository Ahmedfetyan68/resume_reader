from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import uuid
from resume_parser import parse_resume  # Import your resume parser function

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Resume Parser API is running!"}

@app.post("/parse-resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Upload a resume (PDF) and get back JSON with parsed details.
    """

    # Generate a temporary file name
    file_extension = os.path.splitext(file.filename)[1].lower() or ".pdf"
    temp_filename = f"temp_{uuid.uuid4()}{file_extension}"
    temp_path = os.path.join("temp_files", temp_filename)

    # Create temp folder if not exists
    os.makedirs("temp_files", exist_ok=True)

    # Save the uploaded file
    with open(temp_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        # Parse the resume
        structured_data = parse_resume(temp_path)

        # Return structured JSON
        return JSONResponse(content=structured_data)

    finally:
        # Clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
