import csv
from pathlib import Path

from validator import REQUIRED_FIELDS

REQUIRED_COLUMNS = REQUIRED_FIELDS


def read_csv(file_path):
    """Read a CSV file and verify that all required column headers exist."""
    path = Path(file_path)
    records = []

    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or missing a header row.")

        # Remove accidental spaces around header names.
        reader.fieldnames = [name.strip() if name else "" for name in reader.fieldnames]

        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("CSV contains duplicate column names.")

        missing = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

        for row_number, row in enumerate(reader, start=2):
            # Ignore completely blank lines.
            if not row or all(value is None or not str(value).strip() for value in row.values()):
                continue
            if None in row:
                raise ValueError(f"Row {row_number} contains extra values.")
            records.append({field: row.get(field, "") or "" for field in REQUIRED_COLUMNS})

    return records


def write_cleaned_csv(records, file_path):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(records)


def write_error_report(errors, file_path):
    headers = ["row", "field", "problem"]
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(errors)
