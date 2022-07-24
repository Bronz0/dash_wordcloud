
from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

from components import navbar

from app import app



# application layout
app.layout = html.Div(children=[
    navbar.navbar,
    html.Div(
        id="content",
        children=[
            html.H1("Dash Wordcloud"),
        ],
    ),
], )


# start the application
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)