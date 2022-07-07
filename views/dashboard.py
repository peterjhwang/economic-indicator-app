from dash import Input, Output, State, dcc, html, callback_context
import dash_bootstrap_components as dbc
import dash_table
import dash
import json
import requests
import flask
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import os
import base64
from datetime import datetime as dt
from utils.datetime_utils import unixTimeMillis, unixToDatetime, getMarks

from views.common import banner, footer
from dash_app import app

BACKEND_URL = os.getenv('DASHBOARD_BACKEND')
#USERNAME_PASSWORD = get_secret_from_kv('Api--Username') + ':' + get_secret_from_kv('Api--Password')
#encoded_u = base64.b64encode(USERNAME_PASSWORD.encode()).decode()
#headers = {"Authorization" : "Basic %s" % encoded_u}
headers = {}

measure_df = pd.DataFrame()

def generate_category_dropdown():
    url = f'{BACKEND_URL}/get_subjects'
    app.logger.info(url)
    r = requests.get(url, headers= headers)
    options = [{'label': 'All', 'value': 'All'}] + [{'label': sub, 'value': sub} for sub in r.json()['data']]
    return html.Div([
        html.Small('Category', style={'padding-right': '8px', 
            'margin': 'auto', 'width': '80px'}),
        dcc.Dropdown(
            id= 'category-dropdown',
            options= options,
            placeholder="Choose a subject",
            value='All',
            style={'font-size': '11px', 'color': '#333333', 'width': '100%'}
        )],
    style={'padding':'5px', 'display': 'flex'})

def generate_title_search():
    return html.Div([
                html.Small('Search', style={'padding-right': '8px', 
                    'margin': 'auto', 'width': '80px'}),
                dcc.Input(
                    id='title-search', placeholder="Search titles...", type="text",
                    style={'font-size': '11px', 'border-radius': '4px', 
                        'color':'#333',
                        'border': '1px solid #ccc'}
                )],
            style={'padding':'5px', 'display': 'flex'})
def generate_toggle():
    return html.Div([
        html.Div([dbc.Checklist(
            options=[
                {"label": "", "value": 1},
            ],
            value=[],
            id="regional-switch",
            switch=True,
            style={'margin-left': '5px'}
        ),
        html.P('Regional Only', style={'margin-right': '5px', 'font-size': '11px', 'margin-block': 'auto'})], style={'display': 'flex', 'width': '50%'}),
        html.Div([dbc.Checklist(
            options=[
                {"label": "", "value": 2},
            ],
            value=[],
            id="industry-switch",
            switch=True,
        ),
        html.Small('By Industry', style={'margin-right': '5px', 'font-size': '11px', 'margin-block': 'auto'})], style={'display': 'flex'})
    ], style={'display': 'flex', 'margin-top': '5px', 'margin-bottom': '5px'})

def generate_title_dropdown():
    url = f'{BACKEND_URL}/get_titles'
    app.logger.info(url)
    r = requests.get(url, headers= headers)
    options = [{'label': 'All', 'value': 'All'}] + [{'label': sub, 'value': sub} for sub in r.json()['data']]
    return html.Div([
                html.Small('Title', style={'padding-right': '8px', 
                    'margin': 'auto', 'width': '80px'}),
                dcc.Dropdown(
                    id='title-dropdown',
                    options=options,
                    value='All',
                    placeholder="Choose a subject first",
                    style={'font-size': '11px', 'color': '#333333', 'width': '100%'}
                )],
            style={'padding':'5px', 'display': 'flex'})

