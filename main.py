import pandas as pd
import requests
import numpy as np
from chart_studio import plotly as py
import plotly.express as px
import os
import chart_studio.tools
from dotenv import load_dotenv

load_dotenv()

chart_studio.tools.set_credentials_file(username=os.getenv('USER'), api_key=os.getenv('KEY'))


def percentile(a, data):
    perc = 0
    for x in data:
        if a > x:
            perc += 1
    return perc / len(data) * 100


def get_leaderboard(lb_id):
    chart = list()
    i = 0
    step = 10000
    while len(chart) == i:
        url = f'https://aoe2.net/api/leaderboard?game=aoe2de&leaderboard_id={lb_id}&start={i + 1}&count={step}'
        response = requests.get(url)
        leaderboard = response.json()['leaderboard']
        for player in leaderboard:
            chart.append(player['rating'])
        i += step
    df = pd.DataFrame(chart, columns=[''])
    return df


def make_histogram(df, percentiles, nbins):
    fig = px.histogram(data_frame=df, color_discrete_sequence=['green'], template='plotly_white',
                       labels={'x': 'Rating'}, nbins=nbins)
    ht = '''
    <b># of Players: </b> %{y} <br>
    <b>Rating range: </b> %{x} <br>
    <b>Percentile: </b> %{hovertext}%
    '''
    fig.update_traces(hovertext=percentiles)
    fig.update_traces(hovertemplate=ht)
    fig.update_layout(hovermode="x")
    return fig


def make_scatter_plot(df_x, df_y):
    pass


def make_percentiles(df, nbins):
    return [round(percentile(x, df.values), 1) for x in np.histogram(df.values, nbins)[1]]


df_3 = get_leaderboard(3)
percentiles_3 = make_percentiles(df_3, 258)
fig_3 = make_histogram(df_3, percentiles_3, 258)

df_4 = get_leaderboard(4)
percentiles_4 = make_percentiles(df_4, 285)
fig_4 = make_histogram(df_4, percentiles_4, 285)

#fig_scatter = make_scatter_plot(df_3, df_4)

solo_plot_url = py.plot(fig_3, height=500, width=1300, filename='chart3')
team_plot_url = py.plot(fig_4, height=500, width=1300, filename='chart4')
#scatter_plot_url = py.plot(fig_3, height=500, width=1300, filename='scatter')

html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin: auto auto; background:whitesmoke; }</style>
    </head>
    <body>
    <div class="container">
        <div class="centered">
            <h3>Age of Empires II: Definitive Edition Rating Charts</h3>

            <!-- *** Section 1 *** --->
            <iframe width="1200" height="500" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + solo_plot_url + '''.embed?width=1300&height=500"></iframe>

            <!-- *** Section 2 *** --->
            <iframe width="1200" height="500" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + team_plot_url + '''.embed?width=1300&height=500"></iframe>
        </div>
    </div>
    </body>
</html>'''

f = open('index.html', 'w')
f.write(html_string)
f.close()