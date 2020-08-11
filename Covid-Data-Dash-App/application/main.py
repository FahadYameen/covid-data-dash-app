
###############################################################################
#                                MAIN                                         #
###############################################################################


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
from helper.data import Data
from helper.layout import Layout
from helper.styles import tab_selected_style, graphStyleJson
import time
import copy
from helper.constants import *


app = dash.Dash(__name__)
app.title = APP_TITLE


app.index_string = APP_HTML


server = app.server

data = Data()
layout = Layout()
options = data.get_countries_list()

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Commulative Statistics', value='tab-1',
                selected_style=tab_selected_style),
        dcc.Tab(label='Per Day Stastics', value='tab-2',
                selected_style=tab_selected_style),
    ], style={'width': '100%', 'font-size': '20px', 'font-weight': 'bold', 'letter-spacing:': '10px'}),
    html.Div([
        layout.return_graph_div('confirmed-cases'),
        layout.return_graph_div('active-cases'),
        layout.return_graph_div('recoveries'),
        layout.return_graph_div('deaths')
    ], id='tab-1-div'),
    html.Div([
        layout.return_graph_div('daily-confirmed-cases'),
        layout.return_graph_div('daily-active-cases'),
        layout.return_graph_div('daily-recoveries'),
        layout.return_graph_div('daily-deaths')
    ], id='tab-2-div')
])


@app.callback(
    [Output('active-cases-scatter-graph', 'figure'),
     Output('active-cases-historic-graph', 'figure')],
    [Input('active-cases-submit-button', 'n_clicks')],
    [State('active-cases-my-ticker-symbol', 'value'),
     State('active-cases-date-picker', 'start_date'),
     State('active-cases-date-picker', 'end_date')]
)
def update_active_graph(n_clicks, value, start_date, end_date):

    traces_confirmed = data.get_data_wrt_date(
        value, 'confirmed', start_date, end_date, False)
    traces_recoveries = data.get_data_wrt_date(
        value, 'recovered', start_date, end_date, False)
    traces_deaths = data.get_data_wrt_date(
        value, 'deaths', start_date, end_date, False)

    traces_active = traces_confirmed

    for country_idx in range(len(traces_active)):
        for y_val_idx in range(len(traces_active[country_idx]['y'])):
            traces_active[country_idx]['y'][y_val_idx] = traces_confirmed[country_idx]['y'][y_val_idx] - \
                traces_recoveries[country_idx]['y'][y_val_idx] - \
                traces_deaths[country_idx]['y'][y_val_idx]

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_active
    fig['layout']['yaxis']['title'] = "Active Cases"

    tmp = copy.deepcopy(traces_active)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = "Active Cases"

    return fig, fig1


@app.callback(
    [Output('recoveries-scatter-graph', 'figure'),
     Output('recoveries-historic-graph', 'figure')],
    [Input('recoveries-submit-button', 'n_clicks')],
    [State('recoveries-my-ticker-symbol', 'value'),
     State('recoveries-date-picker', 'start_date'),
     State('recoveries-date-picker', 'end_date')]
)
def update_recoveries_graph(n_clicks, value, start_date, end_date):

    traces_recoveries = data.get_data_wrt_date(
        value, 'recovered', start_date, end_date, False)

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_recoveries
    fig['layout']['yaxis']['title'] = RECOVERED_CASES

    tmp = copy.deepcopy(traces_recoveries)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = RECOVERED_CASES

    return fig, fig1


@app.callback(
    [Output('confirmed-cases-scatter-graph', 'figure'),
     Output('confirmed-cases-historic-graph', 'figure')],
    [Input('confirmed-cases-submit-button', 'n_clicks')],
    [State('confirmed-cases-my-ticker-symbol', 'value'),
     State('confirmed-cases-date-picker', 'start_date'),
     State('confirmed-cases-date-picker', 'end_date')]
)
def update_confirmed_graph(n_clicks, value, start_date, end_date):

    traces_confirmed = data.get_data_wrt_date(
        value, 'confirmed', start_date, end_date, False)

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_confirmed
    fig['layout']['yaxis']['title'] = CONFIRMED_CASES

    tmp = copy.deepcopy(traces_confirmed)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = CONFIRMED_CASES

    return fig, fig1


@app.callback(
    [Output('deaths-scatter-graph', 'figure'),
     Output('deaths-historic-graph', 'figure')],
    [Input('deaths-submit-button', 'n_clicks')],
    [State('deaths-my-ticker-symbol', 'value'),
     State('deaths-date-picker', 'start_date'),
     State('deaths-date-picker', 'end_date')]
)
def update_deaths_graph(n_clicks, value, start_date, end_date):

    traces_deaths = data.get_data_wrt_date(
        value, 'deaths', start_date, end_date, False)

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_deaths
    fig['layout']['yaxis']['title'] = DEATHS_CASES

    tmp = copy.deepcopy(traces_deaths)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = DEATHS_CASES

    return fig, fig1


