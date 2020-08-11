import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, timedelta
from helper.data import Data
from helper.styles import button


data = Data()
options = data.get_countries_list()


class Layout:

    def return_graph_div(self, status):
        return (html.Div(id=status, children=[html.Div([

            html.Div([html.H1(status.title() + ' Graph', id=status+'heading')], style={
                     'width': '100%', 'textAlign': 'center', 'color': '#bccbde', 'font-size': '20px', 'backgroundColor': '#000000'}),
            html.Div([html.H3('Select Countries:', style={'paddingRight': '30px'}),
                      dcc.Dropdown(
                id=status+'-my-ticker-symbol',
                options=options,
                value='Pakistan',
                multi=True
            )
            ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%'}), html.Div([
                html.H3('Select Date Range:', style={'paddingRight': '30px'}),
                dcc.DatePickerRange(
                    id=status+'-date-picker',
                    min_date_allowed=datetime(2020, 2, 1),
                    max_date_allowed=datetime.today(),
                    start_date=datetime.now() - timedelta(30),
                    end_date=datetime.today()

                )
            ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '50%', 'text-align': 'center'}),
            html.Div([
                html.Button(
                    id=status+'-submit-button',
                    n_clicks=0,
                    children='Submit',
                    style=button
                ),
            ], style={'text-align': 'center'}),
            dcc.Loading(id=status+'loading-icon', children=[
                html.Div(children=[
                    html.Div(
                        dcc.Graph(id=status+'-scatter-graph'), style={'display': 'inline-block'}),
                    html.Div(
                        dcc.Graph(id=status+'-historic-graph'), style={'display': 'inline-block'})], style={'width': '100%', 'display': 'inline-block'})], type='graph')
        ])
        ])
        )
