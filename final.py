# import os
# # correcting the current working directory
# basename = os.path.basename(os.getcwd())
# if basename == 'pages':
#     os.chdir(os.path.dirname(os.getcwd())) # this is important we have to change the working directory back one
# elif 'hange' in basename or 'ICS-484' in basename:
#     os.chdir(os.path.join(os.getcwd(), 'FogVision')) # 
# print(os.getcwd())

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from glob import glob
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime

st.set_page_config(layout="wide")
st.title("Fog Visualizations In Hawaii")
col1, col2 = st.columns([3,2])

# Load in the CSVs
fog_camera_locations = pd.read_csv('data/siteinfo/fogvision_camera_locations.csv')
auwahi_predictions = pd.read_csv('data/fogdata/auwahi_predictions.csv')
# auwahi cleaned
auwahi_predictions['sitename'].mask(auwahi_predictions['sitename'] == 'auwahiOldLocation', 'auwahi', inplace=True)
haleakala = pd.read_csv('data/fogdata/haleakala_predictions.csv')
# haleakala cleaned
haleakala['sitename'].mask(haleakala['sitename'] == 'haleakalaR', 'haleakalaa', inplace=True)
haleakala['sitename'].mask(haleakala['sitename'] == 'haleakalaROldLocation', 'haleakalaa', inplace=True)
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


sitenames = ['auwahi', 'haleakala', 'honda', 'kaala1000m', 'kaala1200m']
sites_selected = st.sidebar.multiselect("Select sites", sitenames)

with col1:
    # st.header("Fog detection throughout the year")
    with st.form("form_settings"):
        form_section1, form_section2, form_section3 = st.columns([2, 2,2])
        with form_section1: 
            st.subheader("Select an island")
            islands_radio = st.radio(
                "",
                ["Oahu", "Maui", "Both"],
                index=2,
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
        # with form_section3:
        #     st.subheader("Select a site")
        #     # sites_selected = st.multiselect("", sitenames, label_visibility='collapsed')
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

    for sitename in sites_selected:
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
        zoom = 7.6

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
        width=850,
        height=450,
        margin=dict(l=0, r=20, t=10, b=20),
        legend_title_text='Legend'
    )
    st.subheader("Fog detection")
    st.write(fog_detection_map)

