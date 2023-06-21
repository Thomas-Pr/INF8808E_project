import dash
from dash import html, dcc, Input, Output

import radar_chart_def_pos
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
fig_defense_actions,fig_poss=radar_chart_def_pos.get_fig()

def add_graph(id, figure):
    graph = html.Div(dcc.Graph(
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
            ), style={'borderRadius': '8px', 'overflow': 'hidden'})
    return graph


image_url = "https://wallpapercave.com/wp/wp11803334.jpg"  # Replace with your desired image URL

app.layout = html.Div(
    style={
        'font-family': 'Arial',
        'color': '#333333',
        'backgroundColor': 'rgb(235, 59, 59)'
    },
    className='content',
    children=[
    html.Header(style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}, children=[
        html.H1("Morocco's Unexpected Triumph: A Deep Dive into the 2022 World Cup Journey", style={'font-size': '3em', 'marginBottom': '5px', 'font-weight': 'bold', 'color': 'red'}),
        html.Img(src=image_url, style={'height': '500px', 'marginLeft': '20px', 'borderRadius': '8px'}),
        html.P("In this analysis, we're using FIFA's data to highlight Morocco's surprising and exciting journey in the 2022 World Cup. Morocco wasn't seen as a top competitor at the beginning, but they fought their way into the final stages of this world-renowned tournament. Our goal is to show how Morocco's great performance wasn't just luck. We're looking at strategy, teamwork, and determination that helped them exceed everyone's expectations and make a lasting impact on soccer fans everywhere.", style={'font-size': '1.3em', 'marginBottom': '20px', 'marginLeft': '30px', 'text-align': 'center'})
    ]),
    html.Div(style={'padding': '0 30px',
        'backgroundColor': 'rgb(235, 59, 59)'}, children=[
        html.Div([
            html.H2('Breaking Down the Defense', style={'textAlign': 'center', 'fontSize': '2em', 'fontFamily': 'Verdana', 'color': 'white'}),
            html.P("Let's dive into how Morocco's defense stacked up. We're using a radar chart, which is a pretty cool tool that lets us visualize their overall performance. The bigger the area on the chart, the better the team did. We're looking at a bunch of different aspects of defense, like interceptions, tackles, and who won in aerial duels. We also highlighted the number of fouls committed, to get an idea of their discipline level.", style={'textAlign': 'center', 'fontSize': '1em', 'color': 'white'}),
            add_graph(id='radar-chart_defense', figure=fig_defense_actions),
        ], style={'marginBottom': '60px'}),
        html.Div([
            html.H2('The Art of Possession', style={'textAlign': 'center', 'fontSize': '2em', 'fontFamily': 'Verdana', 'color': 'white'}),
            html.P("Next up, let's check out how Morocco controlled the ball. We're using another radar chart here to give you an idea of their possession style and performance. We're comparing general ball possession and how effectively the team moved forward with it. We used a logarithmic scale to make the differences in percentages clearer. As before, Morocco's area is filled in, so you can easily see how they did compared to the other teams.", style={'textAlign': 'center', 'fontSize': '1em', 'color': 'white'}),
            add_graph(id='radar-chart_poss', figure=fig_poss),
        ], style={'marginBottom': '60px'}),
        html.Div([
            html.H2('Offense vs Defense', style={'textAlign': 'center', 'fontSize': '2em', 'fontFamily': 'Verdana', 'color': 'white'}),
            html.P("Offense vs Defense! We're using stacked bar charts to get a clear view of how players perform in both areas. On the defensive side, we're looking at tackles, blocks, and interceptions. On the offense, we're focusing on passes. As any fan knows, good passing is what sets up those spectacular goals. The stacked bar charts let us easily compare each player's performance, and see where their strengths lie.", style={'textAlign': 'center', 'fontSize': '1em', 'color': 'white'}),
            add_graph(id='barchart-offense', figure=fig_offense),
            add_graph(id='barchart-defense', figure=fig_defense),
        ], style={'marginBottom': '60px'}),
        html.Div([
            html.H2('Shots to Goals', style={'textAlign': 'center', 'fontSize': '2em', 'fontFamily': 'Verdana', 'color': 'white'}),
            html.P("Next up, we're going to dive into one of the most thrilling aspects of the game – turning shots into goals. For this, we're using a stacked bar chart, which will really help us to see the ratio of shots taken, shots on target, and goals scored. We're going to lay it all out there, so we can see how successful each team was in making those precious shots count.", style={'textAlign': 'center', 'fontSize': '1em', 'color': 'white'}),
            dcc.Dropdown(
                id="dropdown",
                options=[{"label": s, "value": s} for s in ["Overall", "Per Match"]],
                value="Overall",
                clearable=False,style={'width': '30%'}
            ),
            add_graph(id='barchart-shooting', figure=bar_chart_shooting.get_figure(df=bar_chart_shooting.mask_data(mask="Overall")[0], mask_title=bar_chart_shooting.mask_data(mask="Overall")[1])),
        ], style={'marginBottom': '60px'}),
        html.Div([
    html.H2('Player Performance Heatmap', style={'textAlign': 'center', 'fontSize': '2em', 'fontFamily': 'Verdana', 'color': 'white'}),
    html.P("We've cooked up a heatmap to give us a clear view of which players turned up the heat and who might've been left out in the cold. Our focus here is on their contribution to the offensive side of the game, and ultimately, the team's success. We're not just talking about goals and assists, but the impact they've had overall.", style={'textAlign': 'center', 'fontSize': '1em', 'color': 'white'}),
    html.Div(style={'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'flexDirection' : 'row'}, children=[
        html.Div(style={'width': '60%', 'padding': '10px'}, children=[
            add_graph(id='heatmap-performance', figure=heatmap.get_figure(heatmap.prep_data()))
        ]),
        html.Div(style={'width': '35%', 'padding': '10px'}, children=[
            html.Table(style={
                'marginTop': '20px', 
                'marginLeft': 'auto', 
                'marginRight': 'auto',
                'borderSpacing': '0',
                'width': '100%',
                'textAlign': 'center',
                'border': '1px solid white',
            }, children=[
                html.Thead(
                    style={'backgroundColor': '#4F7942', 'color': 'white'},
                    children=html.Tr(children=[
                        html.Th('Name', style={'padding': '10px'}),
                        html.Th('Description', style={'padding': '10px'})
                    ])
                ),
                html.Tbody(children=[
                    html.Tr(children=[
                        html.Td('G', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'}),
                        html.Td('Goals', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'})
                    ]),
                    html.Tr(children=[
                        html.Td('AG', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'}),
                        html.Td('Assisted Goals', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'})
                    ]),
                    html.Tr(children=[
                        html.Td('onG', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'}),
                        html.Td('Goals scored by team while on pitch', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'})
                    ]),
                    html.Tr(children=[
                        html.Td('onGA', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'}),
                        html.Td('Goals allowed by team while on pitch', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'})
                    ]),
                    html.Tr(children=[
                        html.Td('PlusMinus', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'}),
                        html.Td('Goals scored minus goals allowed while the player was on the pitch', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'})
                    ]),
                    html.Tr(children=[
                        html.Td('On-Off', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'}),
                        html.Td('Net goals by the team while the player was on the pitch minus net goals allowed by the team while the player was off the pitch', style={'padding': '10px', 'border': '1px solid white', 'color': 'white'})
                    ])
                ])
            ])
        ])
    

            ]),
        ], style={'marginBottom': '60px'}),
        html.Div([
            html.H2('Playing Time & Age Analysis', style={'textAlign': 'center', 'fontSize': '2em', 'fontFamily': 'Verdana', 'color': 'white'}),
            html.P("We're turning to the trusty violin plot to shed some light on two key factors: how much time each player spent on the pitch, and the age distribution within the squads. ", style={'textAlign': 'center', 'fontSize': '1em', 'color': 'white'}),
            add_graph(id='violin-min', figure=violin.draw_figure(df=violin.prep_data_violin(), column="Min")),
            add_graph(id='violin-age', figure=violin.draw_figure(df=violin.prep_data_violin(), column="Age")),
        ], style={'marginBottom': '60px'}),
    ]),
])
@app.callback(
    Output("barchart-shooting", "figure"), 
    Input("dropdown", "value"))
def update_bar_chart_shooting(mask):
    df, mask_title = bar_chart_shooting.mask_data(mask)
    fig = bar_chart_shooting.get_figure(df, mask_title)
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
