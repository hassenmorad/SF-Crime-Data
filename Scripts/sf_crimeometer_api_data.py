# Pulling San Francisco Crime Data From Crimeometer.com API
import pandas as pd
import requests
from geopandas import GeoDataFrame
from shapely.geometry import Point
import fiona

lat = '37.7749'
lon = '-122.4194'
distance = '20mi'
datetime_ini = '2018-11-05T00:00:00.000Z'
datetime_end = '2018-11-11T00:00:00.000Z'
page = 1
url = f'https://api.crimeometer.com/v1/incidents/raw-data?lat={lat}&lon={lon}&distance={distance}&datetime_ini={datetime_ini}&datetime_end={datetime_end}&page={page}'
headers = {'Content-Type': 'application/json',
           'x-api-key': 'k3RAzKN1Ag14xTPlculT39RZb38LGgsG8n27ZycG'}

dataframe = pd.DataFrame()
total_pages = requests.get(url=url, headers=headers).json()['total_pages']

for i in range(1,total_pages+1):
    url = f'https://api.crimeometer.com/v1/incidents/raw-data?lat={lat}&lon={lon}&distance={distance}&datetime_ini={datetime_ini}&datetime_end={datetime_end}&page={i}'
    response = requests.get(url=url, headers=headers)
    data = response.json()["incidents"]
    for dict_obj in data:
        df = pd.DataFrame.from_dict(dict_obj, orient='index').transpose()
        dataframe = pd.concat([dataframe, df])

# Data cleaning below (added after initial analysis):
dataframe = dataframe[dataframe.city_key == 'SFO']
dataframe['incident_date'] = pd.to_datetime(dataframe['incident_date']).dt.date.astype(str)  # String format due to issues converting to shapefile when in datetime format
cols = ['city_key', 'incident_code', 'incident_date', 'incident_offense', 'incident_latitude', 'incident_longitude']
dataframe = dataframe[cols]
dataframe = dataframe.rename({'incident_date':'date', 'incident_offense':'offense', 'incident_latitude':'latitude', 'incident_longitude':'longitude'}, axis=1)

dataframe['latitude'] = dataframe['latitude'].astype(float)
dataframe['longitude'] = dataframe['longitude'].astype(float)

# Renaming some crime descriptions (simpler for reader)
crime_desc = {'All Other Offenses':'Other', 
              'Larceny/Theft Offenses':'Larceny/Theft', 
              'Assault Offenses':'Assault', 
              'Burglary/Breaking & Entering':'Burglary/Breaking & Entering',
              'Destruction/Damage/Vandalism of Property':'Destruction of Property/Vandalism', 
              'Drug/Narcotic Offenses':'Drugs',
              'Motor Vehicle Theft':'Motor Vehicle Theft',
              'Fraud Offenses':'Fraud', 
              'Sex Offenses':'Sex Offenses',
              'Suspicious Activity':'Suspicious Activity',
              'Trespass of Real Property':'Trespassing', 
              'Family Offenses':'Family Offenses',
              'Weapon Law Violations':'Weapons Violations',
              'Arson':'Arson',
              'Stolen Property Offenses':'Stolen Property', 
              'Counterfeiting/Forgery':'Counterfeiting/Forgery',
              'Drunkenness':'Drunkenness',
              'Embezzlement':'Embezzlement',
              'Disorderly Conduct':'Disorderly Conduct',
              'Prostitution Offenses':'Prostitution', 
              'Kidnapping/Abduction':'Kidnapping/Abduction',
              'Curfew/Loitering/Vagrancy Violations':'Loitering',
              'Child Abuse':'Child Abuse', 
              'Liquor Law Violations':'Liquor Law Violations', 
              'Human Trafficking':'Human Trafficking',
              'Bad Checks':'Bad Checks'}
dataframe['offense'] = dataframe['offense'].map(crime_desc)

# Converting dataframe to shapefile (source: https://gist.github.com/nygeog/2731427a74ed66ca0e420eaa7bcd0d2b) to create hexbins in QGIS 
geometry = [Point(xy) for xy in zip(dataframe.latitude, dataframe.longitude)]
crs = {'init': 'epsg:4326'}
geo_df = GeoDataFrame(dataframe, crs=crs, geometry=geometry)

geo_df.to_file(driver='ESRI Shapefile', filename='sf_crime_data.shp')