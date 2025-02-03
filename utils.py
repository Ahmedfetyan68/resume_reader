# utils.py
def clean_text(text):
    """Replace special characters like bullet points and fix encoding issues."""
    text = text.replace("•", "*").replace("ΓÇó", "*").strip()
    return text
