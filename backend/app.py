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
import time
import random
import os
import pygame
from gtts import gTTS
import threading
import inflect 
import pyttsx3


app = Flask(_name_)
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
    match = re.findall(r"(\d+[\s-]\d[\s-]\d)", text)
    return match if match else None

def transcribe_audio(audio_path):
    speech, sr = librosa.load(audio_path, sr=16000)
    max_length = 50  # Process 50 seconds at a time
    chunk_size = sr * max_length
    transcriptions = []

    for i in range(0, len(speech), chunk_size):
        chunk = speech[i: i + chunk_size]
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

def extract_city_from_query(query):
    query_tokens = set(word_tokenize(query.lower()))
    possible_cities = {hospital["City"].lower() for hospital in hospital_data if "City" in hospital}
    for city in possible_cities:
        if city in query_tokens:
            return city
    return None

def extract_fee_from_query(query):
    range_match = re.search(r"(\d+)\s*-\s*(\d+)", query)
    single_match = re.search(r"(\d{4,6})", query)  # Match a number with 4-6 digits
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))  # Return min and max fees
    elif single_match:
        single_fee = int(single_match.group(1))
        return single_fee, single_fee  # Single amount with no max
    return None, None

def is_within_fee_range(hospital_fee, min_fee, max_fee):
    match = re.search(r"(\d+)\s*-\s*(\d+)", hospital_fee)
    if match:
        hospital_min_fee, hospital_max_fee = int(match.group(1)), int(match.group(2))
        if min_fee == max_fee:
            return (hospital_min_fee <= max_fee <= hospital_max_fee) or (hospital_max_fee <= max_fee)
        return (hospital_min_fee >= min_fee and hospital_max_fee <= max_fee) or (hospital_min_fee == max_fee)
    return False

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

p = inflect.engine()  # Initialize inflect engine

def convert_numbers_to_words(text):
    def replace_number(match):
        num = int(match.group(0))
        return p.number_to_words(num, andword="")  # Convert number to words
    return re.sub(r"\b\d+\b", replace_number, text) 

audio_lock = threading.Lock()  # Global lock to keep thread alive

def speak(hospitals, user_fee_range=None, use_offline_tts=True):
    def tts_worker():
        try:
            if not hospitals:
                text = "Sorry, no matching hospitals found."
            else:
                hospital_info = []
                for hospital in hospitals:
                    name = hospital.get("Name", "Unknown Hospital")
                    city = hospital.get("City", "Unknown Location")
                    hospital_fees = hospital.get("Fees", "Not Available")

                    hospital_fees = re.sub(r"\b0+\b", "zero", hospital_fees)
                    hospital_fees = convert_numbers_to_words(hospital_fees)

                    user_fee_text = ""
                    if user_fee_range:
                        min_fee, max_fee = user_fee_range
                        user_fee_text = f"Your fee range is {convert_numbers_to_words(str(min_fee))} to {convert_numbers_to_words(str(max_fee))}."

                    hospital_text = f"{name}, located in {city}. Hospital fee range is {hospital_fees}. {user_fee_text}"
                    hospital_info.append(hospital_text)

                text = "Dear user, according to your search following are the hospitals. " + " ".join(hospital_info) + " For more, please visit the website."

            if use_offline_tts:
                engine = pyttsx3.init()
                
                # Try to set Indian English voice
                voices = engine.getProperty("voices")
                indian_voice = None
                for voice in voices:
                    if "en-in" in voice.id.lower() or "india" in voice.name.lower():
                        indian_voice = voice.id
                        break
                if indian_voice:
                    engine.setProperty("voice", indian_voice)
                engine.setProperty("rate", 165)

                with audio_lock:
                    engine.say(text)
                    engine.runAndWait()
            else:
                # Online fallback using gTTS
                tts = gTTS(text, lang="en", tld="co.in")
                temp_filename = f"temp_audio_{int(time.time())}_{random.randint(1000, 9999)}.mp3"
                temp_path = os.path.join(os.getcwd(), temp_filename)
                tts.save(temp_path)

                with audio_lock:
                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_path)
                    pygame.mixer.music.play()

                    while pygame.mixer.music.get_busy():
                        pygame.time.delay(500)

                    pygame.mixer.quit()

                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except PermissionError:
                        print("Could not delete temp file immediately.")

        except Exception as e:
            print(f"Error in speak function: {e}")

    threading.Thread(target=tts_worker).start()

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
        response_json = jsonify({"response": matching_hospitals})
        threading.Thread(target=speak, args=(matching_hospitals,)).start()
        return response_json
    else:
        return jsonify({"response": "Sorry, no matching hospitals found."})

if _name_ == "_main_":
    app.run(debug=True)