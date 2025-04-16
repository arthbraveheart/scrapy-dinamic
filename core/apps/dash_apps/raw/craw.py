from dash.dependencies import Input, Output, State
from ..components.figures import ReportCharts, progress_bar_state
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
        Output('modal', 'is_open'),
        [Input('crawler-button', 'n_clicks'), Input('close', 'n_clicks')],
        [State('modal', 'is_open')],
        prevent_initial_call=True,
    )
    def toggle_modal(crawler_clicks, close_clicks, is_open):
        ctx = callback_context
        if not ctx.triggered:
            return no_update

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'crawler-button':
            return True  # Open modal on crawler button click
        elif trigger_id == 'close':
            return False  # Close modal on close button click

        return is_open

    @app.callback(
        Output('modal-message', 'children'),
        Input('crawler-button', 'n_clicks'),
        [State('sellers_drop', 'value')],
        background=True,
        running=[
            # Disable button and show processing message during execution
            (Output("crawler-button", "disabled"), True, False),
            (Output("modal-message", "children"), "Processing...", no_update),
        ],
        prevent_initial_call=True,
    )
    def run_crawler_background(n_clicks, seller):
        if n_clicks and n_clicks > 0:
            return run_crawler(seller)
        return no_update

    @app.callback(
        output=Output("paragraph_id", "is_active"),
        inputs=Input("button_id", "n_clicks"),
        background=True,
        running=[
            (Output("crawler-button", "disabled"), True, False),
            (Output('modal', 'is_open'), True, False)
        ],
        progress=[
            Output("progress_bar", "value"),
            Output("progress_bar", "max")
        ],
        cancel=Input("cancel_button_id", "n_clicks"),
        prevent_initial_call=True
    )
    def update_progress(set_progress, _):
        total = 0
        just_a_list = []
        now = datetime.now()

        """
        for i in range(total + 1):
            just_a_list.append(i)
            set_progress((str(i), str(total)))
            time.sleep(0.01)"""

        return True

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