"""
project.py
This script serves as the entry point for the Headache Tracker application.
It provides both a CLI and a web API interface for interacting with headache records,
including operations such as adding, filtering, editing, deleting, importing, and exporting records.
"""

from myapp.db import (
    DatabaseManager,
    UserManager,
    HeadacheManager,
    TriggerManager,
    MedicationManager,
    HeadacheTracker,
    export_to_excel,
    upload_from_excel,
)
from myapp.core import filter_criteria as core_filter_criteria
import openpyxl

from myapp.api import app


def run_api():
    """
    Starts the Flask web API server.

    Launches the application in debug mode, accessible via the default localhost settings.
    """
    app.run(debug=True)


def load_data():
    """
    Reads data from the SQLite database and displays it using the HeadacheTracker.

    Utilizes the HeadacheTracker class to retrieve and render database records in a formatted output.
    """
    tracker = HeadacheTracker()  # Initialize the tracker
    try:
        records, column_names = tracker.get_records()
        tracker.display_records_with_formatting(records, column_names)
    finally:
        tracker.close()  # Ensure the connection is closed


def add_record():
    """
    Prompts user to enter a new headache record and adds it to the database.

    Initiates interactive command-line prompts to capture needed details to form a complete headache entry.
    """
    tracker = HeadacheTracker()
    try:
        tracker.add_record()
    finally:
        tracker.close()


def filter_records():
    """
    Collects filter criteria from user input, retrieves filtered headache records,
    and displays them in a formatted manner.

    Allows users to specify fields for filtering data such as user name, date, medication, etc.
    Displays only records matching the entered criteria.
    """
    tracker = HeadacheTracker()
    try:
        # Collect filter criteria
        filter_criteria = {}
        available_user_names = tracker.get_unique_values("users.'user name'")
        print(f"\nAvailable user names: {', '.join(available_user_names)}")
        filter_criteria["user_name"] = (
            input("Filter by user name (leave blank for no filter): ").strip().title()
        )

        available_dates = tracker.get_unique_values("headaches.date")
        print(f"\nAvailable dates: {', '.join(available_dates)}")
        filter_criteria["start_date"] = input(
            "Filter by start date (YYYY-MM-DD, leave blank for no filter): "
        ).strip()
        filter_criteria["end_date"] = input(
            "Filter by end date (YYYY-MM-DD, leave blank for no filter): "
        ).strip()

        available_medications = tracker.get_unique_values("medications.medication")
        print(f"\nAvailable medications: {', '.join(available_medications)}")
        filter_criteria["medication"] = (
            input("Filter by medication used (leave blank for no filter): ")
            .strip()
            .title()
        )

        available_diets = tracker.get_unique_values("triggers.diet")
        print(f"\nAvailable diets: {', '.join(available_diets)}")
        filter_criteria["diet"] = (
            input("Filter by diet triggers (leave blank for no filter): ")
            .strip()
            .title()
        )

        available_sleep = tracker.get_unique_values("triggers.'sleep quality'")
        print(f"\nAvailable sleep qualities: {', '.join(available_sleep)}")
        filter_criteria["sleep"] = (
            input("Filter by quality of sleep level (leave blank for no filter): ")
            .strip()
            .title()
        )

        available_stress = tracker.get_unique_values("triggers.'stress level'")
        print(f"\nAvailable stress levels: {', '.join(available_stress)}")
        filter_criteria["stress"] = (
            input("Filter by stress level (leave blank for no filter): ")
            .strip()
            .title()
        )

        while True:
            effectiveness = (
                input(
                    "\nFilter by effectiveness of medication (Y for Yes, N for No, leave blank for no filter): "
                )
                .strip()
                .lower()
            )
            if effectiveness == "":
                filter_criteria["effectiveness"] = None  # No filtering applied
                break
            elif effectiveness in ["y", "yes", "n", "no"]:
                filter_criteria["effectiveness"] = (
                    "Yes" if effectiveness == "y" else "No"
                )
                break
            else:
                print(
                    "Invalid input. Please enter 'Y' for Yes or 'N' for No, or leave blank for no filter."
                )

        available_intensities = tracker.get_unique_values("headaches.intensity")
        print(
            f"\nAvailable intensity levels: {', '.join(map(str, available_intensities))}"
        )

        while True:
            intensity = input(
                "Filter by intensity (choose from above or leave blank for no filter): "
            ).strip()
            try:
                if intensity:
                    filter_criteria["intensity"] = int(intensity)
                    if filter_criteria["intensity"] in available_intensities:
                        break
                    else:
                        print(
                            "Invalid choice, please choose an available intensity from the list."
                        )
                else:
                    filter_criteria["intensity"] = None
                    break

            except ValueError:
                print(
                    "Invalid intensity input. Please enter a number from the available list."
                )

        # Fetch and display filtered records
        records, column_names = core_filter_criteria(tracker, filter_criteria)
        if records:
            tracker.display_records_with_formatting(records, column_names)
        else:
            print("\nNo records match criteria you provided.\n")

    finally:
        tracker.close()


