from flask import Flask, jsonify
from flask_cors import CORS
import json
import nltk

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load JSON data before defining routes
with open("hospitals.json", "r", encoding="utf-8") as file:
    hospitals = json.load(file)

@app.route("/")  # Define a route for "/"
def home():
    return "Hello, Flask is running!"

@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    return jsonify(hospitals)

if __name__ == "__main__":
    app.run(debug=True)  # Only run Flask once!
