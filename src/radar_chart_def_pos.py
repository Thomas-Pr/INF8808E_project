import plotly.graph_objects as go
import pandas as pd

# DATA LOADING AND PROCESSING

Playingtime=[7.7,7.7,7.3,7.3]

teams=['Argentina','Croatia','France','Morocco']
categories_def = ['Interceptions','AerialDuelswon' , 'Recoveries', 'Clearances','Fouls','Tackles']
categories_pos=['Possession (%)','Touches in defensive 1/3 (%)','Progressive Passes (%)','Progressive Carries (%)']
colors = {
    'Argentina': {'line': 'rgba(255,51,255,1)', 'marker': 'rgba(255,51,255,1.8)'},
    'Croatia': {'line': 'rgba(255, 0, 0, 1)', 'marker': 'rgba(255, 0, 0, 1.3)'},
    'France': {'line': 'rgba(86,180,245, 1)', 'marker': 'rgba(86,180,245, 1.3)'},
    'Morocco': {'line': 'rgba(34, 139, 34,0.5)', 'fillcolor': 'rgba(97,208,79, 0.5)', 'marker': 'rgba(34, 139, 34, 1.3)'}
}

def load_data():
    df_defense = pd.read_csv("assets/data/DefensiveActions.csv", sep=",")
    df_miscellaneous= pd.read_csv("assets/data/MiscellaneousStats.csv", sep=",")
    df_passing = pd.read_csv("assets/data/Passing.csv", sep=",")
    df_possession = pd.read_csv("assets/data/Possession.csv", sep=",")
    df_scorefixtures = pd.read_csv("assets/data/ScoresFixtures.csv", sep=",")
    return df_miscellaneous,df_defense,df_passing,df_possession,df_scorefixtures

def divide_playingtime(stat):
    stat_divide=[(x / y) for x, y in zip(stat, Playingtime)]
    stat_game=[round(val, 1) for val in stat_divide]
    return stat_game

def divide_total_100(count,tot):
    ratio=[(x / y)*100 for x, y in zip(count, tot)]
    ratio_approx=[round(val, 1) for val in ratio]
    return(ratio_approx)

def prep_data_defense(dfmisc,df_def):

    inter=df_def.groupby('Squad')['Int'].sum().to_list()
    tkl=df_def.groupby('Squad')['Tackles-Tkl'].sum().to_list()
    clr=df_def.groupby('Squad')['Clr'].sum().to_list()
    fouls=dfmisc.groupby('Squad')['Perf_Fls'].sum().to_list()

    defenders_data = dfmisc[dfmisc['Pos'] == 'DF']
    recoveries=defenders_data.groupby('Squad')['Perf_Recov'].sum().to_list()
    aerialsDuelswon=dfmisc.groupby('Squad')['AerialDuels_Won'].sum().to_list()

    int_game,tkl_game,clr_game,fouls_game,recov_game,aerial_game=divide_playingtime(inter),divide_playingtime(tkl),divide_playingtime(clr),divide_playingtime(fouls),divide_playingtime(recoveries),divide_playingtime(aerialsDuelswon)

    dict_country={}
    for i in range (len(teams)):
        country=teams[i]
        dict_country[country]=  [int_game[i],tkl_game[i],clr_game[i],fouls_game[i],recov_game[i],aerial_game[i]]
    
    return dict_country

