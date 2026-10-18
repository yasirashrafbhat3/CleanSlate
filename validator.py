"""
CleanSlate - validator.py

Purpose:
- Validate CSV records.
- Detect duplicate records.
- Clean messy values such as extra spaces and inconsistent case.
- Return structured issues for reporting.

Responsibilities:
- Email validation
- Phone validation
- Date of birth validation
- Text normalization and cleaning
- Duplicate detection
- Reporting of issues

Important:
- This file should stay focused on business logic.
- CSV reading/writing belongs in file_handler.py.
- This is only a starter and should not be a full implementation yet.
"""

import re
from datetime import datetime
from typing import Dict, List, Any

# TODO: Add more patterns if needed.
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^\\+?[0-9\\s\\-()]{7,20}$")
EXPECTED_FIELDS = ["name", "email", "phone", "date_of_birth", "city"]


def normalize_text(value: Any) -> str:
    """Return trimmed and standardized string text.

    TODO:
    - Strip leading/trailing spaces.
    - Convert to a consistent case if the project decides to.
    - Handle None or non-string values safely.
    """
    if value is None:
        return ""
    return str(value).strip()


def normalize_for_comparison(value: Any) -> str:
    """Convert text into a safe version for duplicate checks.

    Example:
    ' Alice Smith ' -> 'alice smith'
    'ALICE SMITH' -> 'alice smith'
    """
    return normalize_text(value).lower()


def is_valid_email(email: str) -> bool:
    """Return True if the email looks valid.

    TODO:
    - Implement robust regex or simple checks.
    - Decide whether to allow uppercase letters and plus signs.
    """
    if not email:
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))


def is_valid_phone(phone: str) -> bool:
    """Return True if the phone number looks valid.

    TODO:
    - Decide allowed formats.
    - Remove spaces, dashes, parentheses before checking if you want.
    - Keep it beginner-friendly and simple.
    """
    if not phone:
        return False
    cleaned = phone.strip()
    return bool(PHONE_PATTERN.match(cleaned))


def is_valid_date_of_birth(date_of_birth: str) -> bool:
    """Return True if date_of_birth is a valid date string.

    TODO:
    - Decide if dates should be in YYYY-MM-DD only.
    - Use datetime.strptime for validation.
    - Reject impossible dates like 2025-02-30.
    """
    value = normalize_text(date_of_birth)
    if not value:
        return False

    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def clean_record(record: Dict[str, str]) -> Dict[str, str]:
    """Clean a single record by trimming spaces and standardising text.

    TODO:
    - Trim whitespace from all fields.
    - Standardize name and city capitalization.
    - Decide whether to keep lower/upper case rules consistent.
    - Apply only safe transformations.
    """
    cleaned = {}
    for field in EXPECTED_FIELDS:
        value = record.get(field, "")
        cleaned[field] = normalize_text(value)

    # TODO: Standardize case for name and city:
    # cleaned["name"] = cleaned["name"].title()
    # cleaned["city"] = cleaned["city"].title()

    return cleaned


def validate_record(record: Dict[str, str]) -> Dict[str, Any]:
    """Validate one record and return results.

    The result should include:
    - cleaned_record
    - issues
    - is_valid
    """
    cleaned = clean_record(record)

    issues: List[str] = []
    errors: Dict[str, str] = {}

    # Validate name
    if not cleaned.get("name"):
        issues.append("Missing name")
        errors["name"] = "required"

    # Validate email
    if not is_valid_email(cleaned.get("email", "")):
        issues.append("Invalid email")
        errors["email"] = "invalid"

    # Validate phone
    if not is_valid_phone(cleaned.get("phone", "")):
        issues.append("Invalid phone number")
        errors["phone"] = "invalid"

    # Validate date of birth
    if not is_valid_date_of_birth(cleaned.get("date_of_birth", "")):
        issues.append("Invalid date of birth")
        errors["date_of_birth"] = "invalid"

    # Validate city
    if not cleaned.get("city"):
        issues.append("Missing city")
        errors["city"] = "required"

    return {
        "cleaned_record": cleaned,
        "issues": issues,
        "errors": errors,
        "is_valid": len(issues) == 0,
    }


def find_duplicate_records(records: List[Dict[str, str]]) -> List[int]:
    """Return indexes of duplicate rows based on a normalized key.

    TODO:
    - Decide the duplicate rule.
    - Common simple strategy: compare normalized name + email + phone.
    - Keep this simple for beginners.
    """
    seen = {}
    duplicates = []

    for index, record in enumerate(records):
        cleaned = clean_record(record)
        key = (
            normalize_for_comparison(cleaned.get("name", "")) + "|" +
            normalize_for_comparison(cleaned.get("email", "")) + "|" +
            normalize_for_comparison(cleaned.get("phone", ""))
        )
        if key in seen:
            duplicates.append(index)
        else:
            seen[key] = index

    return duplicates


def detect_duplicate_records(records: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Return duplicate record details.

    TODO:
    - Return a list of duplicate entries with indexes.
    - Include the original record and a duplicate reason.
    - This is useful when exporting error_report.csv.
    """
    duplicate_indexes = find_duplicate_records(records)

    result = []
    for idx in duplicate_indexes:
        result.append({
            "index": idx,
            "reason": "Duplicate record detected",
            "record": records[idx]
        })

    return result


# Example starter usage:
if __name__ == "__main__":
    sample = {
        "name": " Alice Smith ",
        "email": "alice@example.com",
        "phone": "+1 (202) 555-0135",
        "date_of_birth": "1990-05-21",
        "city": "  new york  "
    }

    validation_result = validate_record(sample)
    print("Sample validation result:")
    print(validation_result)
