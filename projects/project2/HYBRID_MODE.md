# Headache Tracker - Hybrid CLI/Web Mode

## Overview

The application now runs in **hybrid mode**, where users can choose between:
- **CLI (Command Line Interface)** - text menu in the terminal
- **Web Interface (HTML)** - web interface in a browser

## How to Run the Application

### Standard Launch (Interactive Menu)

```bash
python project.py
```

An interactive menu will be displayed:

```
============================================================
📋 HEADACHE TRACKER - Main Menu
============================================================
1. View all records
2. Add a new headache record
3. Filter records by criteria
4. Edit or delete a record
5. Export records to Excel
6. Import records from Excel
7. Switch to Web Interface (HTML)
8. Exit
============================================================
```

### Running Commands from Terminal (CLI mode)

You can still use command-line arguments as before:

```bash
# Add a new record
python project.py --add

# Filter records
python project.py --filter

# Edit/Delete records
python project.py --edit
python project.py --delete

# Export to Excel
python project.py --export --file data.xlsx

# Import from Excel
python project.py --upload --file data.xlsx

# View all records
python project.py

# Launch web interface directly
python project.py --web
```

## Switching Between CLI and Web Interface

### CLI → Web Interface

1. In the interactive menu, select option **7** (Switch to Web Interface)
2. The web interface will open in your browser (http://localhost:5000)
3. You can choose between:
   - Adding new records
   - Viewing the records table
   - Viewing graphs
   - Filtering records

### Web Interface → CLI

1. On the web page, click the **⬅️ Return to CLI** button at the top
2. A window with instructions will appear
3. Press **Ctrl+C** in the terminal
4. The CLI menu will automatically return

## Application Structure

```
project2/
├── project.py                 # Main entry point with CLI menu
├── myapp/
│   ├── api.py                 # Flask web server
│   ├── db.py                  # Database logic
│   ├── core.py                # Filtering and logic
│   ├── headache.db            # SQLite database
│   ├── templates/
│   │   └── index.html         # Web frontend
│   └── static/
│       ├── js/
│       │   └── script.js       # JavaScript for web
│       └── css/
│           └── styles.css     # Styling
├── requirements.txt
└── Procfile                   # For Render.com
```

## Render.com Deployment

On Render.com, the application is launched by default in CLI interactive menu:

```
Build Command: pip install -r requirements.txt
Start Command: python project.py
```

The project runs in default CLI mode, where users can:
1. Select one of the 8 CLI menu options
2. Or open the web interface if they prefer a graphical UI

## API Endpoints (for web interface)

The web interface communicates with these API endpoints:

- **GET** `/` - Home page (HTML)
- **POST** `/add` - Add a new record
- **GET** `/records` - View all records
- **GET** `/headaches_by_trigger` - Statistics by triggers
- **POST** `/api/filter` - Filter records
- **PUT** `/api/edit/<id>` - Edit a record
- **DELETE** `/api/delete/<id>` - Delete a record
- **GET** `/api/unique-values` - Available values for filters
- **GET** `/api/stop` - Information about returning to CLI

## Key Benefits

✅ **Minimal Changes** - Existing code remains unchanged
✅ **Flexibility** - Users can choose what works best (CLI or Web)
✅ **Seamless Switching** - Easy to switch between both modes
✅ **Render.com Compatible** - Works without any issues
✅ **Full Features** - All operations available in both modes

## Usage Examples

### Scenario 1: CLI Only
```bash
python project.py
# Select menu → Select operation → Return to menu
# Repeats until user selects "Exit" (8)
```

### Scenario 2: Web Only
```bash
python project.py --web
# Opens http://localhost:5000
# User works in the browser
# Ctrl+C stops the server
```

### Scenario 3: Hybrid (CLI + Web)
```bash
python project.py
# Menu → Select "Switch to Web Interface" (7)
# Web interface opens
# Click "Return to CLI"
# Ctrl+C → Return to menu
```

## Deployment Notes

### Local Machine (python project.py)
- CLI interactive menu is available
- You can switch to web interface (option 7)
- Web server runs on `http://localhost:5000`
- You can return to CLI by pressing Ctrl+C

### Render.com Deployment
- **Only web interface is available** (no interactive CLI)
- Web server runs on your Render.com URL
- The "About CLI Mode" button provides information
- To use CLI mode, run the application locally

This is intentional - Render.com is a web hosting platform, not a terminal environment.

**Q: The "Return to CLI" button doesn't work**
A: It's a design feature - simply press Ctrl+C in the terminal

**Q: The server won't stop**
A: Press Ctrl+C in the terminal where the server is running

**Q: Port 5000 is already in use**
A: Change the PORT: `PORT=8000 python project.py --web`

## Conclusion

The application now offers the best of both worlds:
- **CLI** for quick operations and scripting
- **Web** for intuitive and visual interaction

Switching between them is smooth and user-friendly! 🎉
