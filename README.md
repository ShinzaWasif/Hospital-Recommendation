# Hospital-Recommendation

🏥 AI-Based Hospital Recommendation System
This project is a smart hospital recommendation system developed in Python. It allows users to search for hospitals based on medical specialization, city, and fee range. The system uses the FuzzyWuzzy library to match user queries even when there are spelling mistakes or partial inputs.

🔍 Key Features
Fuzzy Matching: Handles typos and approximate inputs in specialization names.
City Filter: Narrows down search results based on the user’s preferred city.
Fee Range Filter: Lets users search for hospitals within a specified consultation fee range.
Intelligent Suggestions: Returns best-matching hospitals even if exact terms are not entered.

💻 Technologies Used
Python 3
FuzzyWuzzy (for fuzzy string matching)
Python standard libraries

📂 How It Works
The user enters a specialization (e.g., "cardiollogist" instead of "cardiologist").
The system searches for exact matches first.
If no exact match is found, the system uses fuzzy matching to find similar specializations.
It then filters hospitals based on city and fee range if provided.
The final result is a list of matching hospitals shown with details.


🧠 Concepts Demonstrated
Python dictionaries for structured hospital data
String similarity with FuzzyWuzzy
Conditional filtering
Modular code using functions

📽️ YouTube Video Link
https://youtu.be/iUKzhC4drAk?si=EJ9J0QnQCffUWCM8

📎 Project Files
app.py – Main file handling user queries and filtering
beautifulSoup.py - For Web Scraping
hospital.json – Contains sample hospital data
chatbot.jsx – For frontend handling


🙌 Authors:
Project Lead - Syeda Shinza Wasif
Teammate No. 1 – Areeba Batool
Teammate No. 2 – Asifa Siraj

