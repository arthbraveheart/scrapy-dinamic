from dash.dependencies import Input, Output, State
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


    @app.callback(
        Output('output-container-date-picker-range', 'children'),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date')
    )
    def update_output(start_date, end_date):
        string_prefix = 'You have selected: '
        if start_date is not None:
            start_date_object = date.fromisoformat(start_date)
            start_date_string = start_date_object.strftime('%B %d, %Y')
            string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
        if end_date is not None:
            end_date_object = date.fromisoformat(end_date)
            end_date_string = end_date_object.strftime('%B %d, %Y')
            string_prefix = string_prefix + 'End Date: ' + end_date_string
        if len(string_prefix) == len('You have selected: '):
            return 'Select a date to see it displayed here'
        else:
            return string_prefix