def prep_data_possession(df_passing,df_possession,df_scorefixtures):
    
    ScoreFixtures_WC = df_scorefixtures.loc[df_scorefixtures['Comp'] == 'World Cup']
    possession_moy_calc = ScoreFixtures_WC.groupby('Squad')['Poss'].mean().to_list()
    possession_moy=[round(val, 1) for val in possession_moy_calc]
    
    Touches_def = df_possession.groupby('Squad')['Touches-Def 3rd'].sum().to_list()
    Touches_tot = df_possession.groupby('Squad')['Touches'].sum().to_list()
    def_touches = divide_total_100(Touches_def,Touches_tot)
    
    total_PrgD = df_passing.groupby('Squad')['Total-PrgDist'].sum().to_list()
    total_Dist_D = df_passing.groupby('Squad')['Total-TotDist'].sum().to_list()
    prog_dist_ratio = divide_total_100(total_PrgD,total_Dist_D)
    
    total_PrgC = df_possession.groupby('Squad')['Carries-PrgDist'].sum().to_list()
    Total_Dist_C = df_possession.groupby('Squad')['Carries-TotDist'].sum().to_list()
    progDist_ratio_carries = divide_total_100(total_PrgC,Total_Dist_C)

    dict_country={}
    for i in range (len(teams)):
        country=teams[i]
        dict_country[country]=  [possession_moy[i],def_touches[i],prog_dist_ratio[i],progDist_ratio_carries[i]]
    
    return dict_country


def get_radar_figure(team_data,categories):

    """
        Generate a radar chart for the given teams.

        Args:
            categories: List of categories for the radar chart
            category_definitions: Descriptions for each category
            team_data: Dictionary with team names as keys and corresponding data as values

        Returns:
            A plotly Figure with the radar chart
    """

    fig = go.Figure()
  
    hovertext = ['{}: {}'.format(cat, val) for cat, val in zip(categories, team_data["Morocco"])]
    hovertemplate = '<span color: white"><b>{}</b><br>{}: {}</span><extra></extra>'.format("Morocco", '%{theta}', '%{r}')

    trace_morocco = go.Scatterpolar(
        r=team_data['Morocco'] + [team_data['Morocco'][0]],
        theta=categories + [categories[0]],
        fill='toself',
        hoveron='points+fills',
        line=dict(
            shape='spline',
            width=3,
            color=colors['Morocco']['line']
        ),
        name='Morocco',
        marker=dict(color=colors['Morocco']['marker']),
        fillcolor=colors['Morocco']['fillcolor'],
        hovertemplate=hovertemplate,
    )

    fig.add_trace(trace_morocco)

    # Process the remaining teams
    for team_name in team_data.keys():
        if team_name == "Morocco":
            continue 

        hovertext = ['{}: {}'.format(cat, val) for cat, val in zip(categories, team_data[team_name])]
        hovertemplate = '<span color: white"><b>{}</b><br>{}: {}</span><extra></extra>'.format(team_name, '%{theta}', '%{r}')

        trace = go.Scatterpolar(
            r=team_data[team_name] + [team_data[team_name][0]],
            theta=categories + [categories[0]],
            fill='none',
            hoveron='points+fills',
            line=dict(
                shape='spline',
                width=3,
                color=colors[team_name]['line']
            ),
            name=team_name,
            marker=dict(color=colors[team_name]['marker']),
            hovertemplate=hovertemplate,
        )

        fig.add_trace(trace)

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True,linecolor='rgba(0,0,0,0.4)',gridcolor='rgba(0,0,0,0.1)')
        ),
        hovermode='closest',
    )

    fig.update_polars(bgcolor='rgba(0,0,0, 0.1)')

    
    fig.update_traces(hoveron="points")

    return fig

def get_fig():
    df_miscellanous,df_defense,df_passing,df_possession,df_scorefixtures=load_data()
    dict_country_defense= prep_data_defense(df_miscellanous,df_defense)
    dict_country_poss = prep_data_possession(df_passing,df_possession,df_scorefixtures)

    fig_def=get_radar_figure(dict_country_defense,categories_def)
    fig_def.add_annotation(
        x=0.5,
        y=1.23,
        xref='paper',
        text='Defensive actions by game',
        showarrow=False,
        font=dict(
            family='Arial',
            size=18,
            color='black'
        ),
    )
    fig_poss=get_radar_figure(dict_country_poss,categories_pos)
    fig_poss.add_annotation(
        x=0.5,
        y=1.23,
        xref='paper',
        text="Morocco's possession style compared to other teams",
        showarrow=False,
        font=dict(
            family='Arial',
            size=18,
            color='black'
        ),
    )
    fig_poss.update_layout(polar=dict(radialaxis=dict(type='log')))
    return fig_def,fig_poss