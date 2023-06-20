# -*- coding: utf-8 -*-

'''
    This file is the entry point for our dash app.
'''

import dash
from dash import html, dcc, Input, Output

import bar_chart_shooting
import violin
import bar_chart_off_def
import heatmap
import template


app = dash.Dash(__name__)
app.title = 'Project | INF8808E'
server = app.server


template.create_custom_theme()
template.set_default_theme()

fig_offense, fig_defense = bar_chart_off_def.get_fig()


def add_graph(id, figure):
    graph = dcc.Graph(
                id=id,
                className='graph',
                figure=figure,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False
                )
            )
    return graph



app.layout = html.Div(className='content', children=[
    html.Header(children=[
            html.H1('Morocco\'s historic journey during the 2022 World Cup'),
            html.H2('For this analysis, we used the FIFA\'s data. The purpose of this anlaysis is to understand how this country managed to reach the last square of the competition although it was not in the favorites of the competition.')
        ]),

    # VIZ Nabil
    html.Div([
        html.H3('Offense & Defense'),
        html.P('Some text.')
    ]),
    # html.Section(className='viz-container', children=[
    add_graph(id='offense', figure=fig_offense),
    add_graph(id='defense', figure=fig_defense),
    # ]),
        

    # VIZ Mohamed-Salah
    html.Div([
        html.H3('Shooting Efficiency'),
        html.P('Text.'),
    ]),
    # html.Section(className='viz-container', children=[
    dcc.Dropdown(
            id="dropdown",
            options=["Overall", "Per Match"],
            value="Overall",
            clearable=False,style={'width': '30%'}
        ),
    dcc.Graph(id="shooting"),
    # ]),


    # VIZ Thomas
    html.Div([
        html.H3('Offensive performance and impact on team success'),
        html.P('Per 90 minutes played, for the 10 non-goalkeeper players who played the most minutes, by descending order.'),
        html.P('The values correspond to the actual value minus the expected value.')
    ]),
    html.Section(className='viz-container', children=[
        
        add_graph(id='heatmap', figure=heatmap.get_figure(heatmap.prep_data())),

        html.Div(style={'width': '30%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'column'}, children=[
            html.H4('Description of the statistics', id='description'),
            html.Table(children=[
                html.Thead(html.Tr(children=[html.Th('Name'), html.Th('Description')])),
                html.Tbody(children=[
                    html.Tr(children=[html.Td('G'), html.Td('Goals')]),
                    html.Tr(children=[html.Td('AG'), html.Td('Assisted Goals')]),
                    html.Tr(children=[html.Td('onG'), html.Td('Goals scored by team while on pitch')]),
                    html.Tr(children=[html.Td('onGA'), html.Td('Goals allowed by team while on pitch')]),
                    html.Tr(children=[html.Td('PlusMinus'), html.Td('Goals scored minus goals allowed while the player was on the pitch')]),
                    html.Tr(children=[html.Td('On-Off'), html.Td('Net goals by the team while the player was on the pitch minus net goals allowed by the team while the player was off the pitch')])
                ])
            ])
        ])
    ]),


    # VIZ Yassine
    html.Div([
        html.H3('Violin plots'),
        html.P('An analysis of the dataset.')
    ]),
    # html.Section(className='viz-container', children=[
    dcc.Graph(
        className='graph',
        id='violin-plot-1'
    ),
    dcc.Graph(
        className='graph',
        id='violin-plot-2'
    )
    # ])
])


@app.callback(
    Output("shooting", "figure"), 
    Input("dropdown", "value"))
def update_bar_chart_shooting(mask):
    df = bar_chart_shooting.prep_data() 
    mask_title = "Efficiency in offensive actions during the competition" if mask == "Overall" else "Average efficiency in offensive actions per match"
    df = df[df["View"]==mask]
    fig = bar_chart_shooting.get_figure(df, mask_title)
    return fig

@app.callback(
    [Output('violin-plot-1', 'figure'), Output('violin-plot-2', 'figure')],
    [Input('violin-plot-1', 'clickData'), Input('violin-plot-2', 'clickData')]
)
def plots_updated(clickData1, clickData2):
    data = violin.prep_data_violin()
    fig1 = violin.draw_figure(data, "Min")
    fig2 = violin.draw_figure(data, "Age")
    return fig1, fig2
