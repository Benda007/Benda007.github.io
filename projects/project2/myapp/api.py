from flask import Flask, request, jsonify, render_template
from myapp.db import HeadacheTracker, DatabaseManager
from myapp.core import get_headaches_by_trigger, filter_criteria as core_filter_criteria
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


@app.route('/api/filter', methods=['POST'])
def filter_records_api():
    """
    API endpoint to filter headache records based on criteria.
    
    Request Body (JSON):
        - user_name: str (optional)
        - start_date: str (YYYY-MM-DD, optional)
        - end_date: str (YYYY-MM-DD, optional)
        - medication: str (optional)
        - diet: str (optional)
        - sleep: str (optional)
        - stress: str (optional)
        - effectiveness: str (Yes/No, optional)
        - intensity: int (optional)
    
    Returns:
        JSON response with filtered records and column names.
    """
    if not request.json:
        return jsonify({"error": "Request must be in JSON format."}), 400
    
    try:
        data = request.json
        filter_criteria = {
            'user_name': data.get('user_name', '').strip().title() or None,
            'start_date': data.get('start_date', '').strip() or None,
            'end_date': data.get('end_date', '').strip() or None,
            'medication': data.get('medication', '').strip().title() or None,
            'diet': data.get('diet', '').strip().title() or None,
            'sleep': data.get('sleep', '').strip().title() or None,
            'stress': data.get('stress', '').strip().title() or None,
            'effectiveness': data.get('effectiveness') or None,
            'intensity': data.get('intensity') or None,
        }
        
        tracker = HeadacheTracker("myapp/headache.db")
        try:
            records, column_names = core_filter_criteria(tracker, filter_criteria)
            return jsonify({
                "records": records,
                "columns": column_names,
                "count": len(records)
            }), 200
        finally:
            tracker.close()
            
    except Exception as e:
        app.logger.error(f"Error filtering records: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/edit/<int:record_id>', methods=['PUT'])
def edit_record_api(record_id):
    """
    API endpoint to edit a headache record by ID.
    
    Args:
        record_id: int - The ID of the headache record to edit
        
    Request Body (JSON):
        Any fields that need to be updated (date, time, duration, intensity, etc.)
    
    Returns:
        JSON response indicating success or error.
    """
    if not request.json:
        return jsonify({"error": "Request must be in JSON format."}), 400
    
    try:
        tracker = HeadacheTracker("myapp/headache.db")
        try:
            tracker.edit_record(record_id, request.json)
            return jsonify({"message": f"Record {record_id} updated successfully."}), 200
        finally:
            tracker.close()
            
    except Exception as e:
        app.logger.error(f"Error editing record: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/delete/<int:record_id>', methods=['DELETE'])
def delete_record_api(record_id):
    """
    API endpoint to delete a headache record by ID.
    
    Args:
        record_id: int - The ID of the headache record to delete
    
    Returns:
        JSON response indicating success or error.
    """
    try:
        tracker = HeadacheTracker("myapp/headache.db")
        try:
            tracker.delete_record(record_id)
            return jsonify({"message": f"Record {record_id} deleted successfully."}), 200
        finally:
            tracker.close()
            
    except Exception as e:
        app.logger.error(f"Error deleting record: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/unique-values', methods=['GET'])
def get_unique_values():
    """
    API endpoint to retrieve unique values for filtering options.
    
    Query Parameters:
        - field: str - The database field to get unique values for
                      (users.user_name, headaches.date, medications.medication, 
                       triggers.diet, triggers.sleep_quality, triggers.stress_level, headaches.intensity)
    
    Returns:
        JSON response with list of unique values.
    """
    field = request.args.get('field')
    
    if not field:
        return jsonify({"error": "field parameter is required"}), 400
    
    try:
        tracker = HeadacheTracker("myapp/headache.db")
        try:
            values = tracker.get_unique_values(field)
            return jsonify({"field": field, "values": values}), 200
        finally:
            tracker.close()
            
    except Exception as e:
        app.logger.error(f"Error getting unique values: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/stop', methods=['GET'])
def stop_server():
    """
    Endpoint to gracefully stop the Flask server when returning to CLI.
    
    Returns:
        JSON response indicating that the user should stop the server.
    """
    return jsonify({
        "message": "To return to CLI, please press Ctrl+C in your terminal to stop the web server.",
        "instruction": "The CLI menu will automatically reappear after you stop the server."
    }), 200


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
