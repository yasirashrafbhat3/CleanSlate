import unittest
from validator import (
    clean_record,
    detect_duplicates,
    is_valid_dob,
    is_valid_email,
    is_valid_phone,
    process_records,
)


class ValidatorTests(unittest.TestCase):
    def test_email_validation(self):
        self.assertTrue(is_valid_email("person@example.com"))
        self.assertFalse(is_valid_email("person@@example.com"))

    def test_phone_validation(self):
        self.assertTrue(is_valid_phone("9876543210"))
        self.assertFalse(is_valid_phone("12345"))

    def test_dob_validation(self):
        self.assertTrue(is_valid_dob("2002-04-12"))
        self.assertFalse(is_valid_dob("2035-01-01"))
        self.assertFalse(is_valid_dob("2023-02-30"))
        self.assertFalse(is_valid_dob("12-04-2002"))

    def test_cleaning(self):
        record = {
            "name": "  ali khan  ",
            "email": " ALI@GMAIL.COM ",
            "phone": "9876543210",
            "date_of_birth": "2002-04-12",
            "city": " srinagar ",
        }
        cleaned = clean_record(record)
        self.assertEqual(cleaned["name"], "Ali Khan")
        self.assertEqual(cleaned["email"], "ali@gmail.com")
        self.assertEqual(cleaned["city"], "Srinagar")

    def test_duplicate_email(self):
        records = [
            {"name": "A", "email": "a@example.com", "phone": "", "date_of_birth": "", "city": ""},
            {"name": "B", "email": " A@EXAMPLE.COM ", "phone": "", "date_of_birth": "", "city": ""},
        ]
        duplicates = detect_duplicates(records)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]["row"], 3)

    def test_process_records_reports_issues(self):
        records = [{
            "name": "",
            "email": "bad@@email",
            "phone": "123",
            "date_of_birth": "2035-01-01",
            "city": "Delhi",
        }]
        cleaned, errors = process_records(records)
        self.assertEqual(len(cleaned), 1)
        self.assertGreaterEqual(len(errors), 4)


if __name__ == "__main__":
    unittest.main()
