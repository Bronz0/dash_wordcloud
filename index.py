from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
from dash_holoniq_wordcloud import DashWordcloud
import dash_daq as daq

from utils import utils

from components import navbar

from app import app

app = app
server = app.server


# application layout
app.layout = html.Div(
    children=[
        navbar.navbar,
        html.Div(
            className="column",
            id="content",
            children=[
                # Data input
                html.Div(
                    className="row box",
                    children=[
                        html.Div(
                            className="col-md-6",
                            children=[
                                dcc.Textarea(
                                    className="text-area",
                                    id="text-input",
                                    placeholder="Input text here...",
                                    value='',
                                ),
                            ],
                        ),
                        html.H2(
                            className="col-md-1",
                            children=["OR"],
                        ),
                        html.Div(
                            className="col-md-5",
                            children=[
                                dcc.Upload(
                                    id='upload-data',
                                    children=html.Div([
                                        'Drag and Drop or ',
                                        html.A('Select Files'),
                                    ]),
                                    style={
                                        'width': '98%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                    },
                                    # Allow multiple files to be uploaded
                                    multiple=True,
                                    contents=None,
                                    accept='.txt',
                                ),
                            ],
                        ),
                    ],
                ),

                # Contorl
                html.Div(
                    className="row box",
                    children=[
                        html.Div(
                            className='col-md-2',
                            children=[
                                html.H4('N words'),
                                dcc.Dropdown([1, 2, 3],
                                             1,
                                             id="n-words-dropdown",
                                             clearable=False),
                            ],
                        ),
                        html.Div(
                            className='col-md-2',
                            children=[
                                html.H4('Max words'),
                                dcc.Dropdown(
                                    [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                    30,
                                    id="max-words-dropdown",
                                    clearable=False),
                            ],
                        ),
                        html.Div(
                            className='col-md-2',
                            children=[
                                html.H4('Chart Type'),
                                dcc.Dropdown(["Static", "Interactive"],
                                             "Interactive",
                                             id="wordcloud-type",
                                             clearable=False),
                            ],
                        ),
                        html.Div(
                            className='col-md-2',
                            children=[
                                html.H4('Weight Factor'),
                                daq.NumericInput(
                                    id='weight-factor',
                                    value=16,
                                    min=1,
                                    max=100,
                                ),
                            ],
                        ),
                        html.Div(
                            className='col-md-2',
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

                # Results
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
    Output('loading-state', 'children'),
    Input('file-upload', 'loading_state'),
)
def update_loading_state(loading_state):
    print(type(loading_state), loading_state)
    return html.H6(loading_state)

@app.callback(
    Output('wordcloud', 'children'),
    Input('wordcloud-button', 'n_clicks'),
    State('text-input', 'value'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('n-words-dropdown', 'value'),
    State("max-words-dropdown", 'value'),
    State("wordcloud-type", 'value'),
    State('weight-factor', 'value'),
    State("upload-data", 'loading_state'),
)
def generate_word_cloud(n_clicks, text, files, file_name, n_words, max_words,
                        wordcloud_type, weight_factor, loading_state):
    if n_clicks > 0:
        if (text == '') & (files == None):
            return html.H5(
                "Please input text or upload a file!",
                style={
                    'color': 'red',
                    'text-align': 'center'
                },
            )
        if files != None:
            # TODO: get files contents
            # TODO: update uploaded file name
            print(file_name)
        if wordcloud_type == "Static":
            image = utils.text_to_wordcloud(text, int(n_words), int(max_words))
            wordcloud = html.Img(src=image, style={'width': '100%'})
            return wordcloud
        else:
            data = utils.get_holoniq_wordcloud_data(text, int(n_words),
                                                    int(max_words))
            holoniq_wordcloud = DashWordcloud(
                id='holoniq-wordcloud',
                list=data,
                width=1200,
                height=600,
                gridSize=16,
                # color='#f0f0c0',
                backgroundColor='#000000',
                shuffle=False,
                rotateRatio=0.5,
                shape='circle',
                hover=True,
                weightFactor=weight_factor,
                shrinkToFit=True,
            ),
            return holoniq_wordcloud
    else:
        return html.H6('Results will appear here...')


# start the application
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)