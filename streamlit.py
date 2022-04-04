import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



st.set_page_config(layout="centered", page_icon="💬", page_title="Solar energy and weather")



st.title('Solar Power Generation Analysis Using Historical Weather Data')
st.markdown('''
* Objective : Comparison of monthly wise solar power generation with respect to weather indices from nearest observatory(AWS)
* Location of solar power plant : Nargund(North Interior Karnataka)
* Location of the observatory used for historical weather data analysis : Gadag IMD Observatory(North Interior Karnataka)
* ERA5-Land monthly averaged data at the location of solar power plant(30 km horizontal resolution reanalysis data)
* Period : 2018 April to 2021 June(3 years 3 months
* Comparison mode : Monthly-wise
* Two solar power plants are used for analysis: Anantpur Solar Park Private Limited (ASPPL), Thungapatra Solar Power Private Limited (TSPPL)
''')

st.write('---')


st.subheader('Monthly averaged weather variables to compare with Monthly Solar Power generation(in MWh)')

st.markdown('''
* Surface Solar Radiation
* Maximum Temperature
* Mean Temperature
* Total cloud cover
* Rain days
* Relative Humidity
* Dew Point Temperature
* Precipitation
* Percentage soil water
* Evaporation
* Skin Temperature
* Vegetation
* Soil Temperature
''')

st.write('---')



st.subheader('Solar power plant capacity frequency')




solar_plants_file = 'cordiantes_power_chrono.csv'



@st.cache
def load_data():
    solar = pd.read_csv(solar_plants_file)
    lowercase = lambda x: str(x).lower()
    solar.rename(lowercase, axis='columns', inplace=True)
    #data1[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return solar


solar_plants = load_data()


fig, ax = plt.subplots()
ax.hist(solar_plants['power'], bins=35)

st.pyplot(fig)



st.subheader('Locations of solar power plant')


plant_capacity_slider = st.slider('Solar Poer Plant Capacity', int(solar_plants['power'].min()), int(solar_plants['power'].max()), int(solar_plants['power'].max()))
filtered_data = solar_plants[solar_plants['power'] <= plant_capacity_slider]
st.subheader(f'Location of solar power plant whose capacity is less than or equal to {plant_capacity_slider}')
st.map(filtered_data)



st.write('---') #cordiantes


# data = {'location':['ASPPL', 'TSPPL'],
        # 'lat':[15.79030756911847, 16.45777847538088],
        # 'lon':[75.49064818162839, 74.78141029948743],}

# df = pd.DataFrame(data)

# st.map(df)


st.write('---')

aws_stations = 'WMO_SOLAR_Cordinates.csv'

@st.cache
def weather_stations():
    aws = pd.read_csv(aws_stations)
    lowercase = lambda x: str(x).lower()
    aws.rename(lowercase, axis='columns', inplace=True)
    #data1[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return aws


aws_st_data = weather_stations()



st.subheader('Location of weather stations which will be used for analysis')
st.map(aws_st_data)







st.write('---')


option1 = st.selectbox(
     'Weather variable to be correlated with power generation',
     ('ASPPL', 'TSPPL'))
     
     
st.write('You selected:', option1)
     
     
st.write('---')




asppl_data = option1 + '_Analysis.csv'
tsppl_data = 'Full_Analysis.csv'

asppl = pd.read_csv(asppl_data)
#tsppl = pd.read_csv(tsppl_data)



# @st.cache
# def load_data1():
    # asppl = pd.read_csv(asppl_data)
    # lowercase1 = lambda x: str(x).lower()
    # asppl.rename(lowercase, axis='columns', inplace=True)
    # #data1[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    # return asppl


# @st.cache
# def load_data2():
    # tsppl = pd.read_csv(tsppl_data)
    # lowercase2 = lambda x: str(x).lower()
    # tsppl.rename(lowercase2, axis='columns', inplace=True)
    # #data1[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    # return tsppl




# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# # Load 10,000 rows of data into the dataframe.
# data = load_data_()
# # Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')





#st.subheader('Raw data')
#st.write(data)
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(asppl)


st.write('---')



option = st.selectbox(
     'Weather variable to be correlated with power generation',
     (asppl.columns[2:]))

st.write('You selected:', option)



# def scatter_plot():
    # #Create numpy array for the visualisation
    # x = np.array([5,7,8,7,2,17,2,9,4,11,12,9,6])
    # y = np.array([99,86,87,88,111,86,103,87,94,78,77,85,86])    
    
    # fig = plt.figure(figsize=(10, 4))
    # plt.scatter(inp['Generation'], option)
    
    # st.balloons()
    # st.pyplot(fig)


# fig = plt.figure(figsize=(10, 4))
# plt.scatter(inp['Generation'], inp['Generation'])
    
# #st.balloons()
# st.pyplot(fig)

def scatter_plot():
    #Create numpy array for the visualisation

    fig = plt.figure()
    plt.scatter(asppl['Generation'], asppl[option])
    z = np.polyfit(asppl['Generation'], asppl[option], 1)
    p = np.poly1d(z)
    plt.plot(asppl['Generation'],p(asppl['Generation']),"r--")
    plt.xlabel('Solar power generated (MWH)')
    plt.ylabel('Weather variable')
    
    st.pyplot(fig)
    
    
    
scatter_plot()



st.write('---')


st.subheader('Analysis Conclusions')




st.markdown('Mean monthly max Temperature, Surface Solar Radiation and daytime Temperature have good +ve correlation to monthly power generation.')
st.markdown('Total cloud cover, Relative humidity, Dew point Temperature, Precipitation, Percentage Soil Water, Evaporation and no.of rainy days have good -ve correlation to monthly power generation.')
st.markdown('Monthly power generation(2018-21) is highest during March due to high max temperature and low cloud cover followed by less rainy days.')
st.markdown('Monthly power generation are low over monsoon peak months (July-August) due to high cloud cover and more rainy days.')
st.markdown('Several months shows less power generation(June, July, August of 2020) due to very high RH and increase in rainy days & cloud cover followed by less temperature values.')
st.markdown('Total power generation in 2018 is comparatively higher than other two years ,due to the weak monsoon condition prevailed over 2018 september-november period,followed by increase in generation.')
st.markdown('Certain months shows significant increase in power generation(2018 August - November) due to less RH,Rainy days,cloud cover followed by increase in Temperature.')
st.markdown('For regression analysis of weather variables daily or hourly data is more useful.')
st.markdown('More number of data points are needed to improve the results of the regression analysis.')


st.write('---')
