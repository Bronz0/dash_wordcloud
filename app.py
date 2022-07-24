from dash import Dash
import dash_bootstrap_components as dbc

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    dbc.icons.BOOTSTRAP,
]

app = Dash(external_stylesheets=external_stylesheets,
           suppress_callback_exceptions=True)

server = app.server
