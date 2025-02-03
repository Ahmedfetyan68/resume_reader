import pandas as pd

def save_to_csv(parsed_data, output_csv="parsed_resumes.csv"):
    """Save structured resume data to a CSV file."""
    df = pd.DataFrame(parsed_data)
    df.to_csv(output_csv, index=False)
    print(f"Resume data saved to {output_csv}")
