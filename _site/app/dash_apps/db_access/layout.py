import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt


db_query_section = html.Div(
    [
        html.Br(),
        dbc.Row(dbc.Col(html.A('Back to home', href='/', className='btn btn-info btn-block'))),
        dbc.Row(dbc.Col(dbc.Label('Query the database', className='label-info'))),
        dbc.Textarea(id='sql-query', placeholder='SELECT * FROM receipt', className='mb-3'),
        dbc.Row(dbc.Col(dbc.Alert(id='query_error', style={'display': 'none'}, color="danger"))),
        dbc.Row(dbc.Col(dbc.Alert(id='query_info', style={'display': 'none'}, color="success"))),
        dbc.Button('Query', id='btn-query', color='primary', n_clicks=0),
        html.Hr()
    ]
)

table_query = dbc.Row(
    dbc.Col(
    [
        dt.DataTable(
            id='table',
            columns=[{'name': '', 'id': 'None'}],
            data=[{}],
            sort_action='native',
            filter_action='native',
            style_cell={'textAlign': 'center'}
        )
    ]),
    style={'overflowX': 'auto', 'maxHeight': 'calc(100% - 206)'}
)

dropdown_select_axes = html.Div(
    [
        dbc.Row(dbc.Col(dbc.Label('X-Axis', className='label-info'))),
        dbc.Select(id='x-axis', options=[]),
        dbc.Row(dbc.Col(dbc.Label('Y-Axis', className='label-info'))),
        dbc.Select(id='y-axis', options=[]),
        html.Hr()
    ]
)

plotting_tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                id='tabs',
                active_tab='scat-plot',
                card=True,
                children=[
                    # dbc.Tab(label='General Statistics', tab_id='gen-stat'),
                    dbc.Tab(label='Scatter Plot', tab_id='scat-plot'),
                    dbc.Tab(label='Line Plot', tab_id='line-plot'),
                    dbc.Tab(label='Histogram Plot', tab_id='hist-plot')
                ]
            ),
        ),
        dbc.CardBody(
            dcc.Graph(
                id='graph',
                figure={},
                style={
                    'width': '100%',
                    'height': '100%'
                }
            )
        )
    ],
    style={
        'width': '100%',
        'height': 'calc(100% - 205px)'
    }
)

layout = html.Div(
    [
        html.Div(
            [
                dbc.Col(
                    [db_query_section, table_query],
                    width=5,
                    style={'display': 'inline-block', 'height': '100%', 'verticalAlign': 'top', 'overflowY': 'auto'}
                ),
                dbc.Col(
                    [dropdown_select_axes, plotting_tabs],
                    width=7,
                    style={'display': 'inline-block',
                           'verticalAlign': 'top',
                           'height': '100%',
                           'borderLeft': '1px gray solid',
                           'overflowY': 'auto'}
                )
            ],
            style={'position': 'absolute', 'width': '100%', 'height': 'calc(100% - 0px)'}
        )
    ]
)