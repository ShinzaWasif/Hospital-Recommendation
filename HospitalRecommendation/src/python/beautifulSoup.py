# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# url = 'https://visa.nadra.gov.pk/list-of-hospitals/'
# headers = {'User-Agent': 'Mozilla/5.0'}

# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
#     table = soup.find('table')  # Find the table in the HTML
#     rows = table.find_all('tr')  # Find all rows in the table
    
#     data = []
#     for row in rows:
#         cols = row.find_all('td')  # Find all columns
#         cols = [col.text.strip() for col in cols]  # Clean text
#         if cols:
#             data.append(cols)  # Add row data to list
    
#     # Create DataFrame
#     df = pd.DataFrame(data, columns=["ID", "Hospital Name", "City", "Province", "Website", "Address", "Specialty", "Contact Person", "Contact"])
#     print(df)
# else:
#     print("Failed to retrieve the webpage.")
# print(data)

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# urls = ['https://visa.nadra.gov.pk/list-of-hospitals/']
# headers = {'User-Agent': 'Mozilla/5.0'}
# hospitals = []

# for url in urls:
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         data = soup.find_all('td')
        
#         # Assuming there are 9 columns in each row
#         columns = 9
#         for i in range(0, len(data), columns):
#             row = [cell.get_text(strip=True) for cell in data[i:i+columns]]
#             hospitals.append(row)
#     else:
#         print(f"Failed to retrieve data from {url}")

# # Print each hospital in a readable format
# for idx, hospital in enumerate(hospitals, start=1):
#     print(f"\nHospital {idx}:")
#     print(f"  Name: {hospital[1]}")
#     print(f"  City: {hospital[2]}")
#     print(f"  Province: {hospital[3]}")
#     print(f"  Website: {hospital[4]}")
#     print(f"  Address: {hospital[5]}")
#     print(f"  Specialization: {hospital[6]}")
#     print(f"  Contact Person: {hospital[7]}")
#     print(f"  Phone: {hospital[8]}")

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
with open("hospitals.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_output)

# Print JSON
print(json_output)


# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# urls = ['https://visa.nadra.gov.pk/list-of-hospitals/']
# headers = {'User-Agent': 'Mozilla/5.0'}
# hospitals = []

# for url in urls:
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         data = soup.find_all('td')
        
#         # Assuming there are 9 columns in each row
#         columns = 9
#         for i in range(0, len(data), columns):
#             row = [cell.get_text(strip=True) for cell in data[i:i+columns]]
            
#             if len(row) == columns:  # Ensure complete data
#                 hospitals.append(row)
#     else:
#         print(f"Failed to retrieve data from {url}")

# # Convert to DataFrame
# df = pd.DataFrame(hospitals, columns=[
#     "ID", "Name", "City", "Province", "Website", "Address", "Specialization", "Contact Person", "Phone"
# ])

# # Save to CSV
# df.to_csv("hospitals.csv", index=False, encoding="utf-8")

# print("CSV file 'hospitals.csv' has been created successfully!")

