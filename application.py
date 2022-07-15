from dash import Dash, dcc, html, Input, Output
from dash_app import app
from views import about, dashboard
import logging

logging.basicConfig(level=logging.INFO)
application = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/about':
        return about.layout
    elif pathname == '/':
        return dashboard.layout
    else:
        return '404'

if __name__ == '__main__':
    application.run(debug=True, port=8080)