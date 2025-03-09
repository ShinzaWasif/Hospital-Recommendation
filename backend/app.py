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




# from flask import Flask, request, jsonify
# import nltk
# from nltk.tokenize import word_tokenize
# from fuzzywuzzy import process
# import json
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS to allow frontend requests

# nltk.download("punkt")

# # Load hospital data
# with open("hospitals.json", "r", encoding="utf-8") as file:
#     hospital_data = json.load(file)

# # Function to find the best matching hospitals
# def find_matching_hospitals(query):
#     query_tokens = word_tokenize(query.lower())
#     matches = []

#     for hospital in hospital_data:
#         hospital_info = f"{hospital['Name']} {hospital['City']} {hospital['Specialization']}"
#         match_score = process.extractOne(query, [hospital_info])[1]

#         if match_score > 50:  # Threshold to filter relevant hospitals
#             matches.append((hospital, match_score))

#     matches.sort(key=lambda x: x[1], reverse=True)  # Sort by relevance
#     return [hospital[0] for hospital in matches]  # Return hospital details

# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     data = request.get_json()
#     user_query = data.get("query", "")

#     if not user_query:
#         return jsonify({"response": "Please provide a valid query."})

#     matching_hospitals = find_matching_hospitals(user_query)

#     if matching_hospitals:
#         response_texts = [
#             (
#                 f"Hospital: {hospital['Name']}\n"
#                 f"City: {hospital['City']}, {hospital['Province']}\n"
#                 f"Specialization: {hospital['Specialization']}\n"
#                 f"Phone: {hospital['Phone']}\n"
#                 f"Address: {hospital['Address']}\n"
#                 f"Website: {hospital['Website'] if hospital['Website'] != '-' else 'N/A'}"
#             )
#             for hospital in matching_hospitals
#         ]
#         return jsonify({"response": "\n\n".join(response_texts)})
#     else:
#         return jsonify({"response": "Sorry, no matching hospitals found."})

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from fuzzywuzzy import process
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

nltk.download("punkt")

# Load hospital data
with open("hospitals.json", "r", encoding="utf-8") as file:
    hospital_data = json.load(file)

# Function to extract city from query (if mentioned)
def extract_city_from_query(query):
    query_tokens = set(word_tokenize(query.lower()))
    possible_cities = {hospital["City"].lower() for hospital in hospital_data}

    # Check if any word in query matches a city
    for city in possible_cities:
        if city in query_tokens:
            return city
    return None

# Function to find matching hospitals
def find_matching_hospitals(query):
    query = query.lower().strip()
    query_tokens = set(word_tokenize(query))  # Tokenize query for better matching
    city_filter = extract_city_from_query(query)  # Extract city if mentioned

    exact_matches = []
    fuzzy_candidates = []
    specializations_dict = {}

    # **Collect all hospitals in a dictionary for fuzzy matching**
    for hospital in hospital_data:
        specialization = hospital["Specialization"].lower()
        hospital_city = hospital["City"].lower()
        specializations_dict[specialization] = hospital

        # **Strict word match (full token or phrase match)**
        specialization_tokens = set(word_tokenize(specialization))
        
        # Check if query matches specialization
        if query in specialization or query_tokens & specialization_tokens:
            if city_filter:
                # If city is mentioned, match only hospitals in that city
                if hospital_city == city_filter:
                    exact_matches.append(hospital)
            else:
                exact_matches.append(hospital)

    # **Fuzzy matching only if exact matches are missing**
    if not exact_matches:
        fuzzy_results = process.extract(query, specializations_dict.keys(), limit=10)  # Get top 10 results

        for best_match, score in fuzzy_results:
            if score > 70:  # Adjustable threshold
                hospital = specializations_dict[best_match]
                if city_filter:
                    if hospital["City"].lower() == city_filter:
                        fuzzy_candidates.append(hospital)
                else:
                    fuzzy_candidates.append(hospital)

    # Combine exact matches with fuzzy ones, ensuring no duplicates
    final_results = exact_matches + fuzzy_candidates
    return final_results if final_results else None

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query:
        return jsonify({"response": "Please provide a valid query."})

    matching_hospitals = find_matching_hospitals(user_query)

    if matching_hospitals:
        return jsonify({"response": matching_hospitals})
    else:
        return jsonify({"response": "Sorry, no matching hospitals found."})

if __name__ == "__main__":
    app.run(debug=True)
