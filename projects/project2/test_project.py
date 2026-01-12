import os
import tempfile
import pytest
from unittest.mock import patch
from myapp.db import DatabaseManager, UserManager, HeadacheManager, TriggerManager, MedicationManager, HeadacheTracker
from project import add_record, filter_records
from myapp.core import filter_criteria


# this was creating issue when a productino database was created and not a temporary one
# db_manager = DatabaseManager()
# user_manager = UserManager(db_manager)
# headache_manager = HeadacheManager(db_manager)
# trigger_manager = TriggerManager(db_manager)
# medication_manager = MedicationManager(db_manager)
# tracker = HeadacheTracker()


def test_add_record():
    """
    Test the functionality of adding a new record to the database.

    This test case ensures that a new record can be added successfully by first verifying
    the database is empty, then adding a record, and finally checking that the record count increases by one.
    """
    # Create a temporary file path for the database
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        tracker = None
        try:
            # Use the temporary database file with HeadacheTracker
            tracker = HeadacheTracker(temp_file.name)
            records_before, _ = tracker.get_records()
            assert len(records_before) == 0  # Check that there are initially no records

            # Mock inputs and add a record directly on the tracker instance
            with patch('builtins.input', side_effect=[
                'user01', '40', 'M', '2025-08-01', '10:20' , '60', '3', '1', '12', '1', '2', '1', '2', 'Y'
            ]):
                tracker.add_record()

            # Verify if a new record has been added
            records_after, _ = tracker.get_records()
            assert len(records_after) == 1  # Now expecting a single record

        finally:
            # Closing of tracker and the temporary database file is deleted. This is must!
            if tracker is not None:
                tracker.close()
            temp_file.close()
            os.remove(temp_file.name)


