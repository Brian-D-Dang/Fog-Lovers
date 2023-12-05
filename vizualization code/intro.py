import os
# correcting the current working directory
basename = os.path.basename(os.getcwd())
if basename == 'pages':
    os.chdir(os.path.dirname(os.getcwd())) # this is important we have to change the working directory back one
elif 'hange' in basename or 'ICS-484' in basename:
    os.chdir(os.path.join(os.getcwd(), 'FogVision')) # 
print(os.getcwd())
import streamlit as st

st.set_page_config(layout="wide")
st.markdown("""
<style>
.big-font {
    font-size:24px !important;
}
</style>
""", unsafe_allow_html=True)

st.title('Fog: an Important Water Reasource')
col1, col2 = st.columns([2,2])
with col1:
    st.header('Cloud water interception (CWI)')
    # st.write('')
    st.markdown('<p class="big-font">The process by which water droplets within clouds, carried by winds, are captured and deposited onto vegetation and other encountered obstacles. This accumulated water then drips to the ground, supplementing rainfall and contributing to overall water availability. Thus, fog is a crucial water resource on mountainous islands such as the Hawaiian Islands, where it has been studied for over 70 years (DeLay and Giambelluca, 2011). However, there are practical challenges to measuring fog’s contribution to the water balance.</p>', unsafe_allow_html=True)
with col2:
    st.image(os.path.join('media', 'CWI-Han-Tseng-1-1024x765.png'), width=600)

st.header('Traditional Collection methods')
st.markdown('<p class="big-font">Traditionally fog has been measured using mechanical collectors, sometimes referred to as fog gauges, as well as canopy water balance measurements. See image of fog catchment device below.</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">There are some short comings to these traditional techniques. Such as contamination with wind-blow rain and their equitment footprint. Trail Camers offer a low-cost method to observe fog presence. Train cameras can be used to augment traditional equitment installations providing increased spatial coverage.</p>', unsafe_allow_html=True)
col3, col4 = st.columns([1,2])
with col3:
    # st.markdown('<p class="big-font"></p>', unsafe_allow_html=True)
    st.image(os.path.join('media', 'Kahikinui Fog Screens.jpg'), width=300)
with col4:
    st.image(os.path.join('media', 'trailcam.jpg'), use_column_width=False)
    

# col1, col2, _ = st.columns([1,2,2])
# col1.image(os.path.join('media', 'trailcam.jpg'), use_column_width=True)
# col2.image(os.path.join('media', 'fixed_performance_figure.jpg'), use_column_width=True)
# col3.image(os.path.join('media', 'fixed_performance_figure.jpg'), use_column_width=True)


# st.write('The data collected from these trail cameras is unstructured; meaning we need to look at the images and classify them by having fog present or not. However, this is a labor intensive task and creates and extreme human reasource bottleneck. To avoid this issue we used machine learning models to classify images by fog presence automatically. We tested both site-specific models trained only on examples for the given site and general models which were trained on data from other sites. Below you can see the performance of these models for diurnal and nocturnal imagery.')
# st.image(os.path.join('media', 'fixed_performance_figure.jpg'), use_column_width=True)

# st.write("Through our 'Fog Lovers' dashboard you will be able to view fog presence data collected from cameras on the islands of Maui and Oahu")
# st.image(os.path.join('media', 'IMG_0635.JPG'), width=500)

