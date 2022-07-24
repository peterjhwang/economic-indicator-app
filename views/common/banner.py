from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

def load_banner():
    return dbc.Navbar(
                dbc.Container(
                    [
                        html.A(
                        # Use row and col to control vertical alignment of logo / brand
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src='/assets/logo.png', height="30px")),
                                    dbc.Col(dbc.NavbarBrand("NZ Economic Indicator Prediction", className="ms-2", style={'fontWeight': 'bold'})),
                                ],
                                align="center",
                                className="g-0",
                            ),
                            href="/",
                            style={"textDecoration": "none"},
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.NavItem(dbc.NavLink("Playground", href="/", style={'padding': '8px'})), style={'padding': '5px'}),
                                dbc.Col(dbc.NavItem(dbc.NavLink("Prediction", href="/", style={'padding': '8px'})), style={'padding': '5px'}),
                                dbc.Col(dbc.NavItem(dbc.NavLink("About Me", href="/about", style={'padding': '8px'})),  style={'padding': '5px'})
                            ]
                        )
                    ],
                ),
                #brand="NZ-MacroEconomy Trend",
                #brand_href="/",
                color="primary",
                dark=True,
            )