from flask import Flask, flash, render_template, request, session
from flask_session import Session
import sqlite3

# Configure application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
