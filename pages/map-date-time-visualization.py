import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime

st.set_page_config(layout="wide")
col1, col2 = st.columns([3,2])

# Load in the CSVs
fog_camera_locations = pd.read_csv('data/siteinfo/fogvision_camera_locations.csv')
auwahi_predictions = pd.read_csv('data/fogdata/auwahi_predictions.csv')
# auwahi cleaned
auwahi_predictions['sitename'].mask(auwahi_predictions['sitename'] == 'auwahiOldLocation', 'auwahi', inplace=True)
haleakala = pd.read_csv('data/fogdata/haleakala_predictions.csv')
# haleakala cleaned
haleakala['sitename'].mask(haleakala['sitename'] == 'haleakala', 'haleakalaR', inplace=True)
honda = pd.read_csv('data/fogdata/honda_predictions.csv')
kaala1000m = pd.read_csv('data/fogdata/kaala1000m_predictions.csv')
# kaala1000 cleaned
kaala1000m['sitename'].mask(kaala1000m['sitename'] == 'kaala1000mCameraMoved', 'kaala1000m', inplace=True)
kaala1200m = pd.read_csv('data/fogdata/kaala1200m_predictions.csv')
# kaala1200m cleaned
kaala1200m['sitename'].mask(kaala1200m['sitename'] == 'kaala1200mCameraMoved', 'kaala1200m', inplace=True)

# Combine the CSVs into a centralized cummulative CSV
cummulative_station_data = pd.concat([auwahi_predictions, honda, haleakala, kaala1000m, kaala1200m])
cummulative_station_data['timestamp'] = pd.to_datetime(cummulative_station_data['timestamp'])
# island selector


with col1:
    st.header("Fog detection throughout the year")
    with st.form("form_settings"):
        form_section1, form_section2, form_section3 = st.columns([2, 1,2])
        with form_section1: 
            st.subheader("Select an island")
            islands_radio = st.radio(
                "",
                ["Oahu", "Maui", "Both"],
                label_visibility='collapsed')
        with form_section2:
            jan_1 = datetime.date(2021, 3, 22)
            dec_31 = datetime.date(2022, 8, 2)
            st.subheader("Select a date")
            date = st.date_input(
                "",
                (jan_1),
                jan_1,
                dec_31,
                format="YYYY-MM-DD",
                label_visibility='collapsed',
            )
        
        st.subheader("Select a time")
        time = st.slider(
            "",
            min_value=datetime.time(0, 0),
            max_value=datetime.time(23, 45),
            label_visibility='collapsed',
        )
        submitted = st.form_submit_button("Submit")
    date_time = datetime.datetime.combine(date, time)

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
                'size': 9,
                'color':x[0]
            },
            name=x[1],
            showlegend=True
        ))

    for sitename in ['auwahi', 'haleakalaROldLocation', 'haleakalaR', 'honda', 'kaala1000m', 'kaala1200m']:
        site_information = fog_camera_locations[fog_camera_locations['site'] == sitename]
        # DETECT IF SITENAME EXISTS OTHERWISE MAKE IT A NULL VALUE = GREY
        siteCheck = filtered_cummulative_station_data[filtered_cummulative_station_data['sitename'] == sitename]
        color = 'green'
        if len(siteCheck) == 0:
            color='grey'
        else:
            fogCategory = np.array(siteCheck['category'])[0]
            if fogCategory == 1:
                color = 'green'
            elif fogCategory == 0:
                color='red'
            elif fogCategory == -999:
                color='grey'
    
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

    if islands_radio == 'Oahu':
        fog_detection_map_lat = 21.51565
        fog_detection_map_lon = -158.15379
        zoom = 11.5
    elif islands_radio =='Maui':
        fog_detection_map_lat = 20.7171 
        fog_detection_map_lon = -156.345
        zoom = 9.5
    else:
        fog_detection_map_lat = 21.09
        fog_detection_map_lon = -157.3
        zoom = 7

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
    )

    st.write(fog_detection_map)

