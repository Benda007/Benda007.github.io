"""
db.py
This module contains the classes and functions for managing the database related to the Headache Tracker application.
It handles interaction with the SQLite database to add, edit, and retrieve headache-related data.
"""
import sqlite3
import sys
from datetime import datetime
from tabulate import tabulate
import os
import pandas as pd
import csv

# message saying that user canceled operation (OPeration CANceled)
opcan = "Operation was canceled."

# After a lot of DRY mistakes this functin is finally looping through all other functions asking user for inputs.


def select_from_list(options, prompt):
    """
    Displays a list of options to the user and prompts for a selection.

    Args:
        options (list of dict): A list where each dictionary contains 'name' and 'description' keys.
        prompt (str): A message describing what the user is selecting.

    Returns:
        str: The 'name' value of the selected option.

    Raises:
        SystemExit: If the user enters "cancel" to terminate the operation.

    Usage:
        Provide the user with a list of options to choose from. If the user inputs "cancel", the operation will cease.
    """
    print(f"\nSelect {prompt} from the following options or type \"cancel\": ")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option['name']}: {option['description']}")

    while True:
        try:
            choice = input("\nEnter the number corresponding to your choice: ")
            if choice.lower() == "cancel":
                print(opcan)
                sys.exit()
            choice = int(choice)
            if 1 <= choice <= len(options):
                return options[choice - 1]['name']
            else:
                print("Invalid choice. Please, select from the list.")
        except ValueError:
            print("Please, enter a positive number.")


def export_to_excel(db_manager, excel_filename):
    """
    Exports records from the database to an Excel file.

    Args:
        db_manager (DatabaseManager): An instance used for database interaction.
        excel_filename (str): The name of the output Excel file.

    Raises:
        Exception: If the file could not be written due to access issues or invalid paths.

    Effects:
        Generates an Excel file that contains a complete listing of database records.
    """
    tracker = HeadacheTracker()
    try:
        # Fetch records and column names from the database
        records, column_names = tracker.get_records()

        # Convert the records to a DataFrame
        df = pd.DataFrame(records, columns=column_names)

        # Write the DataFrame to an Excel file
        df.to_excel(excel_filename, index=False)

        print(f"Data successfully exported to {excel_filename}.")
    finally:
        tracker.close()


def upload_from_excel(db_manager, excel_filename):
    """
    Imports records from an Excel file into the database, with an option to overwrite existing records.

    Args:
        db_manager (DatabaseManager): An instance used for database interaction.
        excel_filename (str): The name of the Excel file to import data from.

    Raises:
        ValueError: If date parsing fails due to incorrect format.

    Process:
        Prompts the user whether to clear existing records before import.
        Parses each row of the Excel file, adding user and headache records to the database.
        Handles date format discrepancies between hh:mm and hh:mm:ss.
    """
    tracker = HeadacheTracker()
    try:
        # Ask user if they want to overwrite existing records
        action = input("Do you want to overwrite existing records? (yes/no): ").strip().lower()

        if action == 'yes':
            # Clear previous records
            cursor = tracker.db_manager.get_cursor()

            # Remove related records before clearing main entry to maintain referential integrity
            cursor.execute('DELETE FROM triggers')
            cursor.execute('DELETE FROM medications')
            cursor.execute('DELETE FROM headaches')
            cursor.execute('DELETE FROM users')

            tracker.db_manager.commit()
            print("Existing records successfully cleared.")
        elif action != 'no':
            print("Invalid choice. Operation cancelled.")
            return

        # Continue with importing data from Excel file
        df = pd.read_excel(excel_filename)

        for index, row in df.iterrows():
            # Add user and obtain user_id
            user_id = tracker.user_manager.add_user(row['User name'], row['Age'], row['Sex'])

            # Handle date parsing
            date_str = row['Date']
            if isinstance(date_str, datetime):
                date_str = date_str.strftime("%Y-%m-%d %H:%M:%S")

            try:
                if len(date_str.split(':')) == 2:  # Only has hour and minute
                    datetime_combined = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                else:  # Includes seconds
                    datetime_combined = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError as ve:
                print(f"Error parsing date: {ve}")
                continue

            headache_id = tracker.headache_manager.add_headache_record(
                user_id,
                datetime_combined,
                row['Duration'],
                row['Intensity'],
                row['Type']
            )

            tracker.trigger_manager.add_triggers(
                headache_id,
                row['Diet'],
                row['Stress level'],
                row['Sleep quality']
            )

            if pd.notna(row['Medication usage']):
                medications = row['Medication usage'].split(' / ')
                for med_info in medications:
                    med_name, dosage = med_info.split(' (')
                    dosage = dosage.strip(')')
                    effectiveness = row['Effective']
                    tracker.medication_manager.add_medication(
                        headache_id, med_name, dosage, effectiveness)

        print(f"Data successfully imported from {excel_filename}.")
    finally:
        tracker.close()


