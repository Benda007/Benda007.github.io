"""
core.py
This module encompasses the business logic for filtering headache records.
It interacts with the HeadacheTracker class to apply various filter criteria to the stored data.
"""

import sqlite3
from myapp.db import DatabaseManager, UserManager, HeadacheManager, TriggerManager, MedicationManager, HeadacheTracker


def filter_criteria(tracker, filter_criteria):
    """
    Filter headache records from the database based on specified criteria.

    This function constructs a SQL query based on the filter criteria provided.
    It executes the query to retrieve headache records that match the given criteria
    and returns the results along with the column names for display purposes.

    Args:
        tracker (HeadacheTracker): An instance of HeadacheTracker, providing access to the database.
        filter_criteria (dict): A dictionary containing keys that map to potential filter options.
                               Keys may include 'user_name', 'start_date', 'end_date', 'intensity',
                               'dosage', 'medication', 'diet', 'sleep', 'stress', and 'effectiveness'.

    Returns:
        tuple: A pair consisting of:
            - records (list of tuples): The filtered database records.
            - column_names (list of str): Column headers related to the fetched records.

    Raises:
        sqlite3.Error: If an error occurs when executing the SQL query.

    Note:
        Prints a message if no records match the filter criteria.
    """

    # Consistent columns to maintain consistent headers
    query = '''
    SELECT users.id AS 'User ID', users.'user name', users.age, users.sex,
           headaches.id AS 'Headache ID', headaches.date, headaches.duration, headaches.intensity, headaches.type,
           triggers.diet, triggers.'stress level', triggers.'sleep quality',
           GROUP_CONCAT(medications.medication || ' (' || medications.dosage || ')', ' / ') AS 'Medication usage',
           medications.effective
    FROM users
    JOIN headaches ON users.id = headaches.user_id
    JOIN triggers ON headaches.id = triggers.headache_id
    LEFT JOIN medications ON headaches.id = medications.headache_id
    '''

    # Apply filters using WHERE clause
    conditions = []
    params = []

    if filter_criteria.get('user_name'):
        conditions.append("users.'user name' LIKE ?")
        params.append(f"%{filter_criteria['user_name']}%")

    if filter_criteria.get('start_date'):
        conditions.append("headaches.date >= ?")
        params.append(filter_criteria['start_date'])

    if filter_criteria.get('end_date'):
        conditions.append("headaches.date <= ?")
        params.append(filter_criteria['end_date'])

    if filter_criteria.get('intensity') is not None:
        conditions.append("headaches.intensity = ?")
        params.append(filter_criteria['intensity'])

    if filter_criteria.get('dosage'):
        conditions.append("medications.dosage = ?")
        params.append(filter_criteria['dosage'])

    if filter_criteria.get('medication'):
        conditions.append("medications.medication = ?")
        params.append(filter_criteria['medication'])

    if filter_criteria.get('diet'):
        conditions.append("triggers.diet = ?")
        params.append(filter_criteria['diet'])

    if filter_criteria.get('sleep'):
        conditions.append("triggers.'sleep quality' = ?")
        params.append(filter_criteria['sleep'])

    if filter_criteria.get('stress'):
        conditions.append("triggers.'stress level' = ?")
        params.append(filter_criteria['stress'])

    if filter_criteria.get('effectiveness'):
        conditions.append("medications.effective = ?")
        params.append(filter_criteria['effectiveness'])

    # Add WHERE clause if there are filtering conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Aggregate by headache id for unique results
    query += ' GROUP BY headaches.id;'

    cursor = tracker.db_manager.get_cursor()

    cursor.execute(query, params)
    records = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    if not records:
        print("\nSorry, no data to show based on filter criteria.\n")

    return records, column_names

def get_headaches_by_trigger(tracker):
    """
    Aggregates headache records by trigger and calculates the number of occurrences for each trigger.
    """
    query = '''
    SELECT triggers.diet AS trigger, COUNT(headaches.id) AS headache_count
    FROM headaches
    JOIN triggers ON headaches.id = triggers.headache_id
    GROUP BY triggers.diet
    '''
    
    cursor = tracker.db_manager.get_cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    return records  # This will return a list of (trigger, headache_count) tuples
