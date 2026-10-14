"""
CleanSlate - main.py (starter)

Responsibility:
- Provide a simple console menu and orchestrate high-level flow.
- Should remain small: delegate CSV I/O to file_handler and validation/cleaning to validator.

TODOs:
- Wire the menu options to validator and file_handler functions.
- Implement persistent settings or argument parsing if desired later.

This file is intentionally a lightweight starter so you can focus on learning modules separately.
"""

from typing import List, Dict

# TODO: Import the real modules once validator and file_handler are implemented
# from file_handler import read_csv, write_csv
# from validator import validate_record, clean_record, detect_duplicates

SAMPLE_FILE = "sample_data.csv"
CLEANED_OUTPUT = "cleaned_data.csv"
ERROR_OUTPUT = "error_report.csv"


def print_menu() -> None:
    print("\n=== CleanSlate: Data Validation and Cleansing Utility ===")
    print("1. Load sample data")
    print("2. Validate records (detect issues)")
    print("3. Show summary (counts)")
    print("4. Export cleaned data")
    print("5. Export error report")
    print("6. Exit")


def main() -> None:
    """Main menu loop.

    Right now this is a skeleton. Implementations should call file_handler and
    validator functions. Keep main.py focused on user interaction only.
    """
    loaded_records: List[Dict] = []

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            print("Loading sample data (TODO: call file_handler.read_csv)")
            # TODO: loaded_records = read_csv(SAMPLE_FILE)
            print("(Sample loading not implemented in this starter)")

        elif choice == "2":
            print("Validating records (TODO: call validator.validate_record for each row)")
            # TODO: iterate loaded_records and collect issues
            print("(Validation not implemented in this starter)")

        elif choice == "3":
            print("Showing summary (TODO: compute counts of valid/invalid/duplicates)")
            # TODO: print summary based on validation results

        elif choice == "4":
            print(f"Exporting cleaned data to {CLEANED_OUTPUT} (TODO)")
            # TODO: call write_csv to export cleaned rows

        elif choice == "5":
            print(f"Exporting error report to {ERROR_OUTPUT} (TODO)")
            # TODO: call write_csv to export error rows

        elif choice == "6":
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
