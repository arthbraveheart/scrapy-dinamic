from dash.dependencies import Input, Output, State
from ..components.figures import ReportCharts

def register_raw_callbacks(app):
    @app.callback(
        [Output('table', 'children'),
         ],
        [Input('user-store', 'data')]
    )
    def update_table(user_data, user):

        chart_data = ReportCharts()

        table = chart_data.table_chart_pbi()
        #user = None if user.is_manager else str(user)

        return [table]

    @app.callback(
        Output("raw_table_data", "exportDataAsCsv"),
        Input("csv-button", "n_clicks"),
        State("csv-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def export_data_as_csv(n_clicks, current_n_clicks):
        if n_clicks and n_clicks > current_n_clicks:
            return False
        return True