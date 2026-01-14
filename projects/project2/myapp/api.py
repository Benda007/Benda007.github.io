from flask import Flask, request, jsonify, render_template
from myapp.db import HeadacheTracker
from myapp.core import get_headaches_by_trigger
from datetime import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


@app.route('/')
def home():
    """
    Home route serving the main page.

    Returns:
        Rendered HTML for the homepage.
    """
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add_record():
    """
    API endpoint for adding a new headache record to the database.

    Request Body:
        JSON containing user and headache details, including:
        - user_name: Name of the user.
        - user_age: Age of the user.
        - user_sex: Sex of the user ('M' or 'F').
        - date_of_headache: Date of the headache event.
        - time_of_headache: Time of the headache event.
        - duration: Duration of the headache in minutes.
        - intensity: Intensity of the headache on a 1-10 scale.
        - trigger: Trigger associated with the headache.
        - headache_type: Type of headache.
        - medication: Medication taken for relief.
        - dosage: Dosage of the medication.
        - effectiveness: Effectiveness of the medication.

    Returns:
        JSON response with success or error message and HTTP status code.
    """
    if not request.json:
        return jsonify({"error": "Request must be in JSON format."}), 400

    data = request.json
    app.logger.info(f"Data received for adding record: {data}")

    try:
        user_name = data.get('user_name', '').strip().title()
        user_age = int(data.get('user_age', 0))  # Validate age appropriately
        user_sex = data.get('user_sex', '').strip().upper()

        date_str = data.get('date_of_headache', '')
        time_str = data.get('time_of_headache', '')

        date_of_headache = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        if date_of_headache > datetime.now():
            return jsonify({"error": "The date and time of the headache cannot be in the future."}), 400

        # Get the duration value and ensure default is meaningful
        duration = int(data.get('duration', 0))
        intensity = int(data.get('intensity'))
        trigger = data.get('trigger', '')
        headache_type = data.get('headache_type', '')

        medication_name = data.get('medication', '')
        dosage = data.get('dosage', 0)
        effectiveness = data.get('effectiveness', '')

        tracker = HeadacheTracker("myapp/headache.db")
        user_id = tracker.user_manager.add_user(user_name, user_age, user_sex)
        headache_id = tracker.headache_manager.add_headache_record(
            user_id, date_of_headache, duration, intensity, headache_type
        )
        tracker.trigger_manager.add_triggers(headache_id, trigger, "Moderate", "Medium")

        if medication_name and dosage:
            tracker.medication_manager.add_medication(
                headache_id, medication_name, dosage, effectiveness
            )

        return jsonify({"message": "Record added successfully.", "headache_id": headache_id}), 201

    except Exception as e:
        app.logger.error(f"Error adding record: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        tracker.close()


@app.route('/records', methods=['GET'])
def get_records():
    """
    API endpoint to retrieve all headache records from the database.

    Returns:
        JSON response containing all headache records and their associated column names,
        along with a HTTP 200 status code.
    """
    tracker = HeadacheTracker("myapp/headache.db")
    try:
        records, column_names = tracker.get_records()
        return jsonify({"records": records, "columns": column_names}), 200
    finally:
        tracker.close()


@app.route('/headaches_by_trigger', methods=['GET'])
def headaches_by_trigger():
    """
    API endpoint to retrieve headache counts grouped by dietary triggers.

    Returns:
        JSON response with a list of triggers and the number of headaches associated
        with each, along with a HTTP 200 status code.
    """
    tracker = HeadacheTracker("myapp/headache.db")
    try:
        cursor = tracker.db_manager.get_cursor()
        cursor.execute('''
        SELECT Diet, COUNT(*) AS headache_count
        FROM triggers
        GROUP BY Diet
        ''')
        records = cursor.fetchall()
        result = [{'trigger': row[0], 'headache_count': row[1]} for row in records]
        return jsonify(result), 200
    finally:
        tracker.close()


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