def generate_table():
    url = f'{BACKEND_URL}/get_table'
    app.logger.info(url)
    r = requests.post(url, json={'category': None, 'title': None, 'regional': False, 'industry': False}, headers= headers)
    global measure_df
    measure_df = pd.DataFrame(r.json()['data'])
    return dash_table.DataTable(
        id='measure-table',
        columns=[
            {'name': i, 'id': i} for i in ['Title', 'Geo', 'Label1', 'Label2', 'Label3', 'Unit']
            # omit the id column
            if i != 'id'
        ],
        css=[
            {
                'selector': 'table',
                'rule': 'width: 100%;',
            }
        ],
        style_header={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 100,
            'font-size': '11px',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 100,
            'font-size': '10px'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        data=measure_df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode='multi',
        row_selectable='multi',
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 6,
        style_table={'overflow-x':'auto'}
    )

def generate_slide():
    url = f'{BACKEND_URL}/get_timeframe'
    app.logger.info(url)
    r = requests.get(url, headers= headers)
    return dcc.RangeSlider(
        id= 'date-range-slider',
        min=unixTimeMillis(pd.to_datetime(r.json()['min'])),
        max=unixTimeMillis(pd.to_datetime(r.json()['max'])),
        step=2629800,
        value=[unixTimeMillis(dt.now() - pd.DateOffset(years=3, month=1, normalize=True) + pd.DateOffset(days=1)), 
            unixTimeMillis(pd.to_datetime(r.json()['max']))
        ],
        marks=getMarks(pd.to_datetime(r.json()['min']), pd.to_datetime(r.json()['max'])),
    )

def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Div(id='trigger'),
            html.B("Select Metric"),
            html.Div(style={'padding-bottom': '8px'}),
            generate_category_dropdown(),
            #generate_title_search(),
            generate_title_dropdown(),
            generate_toggle(),
            generate_table(),
            #dbc.Input(placeholder="Search metric", size="sm"),
            html.Br(),
            html.Div([dbc.Button(id='add-left-btn', className="btn btn-primary btn-sm", children='Add (left yaxis)'),
                dbc.Button(id='add-right-btn', className="btn btn-primary btn-sm", children='Add (right yaxis)',
                    style={'margin-left': '5px'}),
                dbc.Button(id='reset-btn', className="btn btn-primary btn-sm", children='Reset',
                    style={'margin-right': '0px', 'margin-left': '5px'})
                ], style={'display': 'flex', 'float': 'right', 'padding-bottom': '8px'}),
            html.Br(),
            html.Br(),
            html.B("Time Frame"),
            generate_slide(),
            dbc.Row([dbc.Col(html.Div(id='from-date', children='', style={'padding-left': '10px'})),
                dbc.Col(html.Div(id='to-date', style={'text-align': 'right', 'padding-right': '10px'}, children=''))]
            ),
            html.Br(), 

            #html.B("Custom Data"),
            #dbc.FormText("Upload a CSV file -- in progress"),
            dcc.Upload(
                id='datatable-upload',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')],
                    style={'font-size': '10px', 'text-align': 'center'}
                ),
                style={
                    'width': '95%', 'height': '60px', 'lineHeight': '55px', 'display': 'None',
                    'borderWidth': '1px', 'borderStyle': 'dashed',
                    'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px',
                },
            ),
        ],
    )

layout = dbc.Container([
        # Banner
        dbc.Row(dbc.Col(banner.load_banner())),
        dbc.Row([
            # Left column
            dbc.Col(
                html.Div(className='dashboard-graphbox',
                    children=[generate_control_card()],
                ), md=6, lg=5, xl=4
            ),
            # Right column
            dbc.Col([html.Div(className='dashboard-graphbox',
                    children=[
                        # Patient Volume Heatmap
                        html.Div(
                            id="chart-area1",
                            children=[
                                dbc.Row([
                                    dbc.Col([html.B("NZ Data Trend "),
                                        html.Small(id='agg-level', children='', style={'font-size': '9px'})
                                        ]),
                                    dbc.Col(dbc.Button(id='download-csv', children="Download CSV", className="btn btn-primary btn-sm"), style = {'text-align':'end'})
                                ], justify="between",),
                                dcc.Graph(id="chart1", style={'height': '450px'}),
                                dcc.Download(id="download-text")
                            ],
                        ),
                    ],
                ),
                html.Div(className='dashboard-graphbox',
                    children=[
                        html.B('Correlation Heatmap'),
                        dcc.Graph(id="chart2", style={'height': '350px'}, figure={}),
                    ]
                )
                ], md=6, lg=7, xl=8
            )], 
        ), 
    html.Br(),
    footer.generate_footer('Data Source: Stats NZ'),
    ], style={'background-color': '#EDEDED'},
    fluid=True)

