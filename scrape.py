import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import re

today = datetime.now().strftime('%d/%m/%Y')
url = f"https://www.drikpanchang.com/muhurat/hora.html?geoname-id=5909629&date={today}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Verify location
title = soup.title.string if soup.title else ""
location_match = re.search(r'for Brossard', title)

if not location_match:
    exit(1)

def to_24hr(time_12):
    """Convert '07:34AM' → '07:34', '12:43PM' → '12:43', '01:27PM' → '13:27'"""
    time_12 = time_12.strip().upper()
    if len(time_12) < 5:
        return "00:00"
    
    time_part = time_12[:-2]  # Remove AM/PM
    try:
        hr, minute = map(int, time_part.split(':'))
    except:
        return "00:00"
    
    if 'PM' in time_12 and hr != 12:
        hr += 12
    elif 'AM' in time_12 and hr == 12:
        hr = 0
    
    return f"{hr:02d}:{minute:02d}"

def parse_row_times(full_text):
    """Extract times from 'Mars - Aggressive11:59AMto12:43PM' → '11:59-12:43'"""
    time_match = re.search(r'(\d{1,2}:\d{2}(?:AM|PM))to(\d{1,2}:\d{2}(?:AM|PM))', full_text)
    if time_match:
        start_12, end_12 = time_match.groups()
        start_24 = to_24hr(start_12)
        end_24 = to_24hr(end_12)
        return f"{start_24}-{end_24}"
    return "00:00-00:00"

# Extract hora data
mhurta_divs = soup.find_all('div', class_='dpMuhurtaRow')
running_hora = soup.find('div', class_='dpPHeaderLeftTitle')

output = []
hora_data = []

output.append("=== RUNNING HORA ===")
output.append(running_hora.text.strip() if running_hora else "Not found")
output.append("")

output.append("=== ALL HORA ROWS (12hr → 24hr) ===")
for i, div in enumerate(mhurta_divs):
    full_text = div.get_text(strip=True)
    time_24hr = parse_row_times(full_text)
    hora_name = full_text.split(' - ')[0] if ' - ' in full_text else full_text
    
    hora_data.append({
        'row': i+1,
        'hora': hora_name,
        'time_12hr': full_text,
        'time_24hr': time_24hr
    })
    output.append(f"Row {i+1}: {time_24hr} {full_text}")

# Save to text file
txt_filename = f"brossard_hora_{today.replace('/', '-')}.txt"
with open(txt_filename, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

meaning_filename = "meaning.txt"
with open(  txt_filename, 'a', encoding='utf-8') as f:
    if os.path.exists(meaning_filename):
        with open(meaning_filename, 'r', encoding='utf-8') as mf:
            f.write('\n\n')
            f.write(mf.read())
# Save structured JSON
json_filename = f"brossard_hora_{today.replace('/', '-')}.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump({'date': today, 'location': 'Brossard', 'running_hora': running_hora.text.strip() if running_hora else None, 'horas': hora_data}, f, indent=2)


