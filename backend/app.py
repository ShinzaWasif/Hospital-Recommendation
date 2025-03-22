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

# from flask import Flask, request, jsonify
# import nltk
# from nltk.tokenize import word_tokenize
# from fuzzywuzzy import process
# import json
# from flask_cors import CORS
# import re

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend communication

# nltk.download("punkt")

# # Load hospital data
# with open("hospitals.json", "r", encoding="utf-8") as file:
#     hospital_data = json.load(file)

# # Function to extract city from query (if mentioned)
# def extract_city_from_query(query):
#     query_tokens = set(word_tokenize(query.lower()))
#     possible_cities = {hospital["City"].lower() for hospital in hospital_data}

#     for city in possible_cities:
#         if city in query_tokens:
#             return city
#     return None

# # Function to extract fee range from query
# def extract_fee_range(query):
#     match = re.search(r"(\d+)\s*-\s*(\d+)", query)
#     if match:
#         return int(match.group(1)), int(match.group(2))  # Return min and max fees
#     return None, None

# # Function to check if a hospital falls within the requested fee range
# def is_within_fee_range(hospital_fee, min_fee, max_fee):
#     match = re.search(r"(\d+)\s*-\s*(\d+)", hospital_fee)
#     if match:
#         hospital_min_fee, hospital_max_fee = int(match.group(1)), int(match.group(2))
#         return (hospital_min_fee <= max_fee and hospital_max_fee >= min_fee)
#     return False

# # Function to find matching hospitals
# def find_matching_hospitals(query):
#     query = query.lower().strip()
#     query_tokens = set(word_tokenize(query))
#     city_filter = extract_city_from_query(query)
#     min_fee, max_fee = extract_fee_range(query)

#     exact_matches = []
#     fuzzy_candidates = []
#     specializations_dict = {}

#     for hospital in hospital_data:
#         specialization = hospital["Specialization"].lower()
#         hospital_city = hospital["City"].lower()
#         hospital_fee = hospital.get("Fees", "")

#         specializations_dict[specialization] = hospital
#         specialization_tokens = set(word_tokenize(specialization))

#         # Check specialization match
#         if query in specialization or query_tokens & specialization_tokens:
#             if city_filter and hospital_city != city_filter:
#                 continue
#             if min_fee and max_fee and not is_within_fee_range(hospital_fee, min_fee, max_fee):
#                 continue
#             exact_matches.append(hospital)

#     # Fuzzy matching if no exact match is found
#     if not exact_matches:
#         fuzzy_results = process.extract(query, specializations_dict.keys(), limit=10)
#         for best_match, score in fuzzy_results:
#             if score > 70:
#                 hospital = specializations_dict[best_match]
#                 hospital_city = hospital["City"].lower()
#                 hospital_fee = hospital.get("Fees", "")

#                 if city_filter and hospital_city != city_filter:
#                     continue
#                 if min_fee and max_fee and not is_within_fee_range(hospital_fee, min_fee, max_fee):
#                     continue
#                 fuzzy_candidates.append(hospital)

#     final_results = exact_matches + fuzzy_candidates
#     return final_results if final_results else None

# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     data = request.get_json()
#     user_query = data.get("query", "").strip()

#     if not user_query:
#         return jsonify({"response": "Please provide a valid query."})

#     matching_hospitals = find_matching_hospitals(user_query)

#     if matching_hospitals:
#         return jsonify({"response": matching_hospitals})
#     else:
#         return jsonify({"response": "Sorry, no matching hospitals found."})

# if __name__ == "__main__":
#     app.run(debug=True)
# from flask import Flask, request, jsonify
# import nltk
# from nltk.tokenize import word_tokenize
# from fuzzywuzzy import process
# import json
# from flask_cors import CORS
# import re

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend communication

# nltk.download("punkt")

# # Load hospital data
# with open("hospitals.json", "r", encoding="utf-8") as file:
#     hospital_data = json.load(file)

# # Function to extract city from query (if mentioned)
# def extract_city_from_query(query):
#     query_tokens = set(word_tokenize(query.lower()))
#     possible_cities = {hospital["City"].lower() for hospital in hospital_data if "City" in hospital}
    
