def clean_text(text):
    """Fix encoding issues and remove unwanted characters from text."""
    if isinstance(text, dict):  # Prevents breaking structured data
        return text
    return (
        text.replace("ΓÇó", "*")
        .replace("╬ô├ç├│", "*")
        .replace("\u2022", "*")  # Handles bullet points
        .strip()
    )
