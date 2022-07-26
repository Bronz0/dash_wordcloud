from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from dash_holoniq_wordcloud import DashWordcloud

from utils import utils

from components import navbar

from app import app

security_data = [
    ["Equity", 74, "Zillions of equity based funds"],
    ["Bond", 45],
    ["Global", 30],
    ["Sector Equity", 17],
    ["EUR", 15],
    ["Large Cap", 13],
    ["Europe", 11],
]
# application layout
app.layout = html.Div(children=[
    navbar.navbar,
    html.Div(
        className="column",
        id="content",
        children=[
            html.Div(
                className="row box",
                children=[
                    dcc.Textarea(
                        className="text-area",
                        id="text-input",
                        placeholder="Input text here...",
                        value='',
                    ),
                ],
            ),
            html.Div(
                className="row box",
                children=[
                    html.Div(
                        className='col-md-3',
                        children=[
                            html.H4('N words'),
                            dcc.Dropdown([1, 2, 3], 1, id="n-words-dropdown", clearable=False),
                        ],
                    ),
                    html.Div(
                        className='col-md-3',
                        children=[
                            html.H4('Max words'),
                            dcc.Dropdown([10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                         30,
                                         id="max-words-dropdown", clearable=False),
                        ],
                    ),
                     html.Div(
                        className='col-md-3',
                        children=[
                            html.H4('Chart Type'),
                            dcc.Dropdown(["Static", "Interactive"],
                                         "Static",
                                         id="wordcloud-type", clearable=False),
                        ],
                    ),
                    html.Div(
                        className='col-md-3',
                        children=[
                            dbc.Button(
                                "Generate Wordcloud",
                                className="me-1",
                                id="wordcloud-button",
                                n_clicks=0,
                            ),
                        ],

                    ),
                ],
            ),
            html.Div(
                className="row box",
                children=[
                    html.H5("WordCloud"),
                    html.Br(),
                    html.Div(id='wordcloud'),
                ],
            ),
        ],
    ),
], )


@app.callback(
    Output('wordcloud', 'children'),
    Input('wordcloud-button', 'n_clicks'),
    State('text-input', 'value'),
    State('n-words-dropdown', 'value'),
    State("max-words-dropdown", 'value'),
    State("wordcloud-type", 'value'),
)
def generate_word_cloud(n_clicks, text, n_words, max_words, wordcloud_type):
    if (n_clicks > 0) & (text != ''):
        if wordcloud_type == "Static":
            image = utils.text_to_wordcloud(text, int(n_words), int(max_words))
            wordcloud = html.Img(src=image, style={'width': '100%'})
            return wordcloud
        else:
            data = utils.get_holoniq_wordcloud_data(text, int(n_words), int(max_words))
            holoniq_wordcloud = DashWordcloud(id='holoniq-wordcloud',
                                list=data,
                                width=900,
                                height=420,
                                gridSize=16,
                                color='#f0f0c0',
                                backgroundColor='#001f00',
                                shuffle=False,
                                rotateRatio=0.5,
                                shape='circle',
                                hover=True,
                                weightFactor=16,
                                shrinkToFit=True,
                                ),
            return holoniq_wordcloud
    else:
        return html.H6('Results will appear here...')


# start the application
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)