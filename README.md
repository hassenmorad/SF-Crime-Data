# Automated Data Collection &amp; Visualization
This repository contains files collected and produced while recreating visualizations from this [Hoodline news article](https://hoodline.com/2018/11/the-week-in-sf-crime-reports-overall-complaints-drop-harassment-calls-climb) on weekly crime in San Francisco. My objective was to demonstrate that more effective visualizations could be produced even with Hoodline's automation-centered approach. I've posted a more detailed outline of my thought process [here](https://hassenmorad.github.io/hoodline.html).

## Workflow Summary:
1. Collection
    - Crimeometer SF Crime Data: Pulled data on all crimes committed in SF from 11/5/18 - 11/11/18  from [Crimeometer's API](https://www.crimeometer.com/crime-data-api) (sf_crimeometer_api_data.py)
2. Cleaning
    
    a) Bar Chart & Map:
      - Converted Crimeometer JSON data to Pandas data frame for basic cleaning, then converted to shapefile (sf_crime_data.shp)
    
    b) Map:
      - Created hexbin shapefile in QGIS (sf_hexbins.shp), representing all hex areas in SF where crimes were recorded
      - Extracted top 5 crimes and counts in each hexbin (Mapping_Crime_Stats.ipynb) (for pop up crime stats in map); joined data with hexbin shapefile to link each hexbin w/ the number of crimes that occurred in it (hex_offenses.shp)
3. Visualization

    a) Bar Chart:
      - Plotted top 12 crimes via Altair horizontal bar chart
      
    b) Map:
      - Uploaded hexbins shapefile to Mapbox Studio and implemented hexbin shading 
      - Created html file with Mapbox GL JS code enabling interactivity (zoom & pop up window with crime stats upon hover)

### Notes:
- The current workflow is partially automated. I proceeded with this combination of automated & manual tasks (e.g. QGIS & Mapbox Studio) to create an initial framework. This process can certainly be almost entirely automated by scripting QGIS data manipulation via PyQGIS and importing shapefiles directly into a Mapbox GL JS script (as opposed to using Studio).