#     for city in possible_cities:
#         if city in query_tokens:
#             return city
#     return None

# # Function to extract fee range or single fee from query
# def extract_fee_from_query(query):
#     range_match = re.search(r"(\d+)\s*-\s*(\d+)", query)
#     single_match = re.search(r"(\d{4,6})", query)  # Match a number with 4-6 digits
    
#     if range_match:
#         return int(range_match.group(1)), int(range_match.group(2))  # Return min and max fees
#     elif single_match:
#         single_fee = int(single_match.group(1))
#         return single_fee, single_fee  # Single amount with no max
#     return None, None

# # Function to check if a hospital should be included based on fee
# def is_within_fee_range(hospital_fee, min_fee, max_fee):
#     match = re.search(r"(\d+)\s*-\s*(\d+)", hospital_fee)
#     if match:
#         hospital_min_fee, hospital_max_fee = int(match.group(1)), int(match.group(2))
        
#         # If single fee is given (e.g., 45000)
#         if min_fee == max_fee:
#             return (hospital_min_fee <= max_fee <= hospital_max_fee) or (hospital_max_fee <= max_fee)
        
#         # If range is given (e.g., 70000-100000)
#         return (hospital_min_fee >= min_fee and hospital_max_fee <= max_fee) or (hospital_min_fee == max_fee)
    
#     return False

# # Function to find matching hospitals
# def find_matching_hospitals(query):
#     query = query.lower().strip()
#     query_tokens = set(word_tokenize(query))
#     city_filter = extract_city_from_query(query)
#     min_fee, max_fee = extract_fee_from_query(query)

#     exact_matches = []
#     fuzzy_candidates = []
#     specializations_dict = {}

#     for hospital in hospital_data:
#         specialization = hospital["Specialization"].lower()
#         hospital_city = hospital.get("City", "").lower()
#         hospital_fee = hospital.get("Fees", "")

#         specializations_dict[specialization] = hospital
#         specialization_tokens = set(word_tokenize(specialization))

#         # Check specialization match
#         if query in specialization or query_tokens & specialization_tokens:
#             if city_filter and hospital_city != city_filter:
#                 continue
#             if min_fee is not None and not is_within_fee_range(hospital_fee, min_fee, max_fee):
#                 continue
#             exact_matches.append(hospital)

#     # Fuzzy matching if no exact match is found
#     if not exact_matches:
#         fuzzy_results = process.extract(query, specializations_dict.keys(), limit=10)
#         for best_match, score in fuzzy_results:
#             if score > 70:
#                 hospital = specializations_dict[best_match]
#                 hospital_city = hospital.get("City", "").lower()
#                 hospital_fee = hospital.get("Fees", "")

#                 if city_filter and hospital_city != city_filter:
#                     continue
#                 if min_fee is not None and not is_within_fee_range(hospital_fee, min_fee, max_fee):
#                     continue
#                 fuzzy_candidates.append(hospital)

#     final_results = exact_matches + fuzzy_candidates
#     return sorted(final_results, key=lambda h: int(re.search(r"(\d+)", h["Fees"]).group(1))) if final_results else None

# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     data = request.get_json()
#     user_query = data.get("query", "").strip()

#     if not user_query:
#         return jsonify({"response": "Please provide a valid query."})

#     matching_hospitals = find_matching_hospitals(user_query)

#     if matching_hospitals:
#         return jsonify({"response": matching_hospitals})
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
import re
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import librosa
import numpy as np
from word2number import w2n

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

nltk.download("punkt")

# Load hospital data
with open("hospitals.json", "r", encoding="utf-8") as file:
    hospital_data = json.load(file)

# Load Wav2Vec 2.0 model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

def convert_numbers(transcription):
    words = transcription.lower()
    try:
        return str(w2n.word_to_num(words))  # Convert words to numbers
    except ValueError:
        return words  # Return original if conversion fails

def extract_number_range(text):
    match = re.findall(r"(\d+[\s\-]*\d*[\s\-]*\d*)", text)
    return match if match else None