@app.callback(
    [Output('title-dropdown', 'options'),
    Output('title-dropdown', 'value'),
    Output('measure-table', 'data')#,Output("measure-table", "selected_rows")
    ],
    [Input('category-dropdown', 'value'),
    Input('title-dropdown', 'value'),
    Input('regional-switch', 'value'),
    Input('industry-switch', 'value'),
    ],
    prevent_initial_call=False
)
def category_dropdown_action(category, title, regional_switch, industry_switch):
    global measure_df
    is_regional = True if 1 in regional_switch else False
    is_industry = True if 2 in industry_switch else False
    #print(is_regional, category, title, is_industry) #debug
    if 'category-dropdown.value' in [p['prop_id'] for p in callback_context.triggered]:
        url = f'{BACKEND_URL}/get_titles'
        app.logger.info(url)
        title_response = requests.post(url, 
            json = {'category': category, 'regional': is_regional, 'industry': is_industry}, 
            headers= headers)
        if category == 'All':
            cat = category
        else:
            cat = category + ' All'
        options = [{'label': cat, 'value': 'All'}]\
            + [{'label': sub, 'value': sub} for sub in title_response.json()['data']]

        url = f'{BACKEND_URL}/get_table'
        app.logger.info(url)
        table_response = requests.post(url, 
            json = {'category': category, 'title': None, 'regional': is_regional, 'industry': is_industry}, 
            headers= headers)
        measure_df = pd.DataFrame(table_response.json()['data'])
        return [options, 'All',
                measure_df.to_dict('records')]
    elif 'title-dropdown.value' in [p['prop_id'] for p in callback_context.triggered]:
        url = f'{BACKEND_URL}/get_table'
        app.logger.info(url)
        table_response = requests.post(url, 
            json = {'category': category, 'title': title, 'regional': is_regional, 'industry': is_industry}, 
            headers= headers)
        measure_df = pd.DataFrame(table_response.json()['data'])
        return [dash.no_update, 
                dash.no_update,
                measure_df.to_dict('records')]
    else:
        url = f'{BACKEND_URL}/get_titles'
        app.logger.info(url)
        title_response = requests.post(url, 
            json = {'category': category, 'regional': is_regional, 'industry': is_industry}, 
            headers= headers)
        if category == 'All':
            cat = category
        else:
            cat = category + ' All'
        options = [{'label': cat, 'value': 'All'}] + [{'label': sub, 'value': sub} for sub in title_response.json()['data']]
        
        url = f'{BACKEND_URL}/get_table'
        app.logger.info(url)
        r = requests.post(url, 
            json={'category': None, 'title': None, 'regional': is_regional, 'industry': is_industry}, 
            headers= headers)
        measure_df = pd.DataFrame(r.json()['data'])
        return [options, title,
                measure_df.to_dict('records')]


@app.callback(
    [
        Output('from-date', 'children'),
        Output('to-date', 'children'),
        Output('chart1', 'figure'),
        Output('agg-level', 'children'),
        Output('chart2', 'figure'),
        Output("download-text", "data"),
        Output("measure-table", "selected_rows")        
    ],
    [
        Input('add-left-btn', 'n_clicks'),
        Input('add-right-btn', 'n_clicks'),
        Input('reset-btn', 'n_clicks'),
        Input('download-csv', 'n_clicks'),
        Input('date-range-slider', 'value'),
    ], 
    State('measure-table', 'selected_rows'))
def add_text(left_btn, right_btn, reset_btn, download_csv, date_range, selected_row_ids):
    # get cookie
    cookie = flask.request.cookies.to_dict(flat=False)['_ga'][0]

    # get date range
    from_date = unixToDatetime(date_range[0]) 
    to_date = unixToDatetime(date_range[1])

    if 'reset-btn.n_clicks' in [p['prop_id'] for p in callback_context.triggered]:
        url = f'{BACKEND_URL}/reset_metric'
        app.logger.info(url)
        r = requests.post(url, json = {'cookie': cookie}, headers= headers)
        return [from_date, to_date, {}, '', {}, None, []]

    # axis
    if ('add-left-btn.n_clicks' in [p['prop_id'] for p in callback_context.triggered]) \
        or ('add-right-btn.n_clicks' in [p['prop_id'] for p in callback_context.triggered]):
        if len(selected_row_ids) != 0:
            temp = measure_df.loc[selected_row_ids, ['Title', 'Geo', 'Label1', 'Label2', 'Label3']].copy()
            print(temp['Title'].unique())
            if 'add-left-btn.n_clicks' in [p['prop_id'] for p in callback_context.triggered]:
                temp['secondary_y'] = False
            elif 'add-right-btn.n_clicks' in [p['prop_id'] for p in callback_context.triggered]:
                temp['secondary_y'] = True
            json_data = {'cookie': cookie,
                        'metrics': temp[['Title', 'Geo', 'Label1', 'Label2', 'Label3', 'secondary_y']].to_dict('records')}
            url = f'{BACKEND_URL}/add_metric'
            app.logger.info(url)
            r = requests.post(url, json = json_data, headers= headers)
    json_data = {'cookie': cookie, 'min': from_date, 'max': to_date}

    if 'download-csv.n_clicks' in [p['prop_id'] for p in callback_context.triggered]:
        url = f'{BACKEND_URL}/get_csv'
        app.logger.info(url)
        r = requests.post(url, json = json_data, headers= headers)
        return [from_date, to_date, dash.no_update, dash.no_update, dash.no_update, dict(content=r.json()['data'], filename=r.json()['filename']), []]
    else:
        url = f'{BACKEND_URL}/get_graphs'
        app.logger.info(url)
        r = requests.post(url, json = json_data, headers= headers)
        return [from_date, to_date, json.loads(r.json()['chart1']), r.json()['agg-level'], json.loads(r.json()['chart2']), None, []]
