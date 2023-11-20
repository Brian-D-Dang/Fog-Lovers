import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from glob import glob

def main():
    st.title('My Streamlit App')

    # # Assuming 'hourly_frequencies' is a DataFrame
    # series = st.sidebar.file_uploader("Upload your CSV file", type=['csv'])
    data_files = glob('data/fogdata/*.csv')
    df_list = [pd.read_csv(file) for file in data_files]
    df = df_list[0]

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    hourly_frequencies = df.groupby('hour').size()
    data_files = glob('data/fogdata/*.csv')
    df_list = [pd.read_csv(file) for file in data_files]

    series = hourly_frequencies
    if series is not None:
        # series.set_index('Index_Column_Name', inplace=True) # Replace 'Index_Column_Name' with the name of your index column

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