@app.callback(
    [Output('daily-active-cases-scatter-graph', 'figure'),
     Output('daily-active-cases-historic-graph', 'figure')],
    [Input('daily-active-cases-submit-button', 'n_clicks')],
    [State('daily-active-cases-my-ticker-symbol', 'value'),
     State('daily-active-cases-date-picker', 'start_date'),
     State('daily-active-cases-date-picker', 'end_date')]
)
def update_daily_active_graph(n_clicks, value, start_date, end_date):

    traces_confirmed = data.get_data_wrt_date(
        value, 'confirmed', start_date, end_date, False)
    traces_recoveries = data.get_data_wrt_date(
        value, 'recovered', start_date, end_date, False)
    traces_deaths = data.get_data_wrt_date(
        value, 'deaths', start_date, end_date, False)

    traces_active = traces_confirmed

    for country_idx in range(len(traces_active)):
        for y_val_idx in range(len(traces_active[country_idx]['y'])):
            traces_active[country_idx]['y'][y_val_idx] = traces_confirmed[country_idx]['y'][y_val_idx] - \
                traces_recoveries[country_idx]['y'][y_val_idx] - \
                traces_deaths[country_idx]['y'][y_val_idx]

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_active
    fig['layout']['yaxis']['title'] = ACTIVE_CASES

    tmp = copy.deepcopy(traces_active)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = ACTIVE_CASES

    return fig, fig1


@app.callback(
    [Output('daily-recoveries-scatter-graph', 'figure'),
     Output('daily-recoveries-historic-graph', 'figure')],
    [Input('daily-recoveries-submit-button', 'n_clicks')],
    [State('daily-recoveries-my-ticker-symbol', 'value'),
     State('daily-recoveries-date-picker', 'start_date'),
     State('daily-recoveries-date-picker', 'end_date')]
)
def update_daily_recoveries_graph(n_clicks, value, start_date, end_date):

    traces_recoveries = data.get_data_wrt_date(
        value, 'recovered', start_date, end_date, True)

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_recoveries
    fig['layout']['yaxis']['title'] = RECOVERED_CASES

    tmp = copy.deepcopy(traces_recoveries)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = RECOVERED_CASES

    return fig, fig1


@app.callback(
    [Output('daily-confirmed-cases-scatter-graph', 'figure'),
     Output('daily-confirmed-cases-historic-graph', 'figure')],
    [Input('daily-confirmed-cases-submit-button', 'n_clicks')],
    [State('daily-confirmed-cases-my-ticker-symbol', 'value'),
     State('daily-confirmed-cases-date-picker', 'start_date'),
     State('daily-confirmed-cases-date-picker', 'end_date')]
)
def update_daily_confirmed_graph(n_clicks, value, start_date, end_date):

    traces_confirmed = data.get_data_wrt_date(
        value, 'confirmed', start_date, end_date, True)

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_confirmed
    fig['layout']['yaxis']['title'] = CONFIRMED_CASES

    tmp = copy.deepcopy(traces_confirmed)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = CONFIRMED_CASES

    return fig, fig1


@app.callback(
    [Output('daily-deaths-scatter-graph', 'figure'),
     Output('daily-deaths-historic-graph', 'figure')],
    [Input('daily-deaths-submit-button', 'n_clicks')],
    [State('daily-deaths-my-ticker-symbol', 'value'),
     State('daily-deaths-date-picker', 'start_date'),
     State('daily-deaths-date-picker', 'end_date')]
)
def update_daily_deaths_graph(n_clicks, value, start_date, end_date):

    traces_deaths = data.get_data_wrt_date(
        value, 'deaths', start_date, end_date, True)

    fig = copy.deepcopy(graphStyleJson)
    fig['mode'] = "lines+markers"
    fig['data'] = traces_deaths
    fig['layout']['yaxis']['title'] = DEATHS_CASES

    tmp = copy.deepcopy(traces_deaths)
    for item in tmp:
        item['type'] = 'bar'

    fig1 = copy.deepcopy(graphStyleJson)
    fig1['data'] = tmp
    fig1['layout']['yaxis']['title'] = DEATHS_CASES

    return fig, fig1


@app.callback([Output('tab-1-div', 'style'), Output('tab-2-div', 'style')],
              [Input('tabs', 'value')])
def tab_change(tab_value):
    if(tab_value == 'tab-1'):
        return({'visibility': 'visible'}, {'display': 'none'})
    else:
        return({'display': 'none'}, {'visibility': 'visible'})