def get_valid_record_id():
    """
    Helper function to prompt and validate a numeric record ID input.

    Returns:
        int: Validated numeric record ID input by the user.
    """
    while True:
        try:
            record_id_input = input(
                "Enter the Headache ID of the record you wish to modify: "
            ).strip()
            return int(record_id_input)
        except ValueError:
            print("Invalid ID. Please enter a valid numeric ID.")


def handle_user_action(tracker, option, record_id):
    """
    Executes edit or delete operation based on user choice.

    Args:
        tracker (HeadacheTracker): Instance of HeadacheTracker to handle the chosen action.
        option (str): User's action choice, either 'edit' or 'delete'.
        record_id (int): The ID of the record to be modified.
    """
    if option == "edit":
        tracker.edit_record(record_id)
    elif option == "delete":
        tracker.delete_record(record_id)
    else:
        print('Invalid option. Please enter "edit", "delete", or "cancel".')


def edit_or_delete_records(tracker):
    """
    Continuously prompts the user to choose between editing or deleting a record by its Headache ID.
    Allows cancellation of the operation by user input.

    Ensures that users can interactively choose to modify or remove records within the dataset.
    """
    try:
        while True:
            option = (
                input(
                    'Do you want to edit or delete a record? Enter "edit", "delete", or "cancel" to exit: '
                )
                .strip()
                .lower()
            )
            if option == "cancel":
                break

            # Prompt for a valid record ID
            record_id = get_valid_record_id()
            # Perform action
            handle_user_action(tracker, option, record_id)

    finally:
        tracker.close()


def main():
    """
    Parses command-line arguments and determines application behavior.
    Options include launching the web server, initializing the database, adding, filtering, editing,
    or deleting records, and exporting or importing via Excel.

    This function serves as the primary entry point for the CLI-based interactions of the application.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Headache Tracker Application")
    parser.add_argument("--web", action="store_true", help="Run the API server")
    parser.add_argument("--init", action="store_true", help="Initialize the database")
    parser.add_argument("--add", action="store_true", help="Add a headache record")
    parser.add_argument("--filter", action="store_true", help="Filter and view records")
    parser.add_argument("--edit", action="store_true", help="Edit a headache record")
    parser.add_argument(
        "--delete", action="store_true", help="Delete a headache record"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export data to Excel. Use syntax: --export --file name.xlsx",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Import data from Excel. Use syntax: --upload --file name.xlsx",
    )
    parser.add_argument("--file", type=str, help="Excel file name for import/export")

    args = parser.parse_args()

    if (args.export or args.upload) and not args.file:
        parser.error("--file is required when using --export or --import.")

    db_manager = DatabaseManager()

    if args.web:
        run_api()
    elif args.init:
        tracker = HeadacheTracker()  # Initialize tracker for database operations
        try:
            tracker.db_manager.initdb()
        finally:
            tracker.close()
    elif args.add:
        add_record()
    elif args.filter:
        filter_records()
    elif args.edit:
        filter_records()
        tracker = HeadacheTracker()
        edit_or_delete_records(tracker)
    elif args.delete:
        filter_records()
        tracker = HeadacheTracker()
        edit_or_delete_records(tracker)
    elif args.export:
        export_to_excel(db_manager, args.file)
    elif args.upload:
        upload_from_excel(db_manager, args.file)
    else:
        load_data()


if __name__ == "__main__":
    main()
