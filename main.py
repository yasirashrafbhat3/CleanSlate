
from file_handler import (
    read_csv,
    write_cleaned_csv,
    write_error_report
)
from validator import process_records

records = []
cleaned_records = []
errors = []
data_loaded = False
data_processed = False


def display_menu():
    print("\n" + "=" * 48)
    print("                  CLEANSLATE")
    print("       DATA VALIDATION & CLEANSING UTILITY")
    print("=" * 48)
    print("1. Load CSV File")
    print("2. Validate and Clean Data")
    print("3. Detect Duplicate Records")
    print("4. View Error Report")
    print("5. Export Cleaned Data and Error Report")
    print("6. Exit")
    print("=" * 48)


def load_data():
    global records, cleaned_records, errors
    global data_loaded, data_processed

    filename = input(
        "\nEnter CSV file name or path: "
    ).strip()

    if not filename:
        print("\nPlease enter a valid CSV file name.")
        return

    try:
        new_records = read_csv(filename)

        records = new_records
        cleaned_records = []
        errors = []

        data_loaded = True
        data_processed = False

        print("\nCSV loaded successfully!")
        print("File:", filename)
        print("Total records:", len(records))

    except (OSError, ValueError) as error:
        print("\nUnable to load CSV:", error)


def validate_data():
    global cleaned_records, errors, data_processed

    if not data_loaded:
        print("\nPlease load a CSV file first!")
        return

    cleaned_records, errors = process_records(records)
    data_processed = True

    rows_with_errors = {
        item["row"] for item in errors
    }

    print("\nVALIDATION COMPLETED")
    print("-" * 35)
    print("Total records:", len(records))
    print("Records with issues:", len(rows_with_errors))
    print("Total issues:", len(errors))
    print("Records processed:", len(cleaned_records))


def detect_duplicates():
    if not data_processed:
        print("\nPlease validate the data first!")
        return

    duplicates = [
        item for item in errors
        if "duplicate" in item["problem"].lower()
    ]

    print("\nDUPLICATE RECORD REPORT")
    print("-" * 35)

    if not duplicates:
        print("No duplicate emails found.")
    else:
        for item in duplicates:
            print(
                "Row:", item["row"],
                "| Field:", item["field"],
                "|", item["problem"]
            )


def view_error_report():
    if not data_processed:
        print("\nPlease validate the data first!")
        return

    print("\nERROR REPORT")
    print("-" * 35)

    if not errors:
        print("No errors found.")
        return

    for item in errors:
        print(
            "Row:", item["row"],
            "| Field:", item["field"],
            "| Problem:", item["problem"]
        )


def export_data():
    if not data_processed:
        print("\nPlease validate the data first!")
        return

    try:
        write_cleaned_csv(
            cleaned_records,
            "cleaned_data.csv"
        )

        write_error_report(
            errors,
            "error_report.csv"
        )

        print("\nExport completed successfully!")
        print("Created cleaned_data.csv")
        print("Created error_report.csv")

    except OSError as error:
        print("\nExport failed:", error)


def main():
    while True:
        display_menu()

        choice = input(
            "Enter your choice (1-6): "
        ).strip()

        if choice == "1":
            load_data()

        elif choice == "2":
            validate_data()

        elif choice == "3":
            detect_duplicates()

        elif choice == "4":
            view_error_report()

        elif choice == "5":
            export_data()

        elif choice == "6":
            print("\nThank you for using CleanSlate!")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()