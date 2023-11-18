import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import time, datetime

fog_camera_locations = pd.read_csv('data/siteinfo/fogvision_camera_locations.csv')

st.write(fog_camera_locations)

mapbox_access_token = "pk.eyJ1IjoiYnJpYW4tZC1kYW5nIiwiYSI6ImNsbmZsajNqaTA5MGQyc28yZG1uZ3U5aHUifQ.Zre5_G3J5Ee-HbFtizaWoA"

fig_map = go.Figure()

fig_map.add_trace(go.Scattermapbox(
        name='Current',
        lat=fog_camera_locations['x'],
        lon=fog_camera_locations['y'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=6,
            color='green'
        ),
        text=fog_camera_locations['site'],
    ))

fig_map.update_layout(
    title='Rainfall Measurement Stations',
    hovermode='closest',
    mapbox=dict(
        style='mapbox://styles/mapbox/light-v11',
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=20.83961322,
            lon=-156.9291446
        ),
        pitch=0,
        zoom=5.5
    )
)

st.write(fig_map.show())


# create a oahu map