with col2:
    def main():
        data_files = glob('data/fogdata/*.csv')
        siteNames = []
        for data_file in data_files:
            firstSplit = data_file.split('\\')
            siteNames.append(firstSplit[-1].split('.csv')[0].split('_')[0])
        # sites_selected = st.sidebar.multiselect("Select sites", siteNames)

    # Define the figure and axes outside the loop
        # fig, axs = plt.subplots(nrows = 2, ncols=1, figsize=(6, 6))
        fig = plt.figure(figsize=(6, 10))
        axs = []
        axs.append(fig.add_subplot(2, 1, 1, projection='polar'))
        axs.append(fig.add_subplot(2, 1, 2))

    # Your code for the rectangular plot here

        categories = [f"{i:02d} AM" for i in range(1, 13)] + [f"{i:02d} PM" for i in range(1, 13)]
        temp = categories[11]
        categories[11] = categories[-1]
        categories[-1] = temp
        categories = categories = categories[-1:] + categories[:-1]

        for site_selected in sites_selected:
            file_selected = None
            for data_file in data_files:
                firstSplit = data_file.split('\\')
                if site_selected == firstSplit[-1].split('.csv')[0].split('_')[0]: file_selected = data_file

            if not file_selected is None:
                df = pd.read_csv(file_selected)
                df = df[df['category'] != -999]
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['hour'] = df['timestamp'].dt.hour
                df['12_hour_format'] = df['timestamp'].dt.strftime('%I %p')
                df['12_hour_format'] = pd.Categorical(df['12_hour_format'], categories=categories, ordered=True)
                df_category1 = df[df['category'] == 1]
                ### barchart
                hourly_frequencies_category1 = df_category1.groupby('12_hour_format', observed=False).size()
                hourly_frequencies_total = df.groupby('12_hour_format', observed=False).size()
                series = hourly_frequencies_category1 / hourly_frequencies_total
                series.fillna(0, inplace=True) # should be temporary
                if series is not None:
                    num_vars = len(series.index)
                    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
                    values = series.values.flatten().tolist()
                    values += values[:1] # repeat the first value to close the circle
                    angles += angles[:1]

                    # Set the title for each subplot
                    axs[0].set_title(f'Hourly fog frequency for {sites_selected}')
                    axs[0].set_xticks(angles[:-1], series.index, color='grey', size=8)
                    axs[0].set_theta_offset(np.pi/2) # rotate the plot by 90 degrees so 0 oclock is at the top
                    axs[0].set_theta_direction(-1) # make the plot go clockwise
                    axs[0].set_rlabel_position(30)
                    bars = axs[0].bar(angles[:-1], values[:-1], width=0.15, alpha=0.7, linewidth=2, edgecolor='none') # reduce the width of the bars
                    for bar in bars:  # loop through each bar in the bar plot
                        bar.set_label(site_selected)  # set the label for each bar
                        break
                    axs[0].grid(False) # remove grid lines
                    axs[0].set_yticklabels([])

                    # Add radial axes and labels
                    # y_ticks = np.arange(0, 1.01, 0.20)  # Creates an array from 0 to 1 with a step of 0.20
                    # y_ticks_angles = [x * 2 * np.pi for x in y_ticks]  # Converts the x ticks to angles
                    # axs[0].set_yticks(y_ticks_angles)
                    # axs[0].set_yticklabels([f'{tick:.2f}' for tick in y_ticks], color='grey', size=8)
                    r_ticks = np.linspace(0, 0.9, num=4)#max(values), num=5)  # You can change the number of ticks here
                    axs[0].set_yticks(r_ticks)
                    axs[0].set_yticklabels([f'{tick:.2f}' for tick in r_ticks], color='black', size=8)  # Format the labels as you wish
                    axs[0].yaxis.grid(True)  # Add grid lines for the y-axis
                    axs[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                    # axs[0].legend(loc='lower right')


                # line chart
                df['date'] = df['timestamp'].dt.to_period('W')
                weekly_frequencies_total = df.groupby('date').size()
                weekly_frequencies_category1 = df[df['category'] == 1].groupby('date').size()
                weekly_percentages_category1 = (weekly_frequencies_category1 / weekly_frequencies_total) * 100
                weekly_percentages_category1 = weekly_percentages_category1.reindex(df['date'].unique(), fill_value=0)
                axs[1].set_title(f'Weekly fog frequency for {sites_selected}')
                axs[1].plot(weekly_percentages_category1.index.to_timestamp(), weekly_percentages_category1.values, 'o--')
                # axs[1].bar(weekly_percentages_category1.index.to_timestamp(), weekly_percentages_category1.values)
                axs[1].xaxis.set_major_locator(mdates.MonthLocator())
                axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                plt.xticks(rotation=45)
                axs[1].set_ylabel('Fog Frequency Percentage')




        # Show the plot after the loop
        st.pyplot(fig)



                
            
            # else:
            #     st.experimental_rerun()


    if __name__ == "__main__":
        main()

st.markdown("""
<style>
.big-font {
    font-size:24px !important;
}
</style>
""", unsafe_allow_html=True)

st.title('Fog: an Important Water Reasource')
col3, col4 = st.columns([2,2])
with col3:
    st.header('Cloud water interception (CWI)')
    # st.write('')
    st.markdown('<p class="big-font">The process by which water droplets within clouds, carried by winds, are captured and deposited onto vegetation and other encountered obstacles. This accumulated water then drips to the ground, supplementing rainfall and contributing to overall water availability. Thus, fog is a crucial water resource on mountainous islands such as the Hawaiian Islands, where it has been studied for over 70 years (DeLay and Giambelluca, 2011). However, there are practical challenges to measuring fog’s contribution to the water balance.</p>', unsafe_allow_html=True)
with col4:
    st.image(os.path.join('media', 'CWI-Han-Tseng-1-1024x765.png'), width=600)

st.header('Traditional Collection methods')
st.markdown('<p class="big-font">Traditionally fog has been measured using mechanical collectors, sometimes referred to as fog gauges, as well as canopy water balance measurements. See image of fog catchment device below.</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">There are some short comings to these traditional techniques. Such as contamination with wind-blow rain and their equitment footprint. Trail Camers offer a low-cost method to observe fog presence. Train cameras can be used to augment traditional equitment installations providing increased spatial coverage.</p>', unsafe_allow_html=True)
col5, col6 = st.columns([1,2])
with col5:
    # st.markdown('<p class="big-font"></p>', unsafe_allow_html=True)
    st.image(os.path.join('media', 'Kahikinui Fog Screens.jpg'), width=490)
with col6:
    st.image(os.path.join('media', 'trailcam.jpg'), use_column_width=False)