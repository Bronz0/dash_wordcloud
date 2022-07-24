import dash_bootstrap_components as dbc
from dash import html
from dash_bootstrap_components._components.Container import Container


navbar = dbc.Navbar(
    children=[
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavbarBrand("Dash Wordcloud", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://github.com/Bronz0/dash_wordcloud",
                    target="_blanck",
                    style={"textDecoration": "none"},
                ),
            ]
        ),
    ],
    color="light",
    dark=False,
)
