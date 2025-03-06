# from flask import Flask, jsonify
# from flask_cors import CORS
# import json
# import nltk

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend communication

# # Load JSON data before defining routes
# with open("hospitals.json", "r", encoding="utf-8") as file:
#     hospitals = json.load(file)

# @app.route("/")  # Define a route for "/"
# def home():
#     return "Hello, Flask is running!"

# @app.route('/hospitals', methods=['GET'])
# def get_hospitals():
#     return jsonify(hospitals)

# if __name__ == "__main__":
#     app.run(debug=True)  # Only run Flask once!


from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from fuzzywuzzy import process
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

nltk.download('punkt_tab')
# Load hospital data
with open("hospitals.json", "r", encoding="utf-8") as file:
    hospital_data = json.load(file)

# Function to find best hospital match
def find_best_hospital(query):
    query_tokens = word_tokenize(query.lower())

    best_match = None
    best_score = 0

    for hospital in hospital_data:
        hospital_info = f"{hospital['Name']} {hospital['City']} {hospital['Specialization']}"
        match_score = process.extractOne(query, [hospital_info])[1]

        if match_score > best_score:
            best_score = match_score
            best_match = hospital

    return best_match

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"response": "Please provide a valid query."})

    best_hospital = find_best_hospital(user_query)

    if best_hospital:
        response_text = (
            f"Hospital: {best_hospital['Name']}\n"
            f"City: {best_hospital['City']}, {best_hospital['Province']}\n"
            f"Specialization: {best_hospital['Specialization']}\n"
            f"Phone: {best_hospital['Phone']}\n"
            f"Address: {best_hospital['Address']}\n"
            f"Website: {best_hospital['Website'] if best_hospital['Website'] != '-' else 'N/A'}"
        )
    else:
        response_text = "Sorry, I couldn't find any hospital matching your query."

    return jsonify({"response": response_text})

if __name__ == "__main__":
    nltk.download("punkt")
    app.run(debug=True)
