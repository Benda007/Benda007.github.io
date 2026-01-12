# Headache Tracker
Developed by Jean Kocman
#### Video Demo: [Headache Tracker video](https://youtu.be/kitHMEXwc-g)

#### Description:



The Headache Tracker is a comprehensive application designed to aid users in managing and analyzing their headache episodes. Developed as a final project for the CS50 Python course, this application is built using Python and Flask, providing both command-line and web-based interfaces for user interactions.

## Project Overview

The main objective of the Headache Tracker is to enable users to log, track, and analyze headache occurrences in an organized manner. Users can record the specifics of each headache—such as date, duration, intensity, dietary triggers, stress levels, sleep quality, and the effectiveness of any medications used. These records help users and healthcare professionals identify patterns and possible causes of headaches.

### Key Features

- **Headache Entry and Management**: Add, update, or delete headache records through a command-line interface or a user-friendly web interface.
- **Data Filtering and Viewing**: Search and filter records based on user-specific criteria, making it easier to find trends or particular events.
- **Export Functionality**: Export all recorded data to an Excel spreadsheet for external analysis and record-keeping.
- **User Interface**: A Flask-powered web interface enhances accessibility and ease of use for managing headache data.

### Project Files Overview

**Folder structure**:
```
project
├── README.md
├── myapp/
│   ├── init.py
│   ├── api.py
│   ├── core.py
│   ├── db.py
│   ├── headache.db
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── script.js
│   └── templates/
│       └── index.html
├── project.py
├── requirements.txt
└── test_project.py
```


- **`project.py`**: The main entry point for the application, handling command-line interface operations and initializing various functionalities like record management, data export, and running the web server.

- **`myapp/`**: The core application directory housing all essential modules.
  - **`api.py`**: Sets up the Flask web server and routes to handle HTTP requests for adding, editing, and exporting records.
  - **`core.py`**: Contains business logic for processing and filtering data, maintaining consistency, and validating inputs.
  - **`db.py`**: Manages all database operations, including schema creation and CRUD functions. This file defines key classes for database interaction, such as `DatabaseManager`, `UserManager`, `HeadacheManager`, and `TriggerManager`.
  - **`headache.db`**: The SQLite database storing all recorded headache data.
  - **`templates/`**: Contains HTML templates rendered by Flask, including `index.html`.

- **`test_project.py`**: Houses a suite of tests using `pytest` to validate application functionalities, ensuring correctness in scenarios like record addition, editing, and filtering.

- **`requirements.txt`**: Lists all Python dependencies needed for the application, ensuring a consistent setup environment.

**Command pallete**:

```
usage: project.py [-h] [--web] [--init] [--add] [--filter] [--edit] [--delete] [--export] [--upload] [--file FILE]

Headache Tracker Application

options:
  -h, --help   show this help message and exit
  --web        Run the API server
  --init       Initialize the database
  --add        Add a headache record
  --filter     Filter and view records
  --edit       Edit a headache record
  --delete     Delete a headache record
  --export     Export data to Excel. Use syntax: --export --file name.xlsx
  --upload     Import data from Excel. Use syntax: --upload --file name.xlsx
  --file FILE  Excel file name for import/export
  ```

### Design Choices and Challenges

The decision to implement both command-line and web-based interfaces stems from the need to maximize usability and accessibility. While the command-line interface offers powerful direct control, the web interface simplifies interaction for broader audiences. Furthermore, encapsulating database functions in specific manager classes enhances modularity and eases future development.

### AI Usage

DuckDebugger was a wonderful guide and patient teacher. In addition, I used GPT-4o for refactoring guidance and primarily for sections related to HTML, JS, and CSS parts of my project.

### Future Improvements

Potential future developments include advanced analytics features, such as using machine learning algorithms to predict headache triggers. Additionally, incorporating user authentication would improve data security and personalization. Converting the application to an Android app would also be an interesting challenge. Before these enhancements, implementing even more robust error handling could cover additional edge cases.


### Closing Remarks

The Headache Tracker project offers a practical tool for headache management. It reflects the evolution from learning basic programming concepts to deploying them in real-world applications, providing a robust platform for further enhancements in functionality and user experience.

A big thank you to the entire CS50 team for the outstanding work you do. Thank you!
