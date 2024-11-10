#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('pip', 'install mplleaflet')
import requests
import pandas as pd
import numpy as np
import mplleaflet
import folium
from IPython.display import display, clear_output
import time


# In[2]:


japan_airports=pd.read_csv('japan_airports.csv', delimiter=';')
japan_airports=japan_airports[['Airport Code', 'Latitude', 'Longitude']]
japan_airports=japan_airports[japan_airports['Latitude'] > 30]
#japan_airports


# In[3]:


# Define columns
columns = ['callsign', 'origin_country', 'long', 'lat','true_track']
all_columns = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
                   'long', 'lat', 'baro_altitude', 'on_ground', 'velocity',
                   'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source']

# Define Area over Japan
lon_min, lat_min=128, 30
lon_max, lat_max=149, 46

# Your OpenSkyAPI logins
user_name = '' 
password = ''

# Get flight data from OpenSkyAPI (please be mindful of the request limits)
def get_flight_data():
    url = f'https://{user_name}:{password}@opensky-network.org/api/states/all?' \
          f'lamin={lat_min}&lomin={lon_min}&lamax={lat_max}&lomax={lon_max}'
    response = requests.get(url)
    data = response.json()
    
    flights = pd.DataFrame(data['states'], columns=all_columns)[columns]
    flights = flights[~((flights['lat']>=34)&(flights['lat']<=41)&(flights['long']>=125)&(flights['long']<=130))] #exclude unneeded regions 
    flights = flights[~((flights['lat']>=42)&(flights['lat']<=49)&(flights['long']>=128)&(flights['long']<=139))] #exclude unneeded regions
    flights = flights.fillna('N/A')
    flights = flights[flights['true_track']!='N/A']

    return flights

# Create a flight map
def create_flight_map(flights):
    
    map_center = [(lat_min+lat_max)/2, (lon_min+lon_max)/2] # Center the map about the middle of Japan
    flight_map = folium.Map(location=map_center, zoom_start=5, tiles="OpenStreetMap")
    
    for _, row in flights.iterrows(): 
        
        rotation_angle = row['true_track'] 
    
        # Create a custom plane icon
        plane_icon = folium.DivIcon(f'''<div style=
        
                        "transform: rotate({rotation_angle}deg); 
                        width: 16px; 
                        height: 16px;
                        background: url('https://github.com/william-suu/Air-Traffic-Map/raw/main/plane.png') no-repeat center;
                        background-size: contain;
                        opacity: 0.8;" > </div>''')

        folium.Marker(location=[row['lat'], row['long']], 
                      popup=folium.Popup(f"Callsign: {row['callsign']}, Origin Country: {row['origin_country']}", max_width=300),
                      icon=plane_icon).add_to(flight_map)
        
    #Show the locations of airports in Japan
    for _, row in japan_airports.iterrows():
        folium.CircleMarker(location=[row['Latitude'], row['Longitude']], radius=3, color='red', fill=True,
        fill_color='red', fill_opacity=0.6,tooltip=row['Airport Code']).add_to(flight_map)
    
    return flight_map


end_time=time.time() + 300 # <--- total run time in seconds

while time.time() < end_time:
    
    flights = get_flight_data()
    flight_map = create_flight_map(flights)
    
    clear_output(wait=True)
    display(flight_map)
    time.sleep(30) # update the map every x number of seconds


# In[ ]:




