#!/usr/bin/env python
# coding: utf-8

# In[3]:


import folium

#Define area over Japan
lon_min, lat_min=128, 30
lon_max, lat_max=149, 46

# Define Area over korea
# lon_min, lat_min=125, 34
# lon_max, lat_max=130, 41

# Define Area over ...
# lon_min, lat_min=128, 42
# lon_max, lat_max=139, 49

# Center the map to the middle of the area
map_center = [(lat_min+lat_max)/2, (lon_min+lon_max)/2]
map = folium.Map(location=map_center, zoom_start=4)

# Visualize the aera
boundary = [
    [lat_min, lon_min],  # Bottom-left
    [lat_min, lon_max],  # Bottom-right
    [lat_max, lon_max],  # Top-right 
    [lat_max, lon_min],  # Top-left
    [lat_min, lon_min]   # Closing the box back at the bottom-left corner
]
#print(boundary_box)
folium.PolyLine(boundary,color='red',weight=2,opacity=0.8).add_to(map)

# Add markers at each of the 4 corners
for coord in boundary:
    folium.Marker(location=coord,icon=folium.Icon(color='blue'), popup=f"Latitude: {coord[0]}, Longitude: {coord[1]}").add_to(map)
map


# In[ ]:





# In[ ]:





# In[ ]:




