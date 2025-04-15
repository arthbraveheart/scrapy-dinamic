from dash.dependencies import Input, Output, State
from ..components.figures import ReportCharts
from ..components.triggers import run_crawler
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

    @app.callback(
        [
            Output('modal', 'is_open'),
            Output('modal-message', 'children'),
        ],
        [
            Input('crawler-button', 'n_clicks'),
            Input('close', 'n_clicks'),  # Add close button as input
        ],
        [
            State('sellers_drop', 'value'),
            State('modal', 'is_open'),
        ],
        prevent_initial_call=True,
        background=True,
        running=[
            # Disable crawler button & keep modal open during execution
            (Output("crawler-button", "disabled"), True, False),
            (Output("modal", "is_open"), True, False),
            (Output("modal-message", "children"), "Processing...", ""),
        ],
    )
    def update_prices(crawler_clicks, close_clicks, seller, is_open):
        ctx = callback_context
        if not ctx.triggered:
            return [is_open, ""]

        # Identify which component triggered the callback
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "close":
            # Close modal immediately
            return [False, no_update]

        elif trigger_id == "crawler-button":
            # Run crawler in background
            message = run_crawler(seller)
            return [True, message]  # Keep modal open with final message

        return [is_open, ""]

    @app.callback(
        Output('output-container-date-picker-range', 'children'),
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'))
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