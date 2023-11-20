import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from glob import glob

def main():
    st.title('My Streamlit App')

    data_files = glob('data/fogdata/*.csv')
    file_selected = st.sidebar.selectbox("Select a CSV file", data_files)

    df = pd.read_csv(file_selected)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    hourly_frequencies = df.groupby('hour').size()

    series = hourly_frequencies
    if series is not None:
        num_vars = len(series.index)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = series.values.flatten().tolist()
        values += values[:1] # repeat the first value to close the circle
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        plt.xticks(angles[:-1], series.index, color='grey', size=8)
        ax.set_theta_offset(np.pi/2) # Rotate the plot by 90 degrees
        ax.set_theta_direction(-1) # Make the plot go clockwise
        ax.set_rlabel_position(30)
        bars = ax.bar(angles[:-1], values[:-1], width=0.35, alpha=0.9, linewidth=2, edgecolor='none')

        st.pyplot(fig)

if __name__ == "__main__":
    main()
