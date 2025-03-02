# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# urls = [
#     'https://visa.nadra.gov.pk/list-of-hospitals/',
#     'https://www.urdupoint.com/business/directory/158/hospitals-and-clinics.html'
# ]

# headers = {'User-Agent': 'Mozilla/5.0'}
# hospitals = []

# for url in urls:
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')

#         for item in soup.find_all('div', class_='hospital-list-item'):
#             name = item.find('h2').text if item.find('h2') else 'N/A'
#             location = item.find('span', class_='location').text if item.find('span', class_='location') else 'N/A'
#             fees = item.find('span', class_='fees').text if item.find('span', class_='fees') else 'N/A'
#             timings = item.find('span', class_='timings').text if item.find('span', class_='timings') else 'N/A'
#             specialty = item.find('span', class_='specialty').text if item.find('span', class_='specialty') else 'N/A'

#             hospitals.append([name, location, fees, timings, specialty])
#     else:
#         print(f"Failed to retrieve data from {url}")

# # Convert to DataFrame and save to CSV
# df = pd.DataFrame(hospitals, columns=['Name', 'Location', 'Fees', 'Timings', 'Specialty'])
# df.to_csv('hospital_data.csv', index=False)  


# import requests

# URL = "https://visa.nadra.gov.pk/list-of-hospitals/"
# page = requests.get(URL)

# print(page.text)

# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# urls = [
#     'https://visa.nadra.gov.pk/list-of-hospitals/',
# ]

# headers = {'User-Agent': 'Mozilla/5.0'}
# hospitals = []

# for url in urls:
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')

#         data=soup.find_all('td')
#     else:
#         print(f"Failed to retrieve data from {url}")
 
# print(data)

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

import requests
from bs4 import BeautifulSoup
import pandas as pd

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
            hospitals.append(row)
    else:
        print(f"Failed to retrieve data from {url}")

# Print each hospital in a readable format
for idx, hospital in enumerate(hospitals, start=1):
    print(f"\nHospital {idx}:")
    print(f"  Name: {hospital[1]}")
    print(f"  City: {hospital[2]}")
    print(f"  Province: {hospital[3]}")
    print(f"  Website: {hospital[4]}")
    print(f"  Address: {hospital[5]}")
    print(f"  Specialization: {hospital[6]}")
    print(f"  Contact Person: {hospital[7]}")
    print(f"  Phone: {hospital[8]}")
