import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


st.set_page_config(layout="wide")
col1, col2 = st.columns([2,1])

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

with col1:
    st.header("Fog detection throughout the year")
    st.subheader("Select an Island")
    island_subcol1, island_subcol2, island_subcol3 = st.columns([1,1,1])
    with island_subcol1:
        all_islands_button = st.button("All islands", type="primary")
    with island_subcol2:
        oahu_button = st.button("Oahu", type="primary")
    with island_subcol3:
        maui_button = st.button("Maui", type="primary")
        
    # island_selectbox = st.selectbox(
    #     'Select an island',
    #     ('All islands', 'Oahu', 'Maui'))

    # time selector
    station_data_unique_timestamps = cummulative_station_data['timestamp'].unique()
    # include a date time widget
    # include a time slider
    Year = st.select_slider(
        "Year",
        options=[2021,2022,2023],
    )
    Day = st.select_slider(
        "Date",
        options=np.arange(1,),
    )
    Month = st.select_slider(
        "Month",
        options=station_data_unique_timestamps,
    )
    date_time = st.select_slider(
        "Select a date: format(yyyy-mm-dd hr:min:00)",
        options=station_data_unique_timestamps,
    )
    # st.write(kaala600m)

    filtered_cummulative_station_data = cummulative_station_data[cummulative_station_data['timestamp'] == date_time]

    fog_detection_map = go.Figure()
    mapbox_access_token = "pk.eyJ1IjoiYnJpYW4tZC1kYW5nIiwiYSI6ImNsbmZsajNqaTA5MGQyc28yZG1uZ3U5aHUifQ.Zre5_G3J5Ee-HbFtizaWoA"

    # color types
    color_types = [
        ["green", 'Fog'],
        ["red", "No Fog"],
        ["grey", "Unknown"]
    ]
    for x in color_types:
        fog_detection_map.add_trace(go.Scattermapbox(
            mode='markers',
            lon=np.array(0),
            lat=np.array(0),
            marker={
                'size': 10,
                'color':x[0]
            },
            name=x[1],
            showlegend=True
        ))

    # TODO add code below
    # for x in fog_camera_locations['site']:
    for sitename in ['auwahi', 'haleakalaR', 'kaala600m', 'kaala1200m']:
        site_information = fog_camera_locations[fog_camera_locations['site'] == sitename]
        hasFog = np.array(filtered_cummulative_station_data[filtered_cummulative_station_data['sitename'] == sitename]['category'])[0] >= 1
        color='grey'
        if (hasFog):
            color = 'green'
        elif not hasFog:
            color='red'
        fog_detection_map.add_trace(go.Scattermapbox(
            mode='markers',
            lon=np.array(site_information['y']),
            lat=np.array(site_information['x']),
            marker={
                'size': 10,
                'color':color
            },
            name=sitename,
            showlegend=False
        ))
    # TODO add 3 traces that act as legends
    if oahu_button:
        fog_detection_map_lat = 21.51565
        fog_detection_map_lon = -158.15379
        zoom = 11.5
    elif maui_button:
        fog_detection_map_lat = 20.7171 
        fog_detection_map_lon = -156.345
        zoom = 9.5
    else:
        fog_detection_map_lat = 20.6471
        fog_detection_map_lon = -157.5
        zoom = 5.5

    fog_detection_map.update_layout(
        mapbox={
            'style':'basic',
            'accesstoken':mapbox_access_token,
            'center':go.layout.mapbox.Center(
                lat=fog_detection_map_lat,
                lon=fog_detection_map_lon
            ),
            'zoom':zoom,
        },
        showlegend=True,
        dragmode=False,
        legend_title_text='Legend'
        # modebar_remove=['zoom', 'pan']
        # config={'displayModeBar': False},
    )

    st.write(fog_detection_map)

