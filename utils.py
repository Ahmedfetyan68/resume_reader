def clean_text(text):
    """
    Fix encoding issues and remove unwanted characters from text.
    Also normalizes common bullet points.
    """
    if isinstance(text, dict):  # Prevents breaking structured data
        return text

    return (
        str(text)
        .replace("ΓÇó", "*")
        .replace("╬ô├ç├│", "*")
        .replace("\u2022", "*")      # Bullet
        .replace("\uf0b7", "*")      # Additional bullet
        .replace("•", "*")          # Another bullet
        .strip()
    )
