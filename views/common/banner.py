from dash import Input, Output, dcc, html, State
import dash_bootstrap_components as dbc
from dash_app import app

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

page_bar = dbc.Row(
                    [
                        dbc.Col(dbc.NavItem(dbc.NavLink("Playground", href="/", style={'padding': '8px'})), style={'padding': '5px'}),
                        dbc.Col(dbc.NavItem(dbc.NavLink("Prediction", href="/", style={'padding': '8px'})), style={'padding': '5px'}),
                        dbc.Col(dbc.NavItem(dbc.NavLink("About Me", href="/about", style={'padding': '8px'})),  style={'padding': '5px'})
                    ],
                className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                align="center",
            )


def load_banner():
    return dbc.Navbar(
                dbc.Container(
                    [
                        html.A(
                        # Use row and col to control vertical alignment of logo / brand
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src='/assets/logo.png', height="40px"), style={'padding-left': '5px', 'padding-right': '5px'}),
                                    dbc.Col(dbc.NavbarBrand("NZ Economic Indicator Prediction", className="ms-2", style={'fontWeight': 'bold'})),
                                ],
                                align="center",
                                className="g-0",
                            ),
                            href="/",
                            style={"textDecoration": "none"},
                        ),
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        dbc.Collapse(
                            page_bar,
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        ),
                    ],
                    style={'max-width': 'none'}
                ),
                #brand="NZ-MacroEconomy Trend",
                #brand_href="/",
                color="primary",
                dark=True,
            )

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open