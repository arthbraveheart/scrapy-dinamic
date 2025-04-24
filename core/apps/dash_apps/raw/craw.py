from dash.dependencies import Input, Output, State, ClientsideFunction
from ..components.figures import ReportCharts
from datetime import datetime, date
from dash import callback_context, no_update

def register_raw_callbacks(app, manager):

    @app.callback(
        [Output('table', 'children'),
         ],
        [Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date')]
    )
    def update_table(start_date,end_date):
        chart_data = ReportCharts(start_date=start_date, end_date=end_date)
        table = chart_data.table_chart_pbi()
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