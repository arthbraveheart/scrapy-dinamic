import pandas as pd
import dash_ag_grid as dag
from sqlalchemy import create_engine, text
from django.conf import settings
from target.models import Core, DularEans
#from typing import List, Tuple, Optional
#import plotly.express as px
#import plotly.graph_objects as go
#from dash import dcc, html, dash_table
#import dash_bootstrap_components as dbc
#import re
#from django.db import connection
from django.db.models import Count, Case, When, IntegerField, Sum, F, Q
#from io import StringIO


engine = create_engine(settings.DB_URL)

class ReportCharts:

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def get_table_chart_data(self):

        columns = ('seller','name','price','ean','url')
        q_start = Q(date_now__gt=self.start_date)
        q_end = Q(date_now__lt=self.end_date)
        # Start with the base query
        data = Core.objects.filter(q_start & q_end).order_by('-date_now').values(*columns)

        return columns, data

    def table_chart_pbi(self):

        columns, table_data = self.get_table_chart_data()
        return dag.AgGrid(
            id="raw_table_data",
            rowData=list(table_data),
            columnDefs=[
            {
                "field": i,
                "autoHeight": True,
                "wrapText": True,
                "resizable": True,
                #"width": 500,
                "filter": True,
            } for i in columns[:-1]
            ] + [
                {
                    "headerName": "Link",
                    "field": "url",
                    # stockLink function is defined in the dashAgGridComponentFunctions.js in assets folder
                    "cellRenderer": "SellerLink",
                },
            ],
            csvExportParams={
                "fileName": "pricing_data.csv",
                "columnSeparator": ";",  # fiz the multiselect bug
            },
            columnSize="responsiveSizeToFit",
            dashGridOptions={'pagination': True},
        )


def progress_bar_state(seller, trigger_date):

    total_eans = DularEans.objects.all().distinct().count()
    enas_fetched = Core.objects.filter(seller=seller, date_now__gt=trigger_date).values('ean').distinct().count()



