from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

from views.common import banner, footer

text = '''dbc.Row([
        dbc.Col(
            dbc.Card(className = 'card border-primary mb-3', children=[
                        dbc.CardImg(src="assets/logo.png", top=True, style={'height': '150px'}),
                        dbc.CardBody(
                            [
                                html.H5("Card title", className="card-title"),
                                dbc.Badge("Optimisation", color="info", className="me-1", style={'margin': '5px'}),
                                html.P(
                                    "Some quick example text to build on the card title and "
                                    "make up the bulk of the card's content.",
                                ),
                                dbc.Button("Read", color="primary", className="btn btn-primary btn-sm"),
                            ]
                        ),
                    ],
                ), style = {'max-width': '20rem'}
            ),
        dbc.Col(
            dbc.Card(className = 'card border-primary mb-3', children=[
                        dbc.CardImg(src="assets/logo.png", top=True, style={'height': '150px'}),
                        dbc.CardBody(
                            [
                                html.H5("Card title", className="card-title"),
                                dbc.Badge("Visualisation", color="secondary", className="me-1", style={'margin': '5px'}),
                                html.P(
                                    "Some quick example text to build on the card title and "
                                    "make up the bulk of the card's content.",
                                ),
                                dbc.Button("Read", color="primary", className="btn btn-primary btn-sm"),
                            ]
                        ),
                    ],
                ), style = {'max-width': '20rem'}
            )
        ]
    ),
    dbc.Col()
    '''

portfolios = [
    html.H2('Blog Posts'),
    html.Br(),
    html.Img(src='assets/coming_soon.jpg', style={'display': 'block',
        'height': '60vh',
        'margin-left': 'auto',
        'margin-right': 'auto'
    })
]

layout = dbc.Container([
    banner.load_banner(),
    html.Hr(),
    html.H2('Driven to solve business problem through Data Science', style={'fontWeight': 'bold',
        'padding': '10px'}),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Img(src='assets/peter_hwang.jpeg', width='100%'), md=4),
        dbc.Col([
            html.Div(children=[
                html.Br(),
                html.Small('Hi, My name is '),
                html.B('Peter Hwang', className='text-info'),
                html.Small('. I am currently working as a data scientist. Let me explain a bit more about myself and how I got here now.'),
                html.Br(),
                html.Br(),
                html.Small('Firstly I got a BBA degree specialising in the global finance area. After falling in love with coding, I did another degree, double-majoring in Computer Science and Data Science. Since then, I have been trying to help businesses grow using my data science skills and my business acumen. In my free time, I spend my time on the macro-economy and stock market to try to understand/predict the future. '),
                html.Br(),
                html.Br(),
                html.Small('Apart from that, I am trying to be a good husband and father of two boys. An outdoor person love paddle boarding, swimming and trekking.'),
                html.Br(),
                html.Small(className='text-secondary', children='')
                ], style={'padding': '10px'}
            )
        ], md=8)
    ]),
    html.Br(),

    html.Br(),
    html.Hr(),
    html.Div(id='portfolio', children = portfolios),
    footer.generate_footer('')
], fluid=True)