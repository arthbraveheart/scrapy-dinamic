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

ag_table_1 = html.Div(id='table', className="row")

map_container = html.Div([
    html.Div([
        html.Button("Download CSV", id="csv-button", n_clicks=0, className="btn btn-primary mb-0 toast-btn g-col-2 p-2"),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2023, 12, 1),
            max_date_allowed=date(2027, 12, 30),
            initial_visible_month=date.today(),
            start_date=date.today(),
            end_date=(date.today()).replace(day=(date.today()).day + 1),
            display_format='DD MMMM YYYY',
            className="g-col-2"
        ),
    ], className="p-2 row grid"),
    dcc.Loading(
        id="loading-table",
        type="dot",  # You can choose from "default", "circle", "dot", or "graph"
        children=[
            ag_table_1
        ]
    ),
])

app.layout = html.Div([
    map_container,
    dcc.Store(id='user-store', data=True),
    ])

register_raw_callbacks(app, manager=background_callback_manager)