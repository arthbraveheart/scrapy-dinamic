from dash import html, dcc
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from .craw import register_map_callbacks

app = DjangoDash('Raw',
                 external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
                 suppress_callback_exceptions=True,
                 meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
                 )

# ======================
# Layout pieces
# ======================

## Graphs ##

ag_table_1 = html.Div(id='table')

map_container = dcc.Loading(
    id="loading-table",
    type="dot",  # You can choose from "default", "circle", "dot", or "graph"
    children=[
        ag_table_1
    ]
)

app.layout = html.Div([
    map_container,
    dcc.Store(id='user-store', data=True),
    ])

register_map_callbacks(app)