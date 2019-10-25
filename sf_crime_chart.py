# Creating Bar Charts Summarizing SF Weekly Crime Stats
import pandas as pd
from chart_theme import chart_theme
import geopandas as gpd
import altair as alt

alt.themes.register("chart_theme", chart_theme)
alt.themes.enable("chart_theme")

sf_crime = gpd.read_file('sf_crime_data.shp')  # Data pulled from Crimometer API
dates = sf_crime.date.apply(lambda x:x.replace('-', '/'))
crimes = sf_crime.offense.value_counts().index[:13]
counts = sf_crime.offense.value_counts().values[:13]
crime_counts_df = pd.DataFrame({'Crime':crimes, 'Count':counts})
crime_counts_df = crime_counts_df[crime_counts_df.Crime != 'Other']  # Excluding 'Other' from chart results (b/c unuseful to reader)

cities = ['San Francisco']
week_beg = dates.iloc[-1][-5:]
week_end = dates.iloc[0][-5:]
max_val = crime_counts_df.Count.max()

for city in cities:
    title = city + ' Crime (' + week_beg + ' - ' + week_end + ')'

    base = alt.Chart(crime_counts_df, title=title).encode(
    x=alt.X('Count', axis=None),
    y=alt.Y('Crime', title='Top crimes recorded by ' + city + ' PD', sort=list(crime_counts_df.Crime.values)))

    bars = base.mark_bar(size=22).encode(color=alt.condition(
        alt.datum.Count == max_val,
        alt.value('#e17700'),
        alt.value('#00648e')))

    text = base.mark_text(
        color='white',
        align='right',
        size=12,
        dx=-3
        ).encode(
        text='Count')

    chart = bars + text
    chart.save(city + '_crime_counts.png', scale_factor=3)