import os
# correcting the current working directory
basename = os.path.basename(os.getcwd())
if basename == 'pages':
    os.chdir(os.path.dirname(os.getcwd())) # this is important we have to change the working directory back one
elif 'hange' in basename or 'ICS-484' in basename:
    os.chdir(os.path.join(os.getcwd(), 'FogVision')) # 
print(os.getcwd())


import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from glob import glob

def main():
    st.title('yessaih')
    st.write(os.getcwd())
    data_files = glob('data/fogdata/*.csv')
    print(data_files)
    st.write(data_files)
    siteNames = []
    for data_file in data_files:
        firstSplit = data_file.split('\\')
        siteNames.append(firstSplit[-1].split('.csv')[0].split('_')[0])
    site_selected = st.sidebar.selectbox("Select a site", siteNames)

    file_selected = None
    for data_file in data_files:
        firstSplit = data_file.split('\\')
        if site_selected == firstSplit[-1].split('.csv')[0].split('_')[0]: file_selected = data_file

    if not file_selected is None:
        df = pd.read_csv(file_selected)
        df = df[df['category'] != -999]
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df_category1 = df[df['category'] == 1]
        hourly_frequencies_category1 = df_category1.groupby('hour').size()
        hourly_frequencies_total = df.groupby('hour').size()
        series = hourly_frequencies_category1 / hourly_frequencies_total
        series.fillna(0, inplace=True) # should be temporary
        if series is not None:
            num_vars = len(series.index)
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            values = series.values.flatten().tolist()
            values += values[:1] # repeat the first value to close the circle
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.set_title(f'Hourly fog frequency for {site_selected}')
            plt.xticks(angles[:-1], series.index, color='grey', size=8)
            ax.set_theta_offset(np.pi/2) # rotate the plot by 90 degrees so 0 oclock is at the top
            ax.set_theta_direction(-1) # make the plot go clockwise
            ax.set_rlabel_position(30)
            bars = ax.bar(angles[:-1], values[:-1], width=0.15, alpha=0.9, linewidth=2, edgecolor='none') # reduce the width of the bars
            ax.grid(False) # remove grid lines
            ax.set_yticklabels([])

            # Add radial axes and labels
            r_ticks = np.linspace(0, max(values), num=5)  # You can change the number of ticks here
            ax.set_yticks(r_ticks)
            ax.set_yticklabels([f'{tick:.2f}' for tick in r_ticks], color='grey', size=8)  # Format the labels as you wish
            ax.yaxis.grid(True)  # Add grid lines for the y-axis

            st.pyplot(fig)

        df['date'] = df['timestamp'].dt.date
        daily_frequencies_total = df.groupby('date').size()
        daily_frequencies_category1 = df[df['category'] == 1].groupby('date').size()
        daily_percentages_category1 = (daily_frequencies_category1 / daily_frequencies_total) * 100

        # Create a date range that includes all dates in your data
        date_range = pd.date_range(start=df['date'].min(), end=df['date'].max())

        # Convert your data to a Series with the date range as the index
        daily_percentages_category1 = pd.Series(daily_percentages_category1, index=date_range)

        fig, ax = plt.subplots()
        ax.plot(daily_percentages_category1.index, daily_percentages_category1.values)

        # Set the major ticks to the first day of each month.
        ax.xaxis.set_major_locator(mdates.MonthLocator())

        # Set the major tick labels to the month and year.
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        fig.autofmt_xdate()
        st.pyplot(fig)

    else:
        print('fuckina')
        # st.experimental_rerun()

if __name__ == "__main__":
    main()
