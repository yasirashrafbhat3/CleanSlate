import re
from datetime import date, datetime

REQUIRED_FIELDS = ["name", "email", "phone", "date_of_birth", "city"]
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_PATTERN = re.compile(r"^[6-9][0-9]{9}$")


def is_valid_email(email):
    """Check basic email syntax; this does not verify that a mailbox exists."""
    return bool(EMAIL_PATTERN.fullmatch((email or "").strip()))


def is_valid_phone(phone):
    """Check a 10-digit Indian mobile number beginning with 6, 7, 8 or 9."""
    return bool(PHONE_PATTERN.fullmatch((phone or "").strip()))


def is_valid_dob(dob):
    """Accept YYYY-MM-DD dates that are valid calendar dates and not in the future."""
    value = (dob or "").strip()
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
        # Enforce exact ISO formatting, not just a parseable date.
        return parsed.isoformat() == value and parsed <= date.today()
    except ValueError:
        return False


def clean_record(record):
    """Return a standardised copy; the original input dictionary is not modified."""
    cleaned = {}
    for field in REQUIRED_FIELDS:
        value = (record.get(field) or "").strip()
        if field in ("name", "city"):
            cleaned[field] = value.title()
        elif field == "email":
            cleaned[field] = value.lower()
        else:
            cleaned[field] = value
    return cleaned


def validate_record(record, row_number):
    errors = []

    for field in REQUIRED_FIELDS:
        value = (record.get(field) or "").strip()
        if not value:
            errors.append({
                "row": row_number,
                "field": field,
                "problem": f"{field} is missing",
            })

    email = (record.get("email") or "").strip()
    if email and not is_valid_email(email):
        errors.append({
            "row": row_number,
            "field": "email",
            "problem": "Invalid email address",
        })

    phone = (record.get("phone") or "").strip()
    if phone and not is_valid_phone(phone):
        errors.append({
            "row": row_number,
            "field": "phone",
            "problem": "Invalid Indian mobile number (expected 10 digits starting 6-9)",
        })

    dob = (record.get("date_of_birth") or "").strip()
    if dob and not is_valid_dob(dob):
        errors.append({
            "row": row_number,
            "field": "date_of_birth",
            "problem": "Invalid date or future date of birth (expected YYYY-MM-DD)",
        })

    return errors


def detect_duplicates(records):
    """Flag later records that reuse a non-empty normalised email address."""
    seen_emails = set()
    duplicates = []

    for row_number, record in enumerate(records, start=2):
        email = clean_record(record)["email"]
        if email and email in seen_emails:
            duplicates.append({
                "row": row_number,
                "field": "email",
                "problem": "Duplicate email address / possible duplicate record",
            })
        elif email:
            seen_emails.add(email)

    return duplicates


def process_records(records):
    cleaned_records = []
    errors = []

    for row_number, record in enumerate(records, start=2):
        cleaned = clean_record(record)
        cleaned_records.append(cleaned)
        errors.extend(validate_record(cleaned, row_number))

    errors.extend(detect_duplicates(records))
    return cleaned_records, errors
