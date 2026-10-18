# CleanSlate

CleanSlate is a beginner-friendly Python project for data validation and cleansing. It reads CSV records, checks whether fields are valid, finds duplicates, cleans messy values, and exports the results.

## Project goal
The project helps users learn Python while building a simple console-based tool that:
- Reads CSV files
- Validates names, emails, phone numbers, and dates of birth
- Detects duplicate records
- Cleans extra spaces and inconsistent text case
- Exports cleaned rows and detected issues

## Features
1. Read CSV records with name, email, phone, date_of_birth, and city
2. Detect invalid email addresses
3. Detect invalid phone numbers
4. Detect invalid dates of birth
5. Detect duplicate records
6. Trim extra spaces and standardize text
7. Export cleaned records to cleaned_data.csv
8. Export issues to error_report.csv

## Folder structure
```text
CleanSlate/
├── main.py
├── validator.py
├── file_handler.py
├── sample_data.csv
├── tests/
│   └── test_cases.md
├── README.md
└── .gitignore
```

## What each file does
- main.py: menu-driven console interface
- validator.py: validation, duplicate detection, and cleaning
- file_handler.py: CSV input/output
- sample_data.csv: test dataset with valid and invalid records
- tests/test_cases.md: manual test cases and expected results
- .gitignore: excludes generated and local files

## How to run later
When the project is complete, you can run:
```bash
python main.py
```

## Beginner learning path
Before implementing the full project, focus on these:
1. Python basics: variables, loops, functions
2. Working with dictionaries and lists
3. Reading and writing CSV files using the csv module
4. Regular expressions for validation
5. datetime for date checks
6. Duplicate detection using normalized values
7. Clean console menu design

## Notes
This starter project intentionally avoids a full implementation. The code includes TODO comments to guide beginner development.
