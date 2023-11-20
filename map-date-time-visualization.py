import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import time, datetime

fog_camera_locations = pd.read_csv('data/siteinfo/fogvision_camera_locations.csv')

auwahi_predictions = pd.read_csv('data/fogdata/auwahi_predictions.csv')
haleakala = pd.read_csv('data/fogdata/haleakalaR_predictions.csv')
kaala600m = pd.read_csv('data/fogdata/kaala600m_predictions.csv')
kaala1200m = pd.read_csv('data/fogdata/kaala1200m_predictions.csv')

cummulative_station_data = pd.concat([auwahi_predictions, haleakala, kaala600m, kaala1200m])
cummulative_station_data['timestamp'] = pd.to_datetime(cummulative_station_data['timestamp'])
# auwahi_predictions['timestamp'] = pd.to_datetime(auwahi_predictions['timestamp'])
# haleakala['timestamp'] = pd.to_datetime(haleakala['timestamp'])
# kaala600m['timestamp'] = pd.to_datetime(kaala600m['timestamp'])
# kaala1200m['timestamp'] = pd.to_datetime(kaala1200m['timestamp'])

st.write(fog_camera_locations)

# TODO combine all the csvs into one data frame where
#  we use it to select the lowest and max datetime values

st.header("CSV CHECKING SECTION")
st.write(cummulative_station_data)

mapbox_access_token = "pk.eyJ1IjoiYnJpYW4tZC1kYW5nIiwiYSI6ImNsbmZsajNqaTA5MGQyc28yZG1uZ3U5aHUifQ.Zre5_G3J5Ee-HbFtizaWoA"

# OAHU
st.header("test text")
station_data_unique_timestamps = cummulative_station_data['timestamp'].unique()
date_time = st.select_slider(
    "When do you start?",
    options=station_data_unique_timestamps,
)

filtered_cummulative_station_data = cummulative_station_data[cummulative_station_data['timestamp'] == date_time]

fig_map = go.Figure()

# TODO use this for loop in later implementation 
# for x in fog_camera_locations['site']:
for sitename in ['kaala600m', 'kaala1200m']:

    site_information = fog_camera_locations[fog_camera_locations['site'] == sitename]
    test = (filtered_cummulative_station_data[filtered_cummulative_station_data['sitename'] == sitename]['category']>=1).bool()
    color='red'
    if (test):
        color = 'green'
    fig_map.add_trace(go.Scattermapbox(
        lat=np.array(site_information['x']),
        lon=np.array(site_information['y']),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color=color,
        ),
        text=site_information['site'],
    ))

fig_map.update_layout(
    hovermode='closest',
    mapbox=dict(
        style='mapbox://styles/mapbox/light-v11',
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=21.51565,
            lon=-158.15379
        ),
        pitch=0,
        zoom=12.5
    )
)

st.write(fig_map)

# date_time




