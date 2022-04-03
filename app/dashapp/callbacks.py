from datetime import datetime as dt
import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output


def register_callbacks(app, dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        print("Reading user inside Dashapp:", dashapp.get_current_user())
        df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
        return {
            'data': [{
                'x': df.index,
                'y': df.Close
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }
    # for i in range(8):
    #     if getattr(app,'router').__dict__['routes'][i].__dict__['path'] == '/user':
    #         func = getattr(app,'router').__dict__['routes'][i].__dict__['endpoint']
    #         print(func())
    #         print(type(func))
    #         print('')