def test_cancel_during_user_input():
    """
    Test the cancellation behavior during user input.

    This test simulates the user entering 'cancel' at different stages of the input process
    and verifies that the system exits without completing the operation.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        tracker = None
        try:
            tracker = HeadacheTracker(temp_file.name)
            #tracker.initdb()

            # Mock 'cancel' input at user name prompt. Simple check for first input.
            with patch('builtins.input', side_effect=['cancel']):
                with pytest.raises(SystemExit):
                    tracker.add_record()
            # Mock 'cancel' input at user name prompt. Simple check for second input.
            with patch('builtins.input', side_effect=['user01', 'cancel', 'M', '2025-08-01', '10:30', '60', '3', '1', '12', '1', '2', '1', '2', 'Y']):
                with pytest.raises(SystemExit):
                    tracker.add_record()
            with patch('builtins.input', side_effect=['user01', '99', 'M', '2025-08-01', '10:30','60', '3', '1', '12', '1', 'cancel', '1', '2', 'Y']):
                with pytest.raises(SystemExit):
                    tracker.add_record()
            with patch('builtins.input', side_effect=['user01', 'cancel', 'M', '2025-08-01', '10:30', 'cancel', '3', '1', '12', '1', '2', '1', '2', 'Y']):
                with pytest.raises(SystemExit):
                    tracker.add_record()
            with patch('builtins.input', side_effect=['user01', 'cancel', 'M', '2025-08-01', '10:30', '60', '3', '1', '12', '1', '2', '1', 'cancel', 'Y']):
                with pytest.raises(SystemExit):
                    tracker.add_record()
            with patch('builtins.input', side_effect=['user01', 'cancel', 'M', '2025-08-01', '10:30', '60', '3', '1', '12', '1', '2', '1', '2', 'cancel']):
                with pytest.raises(SystemExit):
                    tracker.add_record()

        finally:
            if tracker is not None:
                tracker.close()
            temp_file.close()
            os.remove(temp_file.name)







def test_for_valid_input():
    """
    Test input validation when adding a new record.

    Simulates incorrect user inputs for various fields to ensure that the program
    prompts for correct inputs and adds the record once valid data is received.
    """

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        tracker = None
        try:
            tracker = HeadacheTracker(temp_file.name)

            # Expanded input list to align with code validation and expected retries
            with patch('builtins.input', side_effect=[
                '',                   # Empty username, re-prompt
                'user01',             # Correct username
                'fourty four',        # Invalid age, re-prompt
                '44',                 # Correct age
                'd',                  # Invalid gender, re-prompt
                'F',                  # Correct gender
                '01-12-1999',         # Invalid date format
                '10:30',              # Correct time
                '2020-01-01',         # Correct date (ensure non-future date)
                '25:80',              # Invalid time format, re-prompt
                '2020-01-01',         # Correct date (ensure non-future date)
                '10:30',              # Correct time
                'one minute',         # Invalid duration, re-prompt
                '60',                 # Correct duration
                'medium',             # Invalid intensity, re-prompt
                '3',                  # Correct intensity
                'invalid_type',       # Invalid headache type, re-select
                '2',                  # Correct - selects "Migraine"
                '',                   # Invalid dietary trigger entry, re-select
                '7',                  # Correct
                'wrong_level',        # Invalid stress level
                '1',                  # Correct stress level - "Low"
                'bad_quality',        # Incorrect quality of sleep
                '2',                  # Correct sleep quality - "Medium"
                '',                   # No medication input previously (blank), re-prompt
                '1',                  # "Paracetamol"
                'twenty',             # Invalid dosage
                '1',                  # Correct dosage as 1 pill
                'Nope',               # Invalid effectiveness input
                'Yes'                 # Correct effectivity
            ]):
                tracker.add_record()

            # Verify the number of records is 1
            records, _ = tracker.get_records()
            assert len(records) == 1

            # Ensure the record data is formatted as expected -- adjust to your logic's design
            expected_record = (
                1, 'User01', 44, 'F', 1, '2020-01-01 10:30', 60, 3, 'Migraine',
                'Chocolate', 'Low', 'Medium', 'Paracetamol (1)', 'Yes'
            )
            assert records[0] == expected_record

        finally:
            if tracker is not None:
                tracker.close()
            temp_file.close()
            os.remove(temp_file.name)

def test_filtering_reccords():
    """
    Test filtering functionality of records based on specific criteria.

    Adds a single record and applies filters to verify that the correct records
    are retrieved based on the given criteria.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        tracker = None
        try:
            tracker = HeadacheTracker(temp_file.name)

            # Simulate adding a single record - ensure each selection input is covered
            with patch('builtins.input', side_effect=[
                'User01',       # User name
                '30',           # Age
                'M',            # Sex
                '2023-08-01',   # Date
                '10:20',        # Time
                '60',           # Duration
                '3',            # Intensity
                '1',            # Headache type (e.g., Tension)
                '12',           # Dietary trigger (e.g., Irregular Meal Patterns)
                '1',            # Stress level (e.g., Low)
                '2',            # Sleep quality (e.g., Medium)
                '1',            # Medication usage (e.g., Eletriptan (1))
                '2',            # Dosage (e.g., number of pills)
                'Yes'           # Effectiveness
            ]):
                tracker.add_record()

            # Verify if a new record has been added
            records, _ = tracker.get_records()
            print("Actual Record:", records[0])
            assert len(records) == 1  # Expecting a single record

            # Establish filter criteria to match this specific record
            criteria = {'user_name': 'User01'}
            filtered_records, _ = filter_criteria(tracker, criteria)

            # Validate the result of filtering
            assert len(filtered_records) == 1
            expected_record = (1, 'User01', 30, 'M', 1, '2023-08-01 10:20', 60, 3, 'Tension',
                            'Irregular Meal Patterns', 'Low', 'Medium', 'Paracetamol (2)', 'Yes')
            assert filtered_records[0] == expected_record

        finally:
            if tracker is not None:
                tracker.close()
            temp_file.close()
            os.remove(temp_file.name)


