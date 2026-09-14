from pathlib import Path
import pandas as pd


def load_requirements(file_path):
    """Load and validate requirements from an Excel file."""

    df = pd.read_excel(file_path)

    required_columns = [
        "Requirement_ID",
        "Requirement_Text",
        "Parent_ID",
        "Verification_Method"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = df.fillna("")

    return df


if __name__ == "__main__":

    # Find the project root directory
    project_root = Path(__file__).resolve().parent.parent

    # Build the path to the Excel file
    requirements_file = project_root / "Data" / "Requirements.xlsx"

    requirements = load_requirements(requirements_file)

    print("Requirements loaded successfully!")
    print(f"Number of requirements: {len(requirements)}")
    print()
    print(requirements)