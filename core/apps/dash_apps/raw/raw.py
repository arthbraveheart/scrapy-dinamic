from dash import html, dcc, CeleryManager
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from .craw import register_raw_callbacks
from datetime import date
from core.celery import app as celery_app

background_callback_manager = CeleryManager(
    celery_app
)

app = DjangoDash('Raw',
                 external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
                 suppress_callback_exceptions=True,
                 background_callback_manager=background_callback_manager,
                 meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
                 )

# ======================
# Layout pieces
# ======================

## Graphs ##

ag_table_1 = html.Div(id='table')

drop_sellers = html.Div(id="drop_sellers", children=[
    #dropdown_options_pbi(users,users,"rpr_drop")
    dcc.Dropdown(
        id="sellers_drop",
        options=["Mercado Livre", "Carrefour", "Madeira Madeira", "testing"],
        #value=labels[0],
        placeholder="Escolha um Concorrente",
    )
])


modal = dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Your progress bar"),
                    close_button=False
                    # ^^ important, otherwise the user can close the modal
                    #    but the callback will be running still
                ),
                dbc.ModalBody(
                    html.Progress(
                        id="progress_bar",
                        value="0",
                        style={'width': '100%'}
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Cancel",
                        id="cancel_button_id",
                        className="ms-auto",
                        n_clicks=0
                    )
                )
            ],
            id="modal",
            is_open=False,
            backdrop="static",
            keyboard=False
            # ^^ important, otherwise the user can close the modal via the ESC button
            #    but the callback will be running still
        )



map_container = html.Div([
    html.Div(className="row row-cols-1 row-cols-sm-1 row-cols-lg-3", children=
        [
            html.Div(className="col p-2 mb-4", children=[
                drop_sellers,
            ])
        ]
        ),
    html.Button("Run!!", id="crawler-button", n_clicks=0, className="btn btn-dark-blue mb-0 toast-btn"),
    html.Button("Download CSV", id="csv-button", n_clicks=0, className="btn btn-dark-blue mb-0 toast-btn"),
    html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2023, 12, 1),
            max_date_allowed=date(2027, 12, 30),
            initial_visible_month=date.today(),
            start_date=date.today(),
            end_date=(date.today()).replace(day=(date.today()).day + 1),
            display_format='DD MMMM YYYY',
        ),
        html.Div(id='output-container-date-picker-range')
    ]),
    dcc.Loading(
        id="loading-table",
        type="dot",  # You can choose from "default", "circle", "dot", or "graph"
        children=[
            ag_table_1
        ]
    ),
   modal,
   dbc.Modal("Done!!", id="paragraph_id"),
]
)

app.layout = html.Div([
    map_container,
    dcc.Store(id='user-store', data=True),
    ])

register_raw_callbacks(app, manager=background_callback_manager)