
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

#setting front page configuration
st.set_page_config(layout="wide",
                   page_title="Kridnatcha Streamlit Traffic Jam")

st.markdown("""
<style>
.big-font {font-size:75px !important;color:black;}
.bgbg {background-image: url('http://www.tlcchiropractic.co.za/cropped-blank-white-image-jpg/');
background-repeat: no-repeat;background-attachment: fixed;background-size: 100% 100%;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bgbg"><p class="big-font">Travelling Data of Bangkok Metropolitan Region</p></div>', unsafe_allow_html=True)
st.title("Streamlit class Geospacial data")

#lay out front page 
row1_1, row1_2 = st.columns(2)

date_select = st.selectbox("Interest Date",("1 January 2019", "2 January 2019","3 January 2019","4 January 2019","5 January 2019"))
hour_selected = st.slider("Select hour of travelling", 0, 23)

st.warning(
    """
    Examining the number of travelling started and destinations reached for Bangkok and areas nearby.
    By sliding the slider on the left and selecting date you can view different slices of date and time and explore different transportation trends.
    This page used for study only (Geospatial Data Science and Analysis)
    """)

#loading data
DATE_TIME = "date/time"
dadate0101 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv")
dadate0102 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190102.csv")
dadate0103 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190103.csv")
dadate0104 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190104.csv")
dadate0105 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190105.csv")

#select data form date_select
if date_select == "1 January 2019" :
  DATA_URL = dadate0101
  st.title("Date Month Year : 1 January 2019")
elif date_select == "2 January 2019" :
  DATA_URL = dadate0102
  st.title("Date Month Year : 2 January 2019")
elif date_select == "3 January 2019" :
  DATA_URL = dadate0103
  st.title("Date Month Year : 3 January 2019")
elif date_select == "4 January 2019" :
  DATA_URL = dadate0104
  st.title("Date Month Year : 4 January 2019")
elif date_select == "5 January 2019" :
  DATA_URL = dadate0105
  st.title("Date Month Year : 5 January 2019")
#loading data
@st.cache(persist=True)
def load_data_origin(nrows):
    datastart = pd.read_csv(DATA_URL, nrows=nrows)
    datastart = datastart[['timestart','latstartl','lonstartl']].copy()
    datastart = datastart.rename(columns = {'timestart': 'Date/Time', 'latstartl': 'Lat', 'lonstartl': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    datastart.rename(lowercase, axis="columns", inplace=True)
    datastart[DATE_TIME] = pd.to_datetime(datastart[DATE_TIME],format= '%d/%m/%Y %H:%M')
    return datastart
    
@st.cache(persist=True)
def load_data_destination(nrows):
    datastop = pd.read_csv(DATA_URL, nrows=nrows)
    datastop = datastop[['timestop','latstop','lonstop']].copy()
    datastop = datastop.rename(columns = {'timestop': 'Date/Time', 'latstop': 'Lat', 'lonstop': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    datastop.rename(lowercase, axis="columns", inplace=True)
    datastop[DATE_TIME] = pd.to_datetime(datastop[DATE_TIME],format= '%d/%m/%Y %H:%M')
    return datastop

data1 = load_data_origin(100000)
data2 = load_data_destination(100000)

#functions page
def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

data1 = data1[(data1[DATE_TIME].dt.hour == hour_selected)]
data2 = data2[(data2[DATE_TIME].dt.hour == hour_selected)]

#center of  maps
zoom_level = 12
midpoint = [13.7382604, 100.5327218]

st.warning("**Departure Time %i:00 - %i:00**" % (hour_selected, (hour_selected + 1) % 24))
map(data1, midpoint[0], midpoint[1], zoom_level)

st.warning("**Arrival Time %i:00 - %i:00**" % (hour_selected, (hour_selected + 1) % 24))
map(data2, midpoint[0], midpoint[1], zoom_level)

#graph1
filtered1 = data1[(data1[DATE_TIME].dt.hour >= hour_selected) & (data1[DATE_TIME].dt.hour < (hour_selected + 1))]
hist1 = np.histogram(filtered1[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data1 = pd.DataFrame({"minute": range(60), "Number of all departure": hist1})

st.write("")
st.warning("**Interval of all departure time per minute in range %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data1)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("Number of all departure:Q"),
        tooltip=['minute', 'Number of all departure']
    ).configure_mark(
        opacity=0.8,
        color='green'
    ), use_container_width=True)

#graph2
filtered2 = data2[
    (data2[DATE_TIME].dt.hour >= hour_selected) & (data2[DATE_TIME].dt.hour < (hour_selected + 1)) ]
hist2 = np.histogram(filtered2[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data2 = pd.DataFrame({"minute": range(60), "Number of all arrival": hist2})

st.write("")
st.warning("**Interval of all arrival time per minute in range %i:00 and %i:00**" % (hour_selected, (hour_selected + 1) % 24))
st.altair_chart(alt.Chart(chart_data2)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("Number of all arrival:Q"),
        tooltip=['minute', 'Number of all arrival']
    ).configure_mark(
        opacity=0.8,
        color='red'
    ), use_container_width=True)
