from dash.dependencies import Input, Output, State
from app import db
from sqlalchemy.exc import SQLAlchemyError
from flask import session
import plotly.graph_objs as go


def register_callbacks(dashapp):
    @dashapp.callback([Output('table', 'columns'),
                       Output('table', 'data'),
                       Output('x-axis', 'options'),
                       Output('y-axis', 'options'),
                       Output('query_error', 'children'),
                       Output('query_error', 'style'),
                       Output('query_info', 'children'),
                       Output('query_info', 'style')],
                      [Input('btn-query', 'n_clicks')],
                      [State('sql-query', 'value')])
    def update_table(_, query):
        if query is not None:
            query = query.strip('\n ')
            if query != '':
                try:
                    q = db.session.execute(query)
                    data = [{f'{column}': value for column, value in row.items()} for row in q]
                    session['query_data'] = data
                    columns = [{'name': f'{column}', 'id': f'{column}'} for column in data[0]] if len(data) > 0 else \
                        [{'name': '', 'id': 'None'}]
                    select_options = [{'label': f'{column}', 'value': f'{column}'} for column in data[0]] \
                        if len(data) > 0 else []
                    info = 'Query returns no data!' if len(data) == 0 else ''
                    style = {} if len(data) == 0 else {'display': 'none'}
                    return columns, data, select_options, select_options, '', {'display': 'none'}, info, style
                except SQLAlchemyError as e:
                    return [{'name': '', 'id': 'None'}], [{}], [], [], str(e), {}, '', {'display': 'none'}
        return [{'name': '', 'id': 'None'}], [{}], [], [], '', {'display': 'none'}, '', {'display': 'none'}

    @dashapp.callback(Output('graph', 'figure'),
                      [Input('x-axis', 'value'),
                       Input('y-axis', 'value'),
                       Input('tabs', 'active_tab')])
    def update_plot(x_axis, y_axis, tab):
        if tab == 'scat-plot' or tab == 'line-plot':
            if any(select is None for select in [x_axis, y_axis]):
                return []
        else:
            if x_axis is None:
                return []
        data = session.get('query_data')
        if data is None:
            return []

        x_data = [row[x_axis] for row in data]

        if tab == 'scat-plot' or tab == 'line-plot':
            y_data = [row[y_axis] for row in data]
            if type(x_data[0]) == str and not x_data[0].startswith('2020'):
                x_data = [f'| {col} |' for col in x_data]
                figure_data = go.Bar(
                    x=x_data,
                    y=y_data
                )
            else:
                figure_data = go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers' if tab == 'scat-plot' else 'lines+markers'
                )

            figure_layout = go.Layout(
                xaxis={'title': x_axis},
                yaxis={'title': y_axis},
                margin={'l': 60, 'b': 40, 't': 10, 'r': 10}
            )

            return {'data': [figure_data], 'layout': figure_layout}

        elif tab == 'hist-plot':
            if type(x_data[0]) == str and not x_data[0].startswith('2020'):
                x_data = [f'| {col} |' for col in x_data]
            figure_data = go.Histogram(
                x=x_data
            )

            figure_layout = go.Layout(
                xaxis={'title': x_axis},
                yaxis={'title': y_axis},
                margin={'l': 60, 'b': 40, 't': 10, 'r': 10}
            )

            return {'data': [figure_data], 'layout': figure_layout}
        else:
            return {}
