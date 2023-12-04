import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dummyData = pd.read_csv("data/dummby/auwahi_predictions.csv")

realData = pd.read_csv("data/fogdata/auwahi_predictions.csv")

# st.write(dummyData)

# st.write(realData)

fogLocations = pd.read_csv('data/siteinfo/fogvision_camera_locations.csv')

auwahi_predictions = pd.read_csv('data/fogdata/auwahi_predictions.csv')
haleakala = pd.read_csv('data/fogdata/haleakala_predictions.csv')
honda = pd.read_csv('data/fogdata/honda_predictions.csv')
kaala1000m = pd.read_csv('data/fogdata/kaala1000m_predictions.csv')
kaala1200m = pd.read_csv('data/fogdata/kaala1200m_predictions.csv')

st.write(fogLocations)
st.write(auwahi_predictions['sitename'].unique())
st.write(haleakala)
st.write(haleakala['sitename'].unique())
st.write(honda['sitename'].unique())
st.write(kaala1000m['sitename'].unique())
st.write(kaala1200m['sitename'].unique())