class DatabaseManager:
    """
    Manages SQLite database connections and schema initialization for the Headache Tracker.

    Attributes:
        connection (sqlite3.Connection): Manages the database connection.

    Methods:
        initdb():
            Configures the database tables if they don't exist upon initialization.

        get_cursor():
            Provides a cursor for performing SQL operations.

        commit():
            Commits the current transaction to save changes.

        close():
            Properly closes the database connection.
    """

    def __init__(self, db_name="myapp/headache.db"):
        self.connection = sqlite3.connect(db_name)
        self.initdb()

    def initdb(self):
        """
        Initializes the database by creating the necessary tables if they don't exist.
        """
        cursor = self.connection.cursor()

        # user - patient
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            'User name' TEXT,
            Age INTEGER,
            Sex TEXT
        );
        ''')
        # severity of headache
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS headaches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            Date DATE NOT NULL,
            Duration INTEGER,
            Intensity INTEGER,
            Type TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        ''')
        # triggers table - what is causing headache
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS triggers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headache_id INTEGER,
            Diet TEXT,
            'Stress level' TEXT,
            'Sleep quality' TEXT,
            FOREIGN KEY (headache_id) REFERENCES headaches (id)
        );
        ''')

        # medications table - pills taken
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headache_id INTEGER,
            Medication TEXT,
            Dosage TEXT,
            Effective TEXT,
            FOREIGN KEY (headache_id) REFERENCES headaches (id)
        );
        ''')
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


