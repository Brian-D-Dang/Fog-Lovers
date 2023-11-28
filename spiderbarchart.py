import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from glob import glob

def main():
    st.title('My Streamlit App')

    data_files = glob('data/fogdata/*.csv')
    siteNames = []
    for data_file in data_files:
        firstSplit = data_file.split('\\')
        siteNames.append(firstSplit[-1].split('.csv')[0].split('_')[0])
    site_selected = st.sidebar.selectbox("Select a site", siteNames)

    file_selected = None
    for data_file in data_files:
        firstSplit = data_file.split('\\')
        if site_selected == firstSplit[-1].split('.csv')[0].split('_')[0]:file_selected = data_file

    if not file_selected is None:
        df = pd.read_csv(file_selected)
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
            ax.set_theta_offset(np.pi/2) # Rotate the plot by 90 degrees
            ax.set_theta_direction(-1) # Make the plot go clockwise
            ax.set_rlabel_position(30)
            bars = ax.bar(angles[:-1], values[:-1], width=0.35, alpha=0.9, linewidth=2, edgecolor='none')
            ax.grid(False) # This line removes the grid
            ax.set_yticklabels([])
            st.pyplot(fig)
    else:
        st.experimental_rerun()

if __name__ == "__main__":
    main()
