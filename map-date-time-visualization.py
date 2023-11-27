import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
# from datetime import time, datetime

# Load in the CSVs
fog_camera_locations = pd.read_csv('data/siteinfo/fogvision_camera_locations.csv')

auwahi_predictions = pd.read_csv('data/fogdata/auwahi_predictions.csv')
haleakala = pd.read_csv('data/fogdata/haleakalaR_predictions.csv')
kaala600m = pd.read_csv('data/fogdata/kaala600m_predictions.csv')
kaala1200m = pd.read_csv('data/fogdata/kaala1200m_predictions.csv')

# Combine the CSVs into a centralized cummulative CSV
cummulative_station_data = pd.concat([auwahi_predictions, haleakala, kaala600m, kaala1200m])
cummulative_station_data['timestamp'] = pd.to_datetime(cummulative_station_data['timestamp'])

# island selector
st.header("Fog detection throughout the year")
island_selectbox = st.selectbox(
    'Select an island',
    ('All islands', 'Oahu', 'Maui'))

# island_selectbox = st.selectbox(
#     'Select an island',
#     ('All islands', 'Oahu', 'Maui'))

# time selector
station_data_unique_timestamps = cummulative_station_data['timestamp'].unique()
date_time = st.select_slider(
    "Select a date: format(yyyy-mm-dd hr:min:00)",
    options=station_data_unique_timestamps,
)
# st.write(kaala600m)

filtered_cummulative_station_data = cummulative_station_data[cummulative_station_data['timestamp'] == date_time]

fog_detection_map = go.Figure()
# TODO use this for loop in later implementation 
# for x in fog_camera_locations['site']:
mapbox_access_token = "pk.eyJ1IjoiYnJpYW4tZC1kYW5nIiwiYSI6ImNsbmZsajNqaTA5MGQyc28yZG1uZ3U5aHUifQ.Zre5_G3J5Ee-HbFtizaWoA"
for sitename in ['auwahi', 'haleakalaR', 'kaala600m', 'kaala1200m']:
    site_information = fog_camera_locations[fog_camera_locations['site'] == sitename]
    test = np.array(filtered_cummulative_station_data[filtered_cummulative_station_data['sitename'] == sitename]['category'])[0] >= 1
    color='red'
    if (test):
        color = 'green'
    fog_detection_map.add_trace(go.Scattermapbox(
        # mode = "markers+text+lines",
        # lon = [-75, -80, -50], lat = [45, 20, -20],
        # marker = {'size': 20, 'symbol': ["bus", "harbor", "airport"]},
        # text = ["Bus", "Harbor", "airport"],textposition = "bottom right"))
        mode='markers+text',
        lon=np.array(site_information['y']),
        lat=np.array(site_information['x']),
        marker={
            'size': 20, 'symbol': ['bus'],'color':'black'
        },
        text=["test"],
        # textsize=15,
        # color='black',
        textposition = "bottom right"))

if island_selectbox == 'Oahu':
    fog_detection_map_lat = 21.51565
    fog_detection_map_lon = -158.15379
    zoom = 11.5
elif island_selectbox == 'Maui':
    fog_detection_map_lat = 20.7171 
    fog_detection_map_lon = -156.345
    zoom = 9.5
else:
    fog_detection_map_lat = 20.6471
    fog_detection_map_lon = -157.5
    zoom = 5.5

fog_detection_map.update_layout(
    mapbox={
        'style':'outdoors',
        'accesstoken':mapbox_access_token,
        'center':go.layout.mapbox.Center(
            lat=fog_detection_map_lat,
            lon=fog_detection_map_lon
        ),
        'zoom':zoom,
    },
    showlegend=False,
)

st.write(fog_detection_map)

