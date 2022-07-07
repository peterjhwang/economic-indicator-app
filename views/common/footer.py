from dash import dcc, html
import dash_bootstrap_components as dbc

def generate_footer(text):
    return dbc.Row([dbc.Col(
            # Footer
                html.Div(
                    children = text,
                ), style={'text-align':'left', 'margin': 'auto'}
            , width=6),
            dbc.Col(
                [html.A([html.Img(src='assets/linkedin-logo.png', style={'height': '25px', 'padding-right': '8px'})],
                    href='https://www.linkedin.com/in/peterjhwang/'),
                html.A([html.Img(src='assets/email-icon.png', style={'height': '25px', 'padding-right': '8px'})],
                    href='mailto:peterhwang105@gmail.com'),                
                ], style={'text-align':'right', 'margin': 'auto'}
            )
        ],
        style={'color':'#fff',
                'font-size':'12px',
                'padding':'10px',
                'height':'50px',
                'background-color':'#343a40'
            }
    )