#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:17:32 2024

@author: rabinson
"""

import pandas as pd
from geopy.geocoders import Nominatim
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the CSV file
input_file = 'mass_shootings_all_pages.csv'  
output_file = 'mass_shootings_with_lat_and_long.csv'
df = pd.read_csv(input_file)

# Clean column names
df.columns = df.columns.str.strip()

# Check column names after cleaning
logging.info(f"Columns in the CSV file: {df.columns}")

# Update required column names based on your CSV
city_column = 'City Or County'
state_column = 'State'

# Check if required columns exist
required_columns = [city_column, state_column]
for col in required_columns:
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in the CSV file. Available columns: {df.columns}")

# Initialize geocoder
geolocator = Nominatim(user_agent="geoapi")

# Create empty lists for latitudes and longitudes
latitudes = []
longitudes = []

# Function to get latitude and longitude
def get_coordinates(location):
    try:
        geocode = geolocator.geocode(location)
        if geocode:
            return geocode.latitude, geocode.longitude
        else:
            return None, None
    except Exception as e:
        logging.warning(f"Error geocoding {location}: {e}")
        return None, None

# Iterate through the locations in the DataFrame
for index, row in df.iterrows():
    location = f"{row[city_column]}, {row[state_column]}"
    logging.info(f"Geocoding: {location}")
    lat, lon = get_coordinates(location)
    latitudes.append(lat)
    longitudes.append(lon)
    time.sleep(1.0)  # To avoid hitting rate limits

# Add latitudes and longitudes to the DataFrame
df['Latitude'] = [lat if lat is not None else "Not Found" for lat in latitudes]
df['Longitude'] = [lon if lon is not None else "Not Found" for lon in longitudes]

# Save the updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)
logging.info(f"Updated CSV saved to {output_file}")
