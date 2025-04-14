import pandas as pd
import dash_ag_grid as dag
from sqlalchemy import create_engine, text
from django.conf import settings
from target.models import Core
#from typing import List, Tuple, Optional
#import plotly.express as px
#import plotly.graph_objects as go
#from dash import dcc, html, dash_table
#import dash_bootstrap_components as dbc
#import re
#from django.db import connection
#from django.db.models import Count, Case, When, IntegerField, Sum, F, Q
#from io import StringIO


engine = create_engine(settings.DB_URL)

class ReportCharts:

    def get_table_chart_data(self):

        columns = ('seller','name','price','ean',)
        # Start with the base query
        data = Core.objects.all().values(*columns)

        return columns, data

    def table_chart_pbi(self):

        columns, table_data = self.get_table_chart_data()
        return dag.AgGrid(
            id="raw_table_data",
            rowData=list(table_data),
            columnDefs=[{
                "field": i,
                "autoHeight": True,
                "wrapText": True,
                "resizable": True,
                #"width": 500,
                "filter": True,
                         } for i in columns],
            csvExportParams={
                "fileName": "pricing_data.csv",
                "columnSeparator": ";",  # fiz the multiselect bug
            },
            columnSize="responsiveSizeToFit",
            dashGridOptions={'pagination': True},
        )
