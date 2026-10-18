"""
CleanSlate - file_handler.py

Purpose:
- Handle CSV input and output only.
- Keep all file-related responsibilities in one place.

Responsibilities:
- Read CSV data into Python dictionaries
- Write cleaned data to cleaned_data.csv
- Write issues to error_report.csv

Important:
- This module should not contain validation logic.
- Validation logic belongs in validator.py.
- All file access should be safe and simple.
"""

import csv
from typing import List, Dict, Any

CSV_HEADERS = ["name", "email", "phone", "date_of_birth", "city"]


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """Read CSV file and return rows as a list of dictionaries.

    TODO:
    - Open file with newline="" to avoid blank lines.
    - Use csv.DictReader.
    - Validate header names.
    - Return a list of dicts.
    """
    rows: List[Dict[str, str]] = []

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                cleaned_row = {}
                for key in CSV_HEADERS:
                    cleaned_row[key] = (row.get(key) or "").strip()
                rows.append(cleaned_row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    return rows


def write_csv(file_path: str, rows: List[Dict[str, Any]]) -> None:
    """Write list of dictionaries to a CSV file.

    TODO:
    - Use csv.DictWriter.
    - Write the header row.
    - Ensure rows are serializable.
    """
    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def export_cleaned_records(file_path: str, rows: List[Dict[str, Any]]) -> None:
    """Write cleaned records to a CSV file.

    TODO:
    - Use write_csv() and pass cleaned rows.
    """
    write_csv(file_path, rows)


def export_error_report(file_path: str, rows: List[Dict[str, Any]]) -> None:
    """Write validation issues to CSV.

    TODO:
    - Decide which columns to include:
      index, name, email, phone, date_of_birth, city, issues
    """
    write_csv(file_path, rows)


if __name__ == "__main__":
    print("file_handler.py loaded. This file is ready to read/write CSV data.")
