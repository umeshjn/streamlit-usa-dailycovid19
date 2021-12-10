# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 15:14:25 2021

@author: 501796582
"""

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import datetime
from datetime import datetime, timedelta

st.markdown("## Daily Covid 19 Cases and Deaths - USA")

## Covid Numbers from Nytimes github repository
states = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")

# Adding Markdown text 
st.markdown("""
    Covid-19 - the virus which brough the all powerful humans to their knees since last two years, it has wrecked havoc like never seen before and devasted the individuals, families, states, countries and the world as a whole.
""")

st.markdown("""
    This application gives you a single page view of the map and the table of daily Covid-19 numbers for the selected date.
""")

selected_date = st.date_input(
	"Select the Date to view the Covid Numbers", 
	datetime.date(datetime(2021, 11, 16))
)

codes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
codes = codes[['code', 'state']]
df = pd.merge(codes, states, on = 'state')

df['dailycases'] = df.groupby('state')['cases'].diff()
df['dailydeaths'] = df.groupby('state')['deaths'].diff()
df.columns = ['Code', 'State', 'LastUpdatedDate', 'Fips', 'TotalCases', 'TotalDeaths', 'DailyCases', 'DailyDeaths']
selected = df[df['LastUpdatedDate'] == str(selected_date)]
selected = selected.reset_index()

previous_date = (datetime.strptime(str(selected_date), "%Y-%m-%d") - timedelta(days=1)).strftime('%Y-%m-%d')
previous = df[df['LastUpdatedDate'] == str(previous_date)]
previous = previous.reset_index()

caseschange = int(float(str(selected[['DailyCases']].sum()[0]))) - int(float(str(previous[['DailyCases']].sum()[0])))
deathschange = int(float(str(selected[['DailyDeaths']].sum()[0]))) - int(float(str(previous[['DailyDeaths']].sum()[0])))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Cases", str(selected[['TotalCases']].sum()[0]), int(float(str(selected[['DailyCases']].sum()[0]))))
col2.metric("Total Deaths", str(selected[['TotalDeaths']].sum()[0]), int(float(str(selected[['DailyDeaths']].sum()[0]))))
col3.metric("Daily Cases", int(float(str(selected[['DailyCases']].sum()[0]))), caseschange)
col4.metric("Daily Deaths", int(float(str(selected[['DailyDeaths']].sum()[0]))), deathschange)

for col in selected.columns:
    selected[col] = selected[col].astype(str)

selected['text'] = selected['State'] + '<br>' + \
    'Daily Cases ' + selected['DailyCases'] + '<br>' + \
    'Daily Deaths ' + selected['DailyDeaths'] + '<br>'

fig = go.Figure(data=go.Choropleth(
    locations=selected['Code'],
    z=selected['DailyCases'].astype(float),
    locationmode='USA-states',
    colorscale='Reds',
    autocolorscale=False,
    text=selected['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Number of Daily Covid Cases"
))

fig.update_layout(
	title_text='Hover over States for Numbers',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='crimson'),
	showlegend = False
)


st.plotly_chart(fig)

st.table(selected[['Code', 'State', 'Fips', 'DailyCases', 'DailyDeaths']])



import plotly.graph_objects as go

states1 = selected[['State', 'DailyCases']].sort_values(by = 'DailyCases', ascending=False)[:5]

fig = go.Figure(go.Bar(
            x=states1['DailyCases'].to_list(),
            y=states1['State'].to_list(),
            orientation='h',
            marker_color = "crimson"))
fig.update_layout(title_text='Top 5 States with Most Cases')
st.plotly_chart(fig)

states1 = selected[['State', 'DailyDeaths']].sort_values(by = 'DailyDeaths', ascending=False)[:5]

fig = go.Figure(go.Bar(
            x=states1['DailyDeaths'].to_list(),
            y=states1['State'].to_list(),
            orientation='h',
            marker_color = "crimson"))
fig.update_layout(title_text='Top 5 States with Most Deaths')
st.plotly_chart(fig)

st.header("Credits")

st.markdown("This application uses the Covid-19 Data Repository of The NewYork Times.")