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

# def main():
#     st.title('yessaih')
#     data_files = glob('data/fogdata/*.csv')
#     st.write(data_files)
#     siteNames = []
#     for data_file in data_files:
#         firstSplit = data_file.split('\\')
#         siteNames.append(firstSplit[-1].split('.csv')[0].split('_')[0])
#     site_selected = st.sidebar.selectbox("Select a site", siteNames)

#     file_selected = None
#     for data_file in data_files:
#         firstSplit = data_file.split('\\')
#         if site_selected == firstSplit[-1].split('.csv')[0].split('_')[0]: file_selected = data_file

#     if not file_selected is None:
def main():
    data_files = glob('data/fogdata/*.csv')
    siteNames = []
    for data_file in data_files:
        firstSplit = data_file.split('\\')
        siteNames.append(firstSplit[-1].split('.csv')[0].split('_')[0])
    sites_selected = st.sidebar.multiselect("Select sites", siteNames)

   # Define the figure and axes outside the loop
    # fig, axs = plt.subplots(nrows = 2, ncols=1, figsize=(6, 6))
    fig = plt.figure(figsize=(6, 6))
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
                axs[0].set_title(f'Hourly fog frequency for {site_selected}')
                plt.xticks(angles[:-1], series.index, color='grey', size=8)
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
                r_ticks = np.linspace(0, max(values), num=5)  # You can change the number of ticks here
                axs[0].set_yticks(r_ticks)
                axs[0].set_yticklabels([f'{tick:.2f}' for tick in r_ticks], color='black', size=8)  # Format the labels as you wish
                axs[0].yaxis.grid(True)  # Add grid lines for the y-axis
                axs[0].legend(loc='upper right')





            # line chart
            # df['date'] = df['timestamp'].dt.date
            # print(df)
            # daily_frequencies_total = df.groupby('date').size()
            # daily_frequencies_category1 = df[df['category'] == 1].groupby('date').size()
            # daily_percentages_category1 = (daily_frequencies_category1 / daily_frequencies_total) * 100
            # date_range = pd.date_range(start=df['date'].min(), end=df['date'].max())
            # daily_percentages_category1 = pd.Series(daily_percentages_category1, index=date_range)
            # print(daily_percentages_category1)
            # axs[1].plot(daily_percentages_category1.index, daily_percentages_category1.values)
            # axs[1].xaxis.set_major_locator(mdates.MonthLocator())
            # axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            # df['date'] = df['timestamp'].dt.to_period('M')
            # print(df)
            # monthly_frequencies_total = df.groupby('date').size()
            # monthly_frequencies_category1 = df[df['category'] == 1].groupby('date').size()
            # print(monthly_frequencies_category1)
            # monthly_percentages_category1 = (monthly_frequencies_category1 / monthly_frequencies_total) * 100
            # date_range = pd.date_range(start=df['date'].min().to_timestamp(), end=df['date'].max().to_timestamp(), freq='M')
            # monthly_percentages_category1 = pd.Series(monthly_percentages_category1, index=date_range)
            # print(monthly_percentages_category1)
            # axs[1].plot(monthly_percentages_category1.index, monthly_percentages_category1.values)
            # axs[1].xaxis.set_major_locator(mdates.MonthLocator())
            # axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            df['date'] = df['timestamp'].dt.to_period('W')
            weekly_frequencies_total = df.groupby('date').size()
            weekly_frequencies_category1 = df[df['category'] == 1].groupby('date').size()
            weekly_percentages_category1 = (weekly_frequencies_category1 / weekly_frequencies_total) * 100
            weekly_percentages_category1 = weekly_percentages_category1.reindex(df['date'].unique(), fill_value=0)
            axs[1].plot(weekly_percentages_category1.index.to_timestamp(), weekly_percentages_category1.values)
            axs[1].xaxis.set_major_locator(mdates.MonthLocator())
            axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))




    # Show the plot after the loop
    st.pyplot(fig)



            
        
        # else:
        #     st.experimental_rerun()


if __name__ == "__main__":
    main()
