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
                    ),
                ],
            ),
            html.Div(
                className="row box",
                children=[
                    html.Div(
                        className='col-md-4',
                        children=[
                            html.H4('N words'),
                            dcc.Dropdown([1, 2, 3], 2, id="n-words-dropdown", clearable=False),
                        ],
                    ),
                    html.Div(
                        className='col-md-4',
                        children=[
                            html.H4('Max words'),
                            dcc.Dropdown([10, 20, 30, 40, 50],
                                         20,
                                         id="max-words-dropdown", clearable=False),
                        ],
                    ),
                    html.Div(
                        className='col-md-4',
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
            # html.Div([
            #     DashWordcloud(id='wordcloud',
            #                   list=security_data,
            #                   width=900,
            #                   height=600,
            #                   gridSize=30,
            #                   color='#f0f0c0',
            #                   backgroundColor='#001f00',
            #                   shuffle=False,
            #                   rotateRatio=0.5,
            #                   shrinkToFit=True,
            #                   shape='circle',
            #                   hover=True),
            # ], className="row box", ),
            html.Div(
                className="row box",
                children=[
                    html.Div(id='output-text'),
                ],
            ),
        ],
    ),
], )


@app.callback(
    Output('output-text', 'children'),
    Input('wordcloud-button', 'n_clicks'),
    State('text-input', 'value'),
    State('n-words-dropdown', 'value'),
    State("max-words-dropdown", 'value'),
)
def generate_word_cloud(n_clicks, text, n_words, max_words):
    #TODO: add error handling
    if n_clicks > 0:
        
        # image = utils.text_to_wordcloud(text, int(n_words), int(max_words))
        # return html.Img(src=image, style={'width': '100%'})
        # return str(utils.text_to_frequencies(text, int(n_words)))
        data = utils.get_holoniq_wordcloud_data(text, int(n_words), int(max_words))
        print(data)
        return DashWordcloud(id='wordcloud',
                              list=data,
                              width=900,
                              height=600,
                              gridSize=16,
                              color='#f0f0c0',
                              backgroundColor='#001f00',
                              shuffle=False,
                              rotateRatio=0.5,
                              shrinkToFit=True,
                              shape='circle',
                              hover=True,
                              drawOutOfBound=False,
                              weightFactor=16,
                              ),
    else:
        return html.H5(':) !')


# start the application
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)