# Automated Data Collection &amp; Visualization
This repository contains files collected and produced while recreating visualizations from this [Hoodline news article](https://hoodline.com/2018/11/the-week-in-sf-crime-reports-overall-complaints-drop-harassment-calls-climb) on weekly crime in San Francisco. My objective was to demonstrate that more effective visualizations could be produced even with Hoodline's automation-centered approach. I've posted a more detailed outline of my thought process [here]().

## Workflow Summary:
1. Collection
    - Crimeometer SF Crime Data: All crimes committed in SF from 11/5/18 - 11/11/18 pulled from [Crimeometer's API](https://www.crimeometer.com/crime-data-api)
2. Cleaning
    - Converted Crimeometer JSON data to Pandas data frame for basic cleaning
    - Converted data frame to shapefile to create hexbin shapefile (in QGIS), representing the number of crimes that occurred in each subsection of SF
    - Extracted top 5 crimes and counts in each hexbin (for pop up crime stats in map); joined data with hexbin shapefile
3. Visualization

    a) Bar Chart:
      - Plotted top 12 crimes via Altair horizontal bar chart
      
    b) Map:
      - Uploaded hexbins shapefile to Mapbox Studio and implemented hexagon shading 
      - Created html file with Mapbox GL JS code enabling interactivity (zoom & pop up window with crime stats upon hover)
