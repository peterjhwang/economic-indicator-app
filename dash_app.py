import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.MINTY],
    #external_scripts = ['https://nz-data.azurewebsites.net/assets/gtag.js'],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])
app.title = "NZ Economic Indicator Prediction Project"