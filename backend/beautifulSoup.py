import requests
from bs4 import BeautifulSoup
import json

urls = ['https://visa.nadra.gov.pk/list-of-hospitals/']
headers = {'User-Agent': 'Mozilla/5.0'}
hospitals = []

for url in urls:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('td')
        
        # Assuming there are 9 columns in each row
        columns = 9
        for i in range(0, len(data), columns):
            row = [cell.get_text(strip=True) for cell in data[i:i+columns]]
            
            if len(row) == columns:  # Ensure complete data
                hospital = {
                    "Name": row[1],
                    "City": row[2],
                    "Province": row[3],
                    "Website": row[4],
                    "Address": row[5],
                    "Specialization": row[6],
                    "ContactPerson": row[7],
                    "Phone": row[8]
                }
                hospitals.append(hospital)
    else:
        print(f"Failed to retrieve data from {url}")

# Convert to JSON
json_output = json.dumps(hospitals, indent=4)

# Save to a file
with open("h.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_output)

# Print JSON
print(json_output)