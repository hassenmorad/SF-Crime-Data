# Linking crime stats w/ hexbins created in QGIS
import pandas as pd
import numpy as np
import geopandas as gpd

sf_crime = gpd.read_file('sf_crime_data.shp')
hex_bins = gpd.read_file('sf_hexbins.shp')

offenses = {0:[], 1:[], 2:[], 3:[], 4:[]}
counts = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
incidents = []

for row in hex_bins.itertuples():
    hex_left = row.left
    hex_bottom = row.bottom
    hex_right = row.right
    hex_top = row.top
    offenses_dict = {}
    
    for row2 in sf_crime.itertuples():
        lat = row2.latitude
        lon = row2.longitude
        incident = row2.incident_c
        if (lon > hex_left and lon < hex_right) and (lat > hex_bottom and lat < hex_top) and (incident not in incidents):
            incidents.append(incident)
            offense = row2.offense
            if offense in offenses_dict:
                offenses_dict[offense] += 1
            else:
                offenses_dict[offense] = 1
                
    # Storing top 5 offenses and corresponding counts in separate dicts (which will be converted to dfs and joined together)    
    top5 = sorted(offenses_dict.items(), key=lambda x: x[1], reverse=True)[:5]  # Sorting offenses dict by values in descending order
    top5_count = len(top5)
    
    for i in range(top5_count):
        offenses[i].append(top5[i][0])
        counts[i].append(top5[i][1])
    if top5_count < 5:
        for i in range(top5_count, 5):
            offenses[i].append(np.nan)
            counts[i].append(np.nan)
    counts[5].append(sum([x[1] for x in top5]))

off_df = pd.DataFrame.from_dict(offenses)
off_df.columns = ['Offense1', 'Offense2', 'Offense3', 'Offense4', 'Offense5']

counts_df = pd.DataFrame.from_dict(counts)
counts_df.columns = ['Count1', 'Count2', 'Count3', 'Count4', 'Count5', 'Total_Count']

top5_offenses = off_df.join(counts_df)
hex_offenses = hex_bins.join(top5_offenses)

hex_offenses.to_file('hex_offenses.shp')