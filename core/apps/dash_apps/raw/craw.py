from dash.dependencies import Input, Output
from ..components.figures import ReportCharts

def register_map_callbacks(app):
    @app.callback(
        [Output('table', 'children'),
         ],
        [Input('user-store', 'data')]
    )
    def update_map(user_data, user):

        chart_data = ReportCharts()

        table = chart_data.table_chart_pbi()
        #user = None if user.is_manager else str(user)

        return [table]