def transcribe_audio(audio_path):
    speech, sr = librosa.load(audio_path, sr=16000)
    max_length = 50  # Process 30 seconds at a time
    chunk_size = sr * max_length  
    transcriptions = []
    
    for i in range(0, len(speech), chunk_size):
        chunk = speech[i : i + chunk_size]  
        input_values = processor(chunk, return_tensors="pt", sampling_rate=16000).input_values
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcriptions.append(processor.batch_decode(predicted_ids)[0])
    
    full_transcription = " ".join(transcriptions).lower()
    full_transcription = convert_numbers(full_transcription)
    number_ranges = extract_number_range(full_transcription)
    if number_ranges:
        full_transcription += " " + " ".join(number_ranges)
    
    return full_transcription

# Function to extract city from query (if mentioned)
def extract_city_from_query(query):
    query_tokens = set(word_tokenize(query.lower()))
    possible_cities = {hospital["City"].lower() for hospital in hospital_data if "City" in hospital}
    
    for city in possible_cities:
        if city in query_tokens:
            return city
    return None

# Function to extract fee range or single fee from query
def extract_fee_from_query(query):
    range_match = re.search(r"(\d+)\s*-\s*(\d+)", query)
    single_match = re.search(r"(\d{4,6})", query)  # Match a number with 4-6 digits
    
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))  # Return min and max fees
    elif single_match:
        single_fee = int(single_match.group(1))
        return single_fee, single_fee  # Single amount with no max
    return None, None

# Function to check if a hospital should be included based on fee
def is_within_fee_range(hospital_fee, min_fee, max_fee):
    match = re.search(r"(\d+)\s*-\s*(\d+)", hospital_fee)
    if match:
        hospital_min_fee, hospital_max_fee = int(match.group(1)), int(match.group(2))
        
        if min_fee == max_fee:
            return (hospital_min_fee <= max_fee <= hospital_max_fee) or (hospital_max_fee <= max_fee)
        return (hospital_min_fee >= min_fee and hospital_max_fee <= max_fee) or (hospital_min_fee == max_fee)
    
    return False

# Function to find matching hospitals
def find_matching_hospitals(query):
    query = query.lower().strip()
    query_tokens = set(word_tokenize(query))
    city_filter = extract_city_from_query(query)
    min_fee, max_fee = extract_fee_from_query(query)

    exact_matches = []
    fuzzy_candidates = []
    specializations_dict = {}

    for hospital in hospital_data:
        specialization = hospital["Specialization"].lower()
        hospital_city = hospital.get("City", "").lower()
        hospital_fee = hospital.get("Fees", "")

        specializations_dict[specialization] = hospital
        specialization_tokens = set(word_tokenize(specialization))

        if query in specialization or query_tokens & specialization_tokens:
            if city_filter and hospital_city != city_filter:
                continue
            if min_fee is not None and not is_within_fee_range(hospital_fee, min_fee, max_fee):
                continue
            exact_matches.append(hospital)

    if not exact_matches:
        fuzzy_results = process.extract(query, specializations_dict.keys(), limit=10)
        for best_match, score in fuzzy_results:
            if score > 70:
                hospital = specializations_dict[best_match]
                hospital_city = hospital.get("City", "").lower()
                hospital_fee = hospital.get("Fees", "")

                if city_filter and hospital_city != city_filter:
                    continue
                if min_fee is not None and not is_within_fee_range(hospital_fee, min_fee, max_fee):
                    continue
                fuzzy_candidates.append(hospital)

    final_results = exact_matches + fuzzy_candidates
    return sorted(final_results, key=lambda h: int(re.search(r"(\d+)", h["Fees"]).group(1))) if final_results else None

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_query = data.get("query", "").strip()
    audio_file = data.get("audio")

    if audio_file:
        transcription = transcribe_audio(audio_file)
        user_query = transcription
    
    if not user_query:
        return jsonify({"response": "Please provide a valid query."})

    matching_hospitals = find_matching_hospitals(user_query)

    if matching_hospitals:
        return jsonify({"response": matching_hospitals})
    else:
        return jsonify({"response": "Sorry, no matching hospitals found."})

if __name__ == "__main__":
    app.run(debug=True)