class UserManager:
    """
    Handles operations related to user information in the database.

    Attributes:
        db_manager (DatabaseManager): The database manager to execute operations.

    Methods:
        add_user(): Prompts for user input to add a new user to the database.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_user(self, name=None, age=None, sex=None):
        """
        Register a user profile in the database. Supports CLI input when arguments omitted.

        Args:
            name (str): The name of the user.
            age (int): The age of the user.
            sex (str): The biological sex of the user ('M' or 'F').

        Returns:
            int: Database ID of newly added user.
        """
        # If called from CLI, collect data interactively
        if name is None:
            # Get username from user.
            while True:
                name = input("Enter username or type \"cancel\": ").strip()
                if name.lower() == "cancel":
                    print(opcan)
                    sys.exit()
                elif name:
                    name = name.strip().title()
                    break
                else:
                    print("Name cannot be empty. Please, enter valid name.")

        if age is None:
            while True:
                try:
                    age = input("\nEnter user\'s age or type \"cancel\": ")
                    if age.lower() == "cancel":
                        print(opcan)
                        sys.exit()
                    elif int(age) > 0:
                        age = int(age)
                        break
                    else:
                        print("Age must be a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        if sex is None:
            while True:
                sex = input("\nEnter user\'s sex (M or F) or type \"cancel\": ").strip().upper()
                if sex.lower() == "cancel":
                    print(opcan)
                    sys.exit()
                elif sex in ['M', 'F']:
                    break
                else:
                    print("Invalid input. Please, enter M or F.")

        cursor = self.db_manager.get_cursor()
        cursor.execute("INSERT INTO users ('User name', Age, Sex) VALUES (?, ?, ?)",
                       (name, age, sex))
        self.db_manager.commit()
        return cursor.lastrowid


class HeadacheManager:
    """
    Manages headache records, including adding and querying episodes.

    Attributes:
        db_manager (DatabaseManager): The database manager for executing SQL commands.

    Methods:
        add_headache_record(user_id, datetime_combined, duration, intensity, headache_type):
            Adds a new headache record to the database.
        get_datetime_for_headache(): Prompts user to input date and time for the headache episode.
        get_duration(): Prompts user to input headache duration in minutes.
        get_intensity(): Prompts user to rate headache intensity on a scale from 1 to 10.
        choose_headache_type(): Allows user to select headache type from a predefined list.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_headache_record(self, user_id, datetime_combined, duration, intensity, headache_type):
        """
        Insert a headache record associated with a user.

        Args:
            user_id (int): User ID linking record to user.
            datetime_combined (DateTime): Combined date and time of headache occurrence.
            duration (int): Duration in minutes.
            intensity (int): Intensity score (1-10).
            headache_type (str): Description of headache type.

        Returns:
            int: Database ID of newly added headache record.
        """
        cursor = self.db_manager.get_cursor()
        cursor.execute("INSERT INTO headaches (user_id, Date, Duration, Intensity, Type) VALUES (?, ?, ?, ?, ?)",
                       (user_id, datetime_combined.strftime("%Y-%m-%d %H:%M"), duration, intensity, headache_type))
        self.db_manager.commit()
        return cursor.lastrowid

    # Include get_datetime_for_headache, get_duration, get_intensity, and choose_headache_type

    def get_datetime_for_headache(self):
        """
        Prompt the user for the date and time of the headache episode.

        Collect input for both date in 'YYYY-MM-DD' format and time in 'HH:MM'.
        Validate that provided datetime is not in the future.

        Returns:
            datetime: Validated headache datetime entry.
        """
        while True:
            try:
                # Ask for a date of headache episode
                user_date = input(
                    "\nEnter the date of the headache episode in format (YYYY-MM-DD), or type \"cancel\": ")
                if user_date.lower() == "cancel":
                    print(opcan)
                    sys.exit()

                date = datetime.strptime(user_date, "%Y-%m-%d").date()

                # Ask for a time of the headache episode
                user_time = input(
                    "\nEnter the time of the headache episode in format (HH:MM), or type \"cancel\": ")
                if user_time.lower() == "cancel":
                    print(opcan)
                    sys.exit()

                time = datetime.strptime(user_time, "%H:%M").time()
                headache_datetime = datetime.combine(date, time)

                # Ensure the combined datetime is not in the future
                if headache_datetime > datetime.now():
                    print("The date and time cannot be in the future. Please enter a valid past date and time.")
                    continue  # Restart the input process for both date and time

                return headache_datetime  # Return the valid past datetime

            except ValueError as e:
                print(
                    f"Invalid input: {e}. Please ensure your inputs match the required format and try again.")

    def get_duration(self):
        """
        User prompt to input headache duration. Limited to less than one day.

        Returns:
            int: Accepted duration value in minutes.
        """
        while True:
            try:
                duration = input(
                    "\nEnter the duration of the headache in minutes, or type \"cancel\": ")
                if duration.lower() == "cancel":
                    print(opcan)
                    sys.exit()
                duration = int(duration)
                if 0 < duration <= 86400:  # lower than one day, 24 hours
                    return duration
                    # break - not needed in this scenario
                else:
                    print("Duration must be between 1 and 86400 minutes.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_intensity(self):
        """
        Prompt the user for headache intensity using a visual analog scale (VAS).

        Returns:
            int: Intensity level chosen.
        """
        while True:
            try:
                intensity = input(
                    "\nRate the intensity of the headache on a scale from 1 (very mild) to 10 (unspeakable) or type \"cancel\": ")
                if intensity.lower() == "cancel":
                    print(opcan)
                    sys.exit()
                intensity = int(intensity)
                if 1 <= intensity <= 10:
                    return intensity
                    # break - not needed in this scenario
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Enter a numerical value.")

    def choose_headache_type(self):
        """
        Present users with headache types to classify their headache experience.

        Usage:
            Choose from tension, migraine, cluster, or other types.

        Returns:
            str: Name of the chosen headache type.
        """
        types = [
            {
                "name": "Tension",
                "description": "Dull, aching pain on both sides of the head."
            },
            {
                "name": "Migraine",
                "description": "Intense, throbbing headaches."
            },
            {
                "name": "Cluster",
                "description": "Severe, burning pain, usually around one eye or one side of the head."
            },
            {
                "name": "Other",
                "description": ""
            }
        ]
        return select_from_list(types, "Types of headache.")


class TriggerManager:
    """
    Administer headache trigger records in the database.

    Attributes:
        db_manager (DatabaseManager): Bridge to carry out database operations.

    Methods:
        add_triggers(headache_id, diet, stress_level, sleep_quality): Record trigger information relative to a headache record.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_triggers(self, headache_id, diet, stress_level, sleep_quality):
        """
        Add trigger data concerning a headache event.

        Args:
            headache_id (int): Reference to the specific headache event.
            diet (str): Diet details during the headache.
            stress_level (str): Stated stress level.
            sleep_quality (str): Quality assessment of sleep.

        Commits trigger data into the database.
        """
        cursor = self.db_manager.get_cursor()
        cursor.execute("INSERT INTO triggers (headache_id, Diet, 'Stress level', 'Sleep quality') VALUES (?, ?, ?, ?)",
                       (headache_id, diet, stress_level, sleep_quality))
        self.db_manager.commit()


class MedicationManager:
    """
    Coordinate medication details linked with headache records.

    Attributes:
        db_manager (DatabaseManager): Collaboration for executing database related actions.

    Methods:
        add_medication(headache_id, medication_name, dosage, effectiveness): Insert medication details alongside a headache report.
    """

    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_medication(self, headache_id, medication_name, dosage, effectiveness):
        """
        Add medication information for a headache event.

        Args:
            headache_id (int): Reference ID for the related headache record.
            medication_name (str): Name of medication taken.
            dosage (str): Dosage taken (e.g., number of pills).
            effectiveness (str): User-reported effectiveness ('Yes' or 'No').

        Commits medication data into the database.
        """
        cursor = self.db_manager.get_cursor()
        cursor.execute("INSERT INTO medications (headache_id, Medication, Dosage, Effective) VALUES (?, ?, ?, ?)",
                       (headache_id, medication_name, dosage, effectiveness))
        self.db_manager.commit()


class HeadacheTracker:
    """
    Encapsulates functionality for managing the Headache Tracker application.

    Attributes:
        db_manager (DatabaseManager): Handles direct communication with the database.
        user_manager (UserManager): Directs user-based database activities.
        headache_manager (HeadacheManager): Facilitates headache records.
        trigger_manager (TriggerManager): Manages headache trigger records.
        medication_manager (MedicationManager): Handles medication records.

    Methods:
        add_record(): Gather and add new user record related to headaches.
        edit_record(headache_id): Offers editing of an extant headache record.
        delete_record(headache_id): Initiates the removal of a headache record.
        get_unique_values(column): Retrieves distinct values from a database column.
        choose_diet(): User selection for dietary triggers involved in headache.
        choose_stress_level(): User choice for stress levels contributing to headache.
        choose_sleep_quality(): Verify sleep quality levels for user headache episodes.
        get_medication_info(): Details user medication specifics for treatment tracking.
        get_records(): Retrieve all database entries for display or analysis.
        display_records_with_formatting(records, column_names): Provides formatted database records for user reading.
        close(): Dispose of the database connection.
    """

    def __init__(self, db_path="myapp/headache.db"):

        self.db_manager = DatabaseManager(db_path)
        self.user_manager = UserManager(self.db_manager)
        self.headache_manager = HeadacheManager(self.db_manager)
        self.trigger_manager = TriggerManager(self.db_manager)
        self.medication_manager = MedicationManager(self.db_manager)

    def add_record(self):
        """
        Interactively collects data from the user to enter a new headache record.

        Steps include:
        - Capture user and headache details (duration, intensity, type).
        - Collect triggers such as diet, stress, and sleep information.
        - Record any medication taken for headache relief.
        - Stores the collected data in the database.
        - Short descrtiption is provided to each of records.
        """
        # this was very complicated and without help from external resouces
        # I could not understand this topic.
        user_id = self.user_manager.add_user()
        datetime_combined = self.headache_manager.get_datetime_for_headache()

        duration = self.headache_manager.get_duration()
        intensity = self.headache_manager.get_intensity()
        headache_type = self.headache_manager.choose_headache_type()

        headache_id = self.headache_manager.add_headache_record(
            user_id, datetime_combined, duration, intensity, headache_type)

        diet = self.choose_diet()
        stress_level = self.choose_stress_level()
        sleep_quality = self.choose_sleep_quality()

        self.trigger_manager.add_triggers(headache_id, diet, stress_level, sleep_quality)

        medication_name, dosage, effectiveness = self.get_medication_info()
        self.medication_manager.add_medication(headache_id, medication_name, dosage, effectiveness)

        print("\nRecord added successfully!\n")

    def edit_record(self, headache_id):
        """Edit a record identified by its ID. ID of headache incident"""
        cursor = self.db_manager.get_cursor()

        cursor.execute('''SELECT * FROM headaches WHERE id = ?''', (headache_id,))
        record = cursor.fetchone()
        if not record:
            print("No such record exists.")
            return

        # Prompt for user inputs to update fields. These fields can be extended
        # as per logic similar to adding record.
        duration = self.headache_manager.get_duration()
        intensity = self.headache_manager.get_intensity()
        headache_type = self.headache_manager.choose_headache_type()

        cursor.execute('''
            UPDATE headaches SET Duration = ?, Intensity = ?, Type = ?
            WHERE id = ?''', (duration, intensity, headache_type, headache_id))
        self.db_manager.commit()
        print(f"Record with Headache ID {headache_id} updated successfully!")

    def delete_record(self, headache_id):
        """Delete a record by its ID."""
        cursor = self.db_manager.get_cursor()

        cursor.execute('''SELECT * FROM headaches WHERE id = ?''', (headache_id,))
        record = cursor.fetchone()
        if not record:
            print("No such record exists.")
            return

        # Delete related records in triggers and medications first, then headache
        cursor.execute('''DELETE FROM triggers WHERE headache_id = ?''', (headache_id,))
        cursor.execute('''DELETE FROM medications WHERE headache_id = ?''', (headache_id,))
        cursor.execute('''DELETE FROM headaches WHERE id = ?''', (headache_id,))
        self.db_manager.commit()
        print("Record deleted successfully!")

    def get_unique_values(self, column):
        """This is defining unique values which can be used for linking with already existing data in
        database so filter function is offering only existing data."""

        cursor = self.db_manager.get_cursor()
        query = f"SELECT DISTINCT {column} FROM users JOIN headaches ON users.id = headaches.user_id JOIN triggers ON headaches.id = triggers.headache_id LEFT JOIN medications ON headaches.id = medications.headache_id"
        cursor.execute(query)
        results = cursor.fetchall()
        # Flatten the list and keep only non-null values
        return [result[0] for result in results if result[0] is not None]

    def choose_diet(self):
        """
        Interactively collects possible triggers which causes headached.

        Steps include:
        - Offering of predefined list of triggers to the user.
        - Sellection of given trigger by user.
        - Storing of selected option into the database.
        - Short descrtiption is provided to each of records.
        """
        dietary_triggers = [
            {
                "name": "Tyramine",
                "description": "Found in aged cheeses and cured meats."
            },
            {
                "name": "Nitrates/Nitrites",
                "description": "Common in processed meats like bacon and hot dogs."
            },
            {
                "name": "Alcohol",
                "description": "Especially red wine."
            },
            {
                "name": "Caffeine",
                "description": "Found in coffee, tea, and some sodas."
            },
            {
                "name": "Monosodium Glutamate (MSG)",
                "description": "Used as a flavor enhancer in many foods."
            },
            {
                "name": "Aspartame",
                "description": "An artificial sweetener in diet products."
            },
            {
                "name": "Chocolate",
                "description": "Contains caffeine and theobromine."
            },
            {
                "name": "Cultured Dairy Products",
                "description": "Like yogurt and sour cream."
            },
            {
                "name": "Processed Foods",
                "description": "High in preservatives and additives."
            },
            {
                "name": "High Sugar Intake",
                "description": "Can cause blood sugar fluctuations."
            },
            {
                "name": "Dehydration",
                "description": "Not drinking enough water."
            },
            {
                "name": "Irregular Meal Patterns",
                "description": "Skipping meals or eating at odd times."
            }
        ]
        return select_from_list(dietary_triggers, "Dietary trigger")
        # return dietary_triggers

    def choose_stress_level(self):
        """
        Interactively select stress level which inpacted headache incidnet.

        Steps include:
        - Selection of stress level from predefined scale.
        - Storing of selected stress level into the database.
        - Short descrtiption is provided to each of records.
        """
        stress_levels = [
            {
                "name": "Low",
                "description": "Minimal stress, manageable daily life."
            },
            {
                "name": "Moderate",
                "description": "Increased stress from work or personal life."
            },
            {
                "name": "High",
                "description": "Significant stress, anxiety, or pressure."
            },
            {
                "name": "Severe",
                "description": "Chronic stress, trauma, or overwhelming situations"
            }
        ]
        return select_from_list(stress_levels, "Stress level")
        # return stress_levels

    def choose_sleep_quality(self):
        """
        Interactively selects quality sleep from predefined list.

        Steps include:
        - Selection of quality sleep category from list offered to user.
        - Collecting of selected data.
        - Storring into database.
        - Short descrtiption is provided to each of records.
        """

        sleep_category = [
            {
                "name": "Low",
                "description": "Sleep duration of less than 6 hours per night."
            },
            {
                "name": "Medium",
                "description": "Sleep duration between 6 to 8 hours per night."
            },
            {
                "name": "High",
                "description": "Sleep duration of 7 to 9 hours per night."
            }
        ]

        return select_from_list(sleep_category, "Quality of sleep")
        # return sleep_category

    def get_medication_info(self):
        """
        User is selecting what medication was used for headache.

        - Captures user input for medication
        - Short descrtiption is provided to each of records.
        """
        # Medication part
        medications = [
            {
                "name": "Paracetamol",
                "description": "Safe for most; short-term use."
            },
            {
                "name": "Ibuprofen",
                "description": "Effective; caution with GI issues."
            },
            {
                "name": "Aspirin",
                "description": "Not for children; Reye's risk."
            },
            {
                "name": "Naproxen",
                "description": "Effective; similar to ibuprofen."
            },
            {
                "name": "Metamizol",
                "description": "Similar to Paracetamol but a bit stronger."
            },
            {
                "name": "Diclofenac",
                "description": "Caution in CV/GI issues."
            },
            {
                "name": "Sumatriptan",
                "description": "For acute migraines; medical guidance needed."
            },
            {
                "name": "Rizatriptan",
                "description": "For acute migraines; consult provider."
            },
            {
                "name": "Eletriptan",
                "description": "For migraines; caution in CV issues."
            }
        ]
        medication_name = select_from_list(medications, "medication taken for the headache")

        while True:
            try:
                # Prompt for dosage as number of pills
                dosage = input(
                    f"\nEnter the number of pills taken for {medication_name} or type \"cancel\": ")
                if dosage.lower() == "cancel":
                    print(opcan)
                    sys.exit()
                dosage = int(dosage)  # Convert dosage to integer
                if dosage > 0:  # Ensure dosage is positive
                    break
                else:
                    print("Invalid input. Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a positive number.")

        # Track whether medication did help or not.
        while True:
            try:
                effectiveness = input(
                    "\nDid the medication help? Enter Yes or No, or type \"cancel\": ").strip().title()
                if effectiveness.lower() == "cancel":
                    print(opcan)
                    sys.exit()
                elif effectiveness in ["Yes", "Y", "No", "N"]:
                    if effectiveness.startswith("Y"):
                        effectiveness = "Yes"
                    else:
                        effectiveness = "No"
                    break
                print("Invalid input. Please enter \"Yes\" or \"No\".")
            except ValueError:
                print("Invalid input. Please enter 'Yes' or 'No'.")

        return medication_name, dosage, effectiveness

    def get_records(self):
        cursor = self.db_manager.get_cursor()
        cursor.execute('''
        SELECT users.id AS 'User ID', users.'user name', users.age, users.sex,
            headaches.id AS 'Headache ID', headaches.date, headaches.duration, headaches.intensity, headaches.type,
            triggers.diet, triggers.'stress level', triggers.'sleep quality',
            GROUP_CONCAT(medications.medication || ' (' || medications.dosage || ')' , ' / ') AS 'Medication usage', medications.effective
        FROM users
        JOIN headaches ON users.id = headaches.user_id
        JOIN triggers ON headaches.id = triggers.headache_id
        LEFT JOIN medications ON headaches.id = medications.headache_id
        GROUP BY headaches.id;
        ''')

        column_names = [description[0] for description in cursor.description]
        records = cursor.fetchall()
        return records, column_names

    def preprocess_records(self, records):
        # Replace None in records with 'N/A' or an appropriate placeholder
        return [[cell if cell is not None else 'N/A' for cell in record] for record in records]

    # Display formatted records with headers

    def display_records_with_formatting(self, records, column_names):
        # Ensure your records are preprocessed
        processed_records = self.preprocess_records(records)

        if not processed_records:
            # Manually print headers, if no data is present
            header_line = " | ".join(column_names)
            print("\nNo records found. Below are the table headers:")
            print(header_line)
            print("-" * len(header_line))
        else:
            print(tabulate(processed_records, headers=column_names, tablefmt="fancy_grid", maxcolwidths=[
                25] * len(column_names), colalign=["center"] * len(column_names)))

    def close(self):
        self.db_manager.close()
