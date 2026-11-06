# CleanSlate
## Data Validation and Cleansing Utility

### 1. Project Overview
CleanSlate is a menu-driven Python console application that checks customer records stored in CSV files. It identifies common data-quality problems, standardises safe formatting issues, detects repeated email addresses, and exports a cleaned copy together with an error report.

### 2. Problem Statement
Customer datasets often contain missing fields, incorrectly formatted email addresses, invalid phone numbers, impossible or future dates, duplicate entries, and inconsistent spacing or capitalisation. These issues reduce data reliability and make later analysis difficult. Manually checking large CSV files is time-consuming and error-prone.

### 3. Proposed Solution
CleanSlate automates basic data-quality checks on CSV records. It reads the input, creates standardised copies of records, validates required fields and formats, flags repeated email addresses, and generates two output files:
- `cleaned_data.csv`: standardised records, retaining all input rows.
- `error_report.csv`: row number, field name, and description of each detected issue.

### 4. Objectives
- Read structured customer data from CSV files.
- Check required fields for missing values.
- Validate basic email syntax, Indian mobile number format, and date of birth.
- Detect repeated non-empty email addresses.
- Trim extra spaces and standardise names, cities, and email case.
- Export processed records and a detailed issue report.

### 5. Main Features
1. **CSV input:** loads a user-selected CSV file; Enter uses `sample_data.csv`.
2. **Missing-field detection:** reports blank name, email, phone, date of birth, or city.
3. **Email validation:** checks basic email syntax.
4. **Phone validation:** expects a 10-digit Indian mobile number beginning with 6, 7, 8, or 9.
5. **Date validation:** expects `YYYY-MM-DD`, a real calendar date, and a date that is not in the future.
6. **Duplicate detection:** flags later records that reuse a normalised, non-empty email address.
7. **Data cleansing:** trims surrounding whitespace, title-cases names and cities, and lowercases email addresses.
8. **CSV export:** writes the standardised records and a separate error report.

### 6. System Workflow
1. Start the application.
2. Load `sample_data.csv` or enter another CSV path.
3. Validate and clean the loaded records.
4. View duplicate entries and the full error report.
5. Export `cleaned_data.csv` and `error_report.csv`.
6. Exit the application.

### 7. Technology Stack
- Python 3
- `csv` for reading and writing CSV files
- `re` for basic format validation
- `datetime` for date validation
- `unittest` for automated tests
- VS Code and Git/GitHub for development and version control

No third-party Python packages or database are required.

### 8. Project Structure
```text
CleanSlate/
├── main.py
├── validator.py
├── file_handler.py
├── sample_data.csv
├── tests/
│   ├── test_cases.md
│   └── test_validator.py
├── README.md
└── .gitignore
```

The application generates `cleaned_data.csv` and `error_report.csv` when export is selected.

### 9. Validation Rules and Limitations
- Email validation checks syntax only; it cannot confirm that an email inbox exists.
- Phone validation follows a basic Indian 10-digit mobile-number rule.
- Date of birth must be a valid past date in `YYYY-MM-DD` format.
- Duplicate detection uses normalised email addresses as the matching key. It flags possible duplicate records but does not delete them.
- All input rows are retained in the cleaned output. Problems are described in the error report; invalid records are not silently removed.
- Name and city title-casing is a simple standardisation rule and may not preserve every person's preferred spelling.

### 10. How to Run
1. Install Python 3.
2. Open the project folder in a terminal.
3. Run:
   ```bash
   python3 main.py
   ```
4. Follow the numbered menu.
5. To run automated tests:
   ```bash
   python3 -m unittest discover -s tests -v
   ```

### 11. Testing
The test suite checks email, phone, and date validation; formatting cleanup; duplicate email detection; and combined record processing. Additional manual CSV test cases are documented in `tests/test_cases.md`.

### 12. Team Contributions
This project is developed collaboratively by two team members. Record the actual contribution of each member here before submission:
- **Yasir Ashraf Bhat:** validation, cleansing, duplicate detection, integration, and testing.
- **Sostika Yadav:** CSV file handling, sample data, test-case documentation, and integration support.

Update these descriptions if the actual division of work changes.

### 13. Future Scope
- Support configurable validation rules for different countries.
- Add more duplicate-matching options beyond email.
- Provide a summary report with issue counts by category.
- Support larger datasets and additional file formats.
- Add optional data-quality scoring.

### 14. Project Scope
CleanSlate is a command-line academic capstone project. It does not require a graphical interface, website, cloud service, or database.
