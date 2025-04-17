#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 10:11:56 2024

@author: rabinson
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for scraping
BASE_URL = "https://www.gunviolencearchive.org/mass-shooting?page={}"

# Spoofing headers to appear as a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Columns for the CSV
columns = ["Incident ID", "Incident Date", "State", " City Or County", "Address", "Killed", "Injured"]

# Function to scrape a single page and extract data
def scrape_page(url):
    response = requests.get(url, headers=HEADERS)  # Add headers here
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {url}, Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Locate the table
    table = soup.find("table", {"class": "sticky-enabled"})
    if not table:
        raise Exception("Could not find the table on the page.")
    
    rows = table.find_all("tr")[1:]  # Exclude the header row
    data = []
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 6:
            continue  # Skip rows with incomplete data
        # Extract data from each cell
        incident_id = cells[0].get_text(strip=True)
        incident_date = cells[1].get_text(strip=True)
        # Convert date to dd/mm/yyyy format
        try:
            incident_date = pd.to_datetime(incident_date, format="%B %d, %Y").strftime("%d/%m/%Y")
        except ValueError:
            incident_date = "Invalid Date"
        state = cells[2].get_text(strip=True)
        city_or_county = cells[3].get_text(strip=True)
        address = cells[4].get_text(strip=True)
        killed = cells[5].get_text(strip=True)
        injured = cells[6].get_text(strip=True)
        
        data.append([incident_id, incident_date, state, city_or_county, address, killed, injured])
    
    return data

# Scrape all pages and save data
all_data = []
for page_num in range(80):  # Loop through pages 0 to 79
    print(f"Scraping page {page_num + 1}/80...")
    try:
        url = BASE_URL.format(page_num)
        page_data = scrape_page(url)
        all_data.extend(page_data)
    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")
        continue

# Save data to CSV
if all_data:
    df = pd.DataFrame(all_data, columns=columns)
    df.to_csv("mass_shootings_final.csv", index=False)
    print("All data successfully saved to mass_shootings_all_pages.csv")
else:
    print("No data scraped.")