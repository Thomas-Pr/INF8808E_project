import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def load_data():
    '''
        Imports the data from two .csv files.

        Returns:
            Two pandas dataframe containing the offensive and defensive data.
    '''
    df_offense = pd.read_csv("./assets/data/Passing.csv", sep=",")
    df_defense = pd.read_csv("./assets/data/DefensiveActions.csv", sep=",")
    return df_offense, df_defense


def prep_offense_data(df):
    '''
        Processes the offense data.

        Args:
            df: dataframe to process
        Returns:
            A prepared pandas dataframe containing the offensive data.
    '''
    df_offense = df[df['Player'].isin(['Youssef EnNesyri', 'Sofiane Boufal','Azzedine Ounahi','Hakim Ziyech','Achraf Hakimi'])]
    df_offense = df_offense.rename(columns={"Short-Cmp": "Short Pass", "Medium-Cmp": "Medium Pass", "Long-Cmp": "Long Pass"})
    df_offense['Total'] = df_offense[["Short Pass", "Medium Pass", "Long Pass"]].sum(axis=1)
    df_offense = df_offense.sort_values('Total', ascending=False)
    df_offense.drop('Total', axis=1, inplace=True)
    df_off = pd.melt(df_offense[["Player","Short Pass", "Medium Pass", "Long Pass"]], id_vars=['Player'], var_name=['Pass Types']).copy()
    df_off["percentages"] = ((df_off["value"] / df_off['value'].groupby(df_off['Player']).transform('sum'))*10000).astype(int) /100
    return df_off


def prep_defense_data(df):
    '''
        Processes the defense data.

        Args:
            df: dataframe to process
        Returns:
            A prepared pandas dataframe containing the offensive data.
    '''
    df_defense = df[df['Player'].isin(['Romain Saiss', 'Noussair Mazraoui', 'Nayef Aguerd', 'Achraf Hakimi', 'Sofyan Amrabat'])]
    df_defense = df_defense.rename(columns={"Tackles-Tkl": "Tackles", "Int": "Interceptions"})
    df_defense['Total'] = df_defense[["Tackles", "Blocks", "Interceptions"]].sum(axis=1)
    df_defense = df_defense.sort_values('Total', ascending=False)
    df_defense.drop('Total', axis=1, inplace=True)
    df_def = pd.melt(df_defense[["Player","Tackles", "Blocks", "Interceptions"]], id_vars=['Player'], var_name=['Defensive Actions']).copy()
    df_def["percentages"] = ((df_def["value"] / df_def['value'].groupby(df_def['Player']).transform('sum'))*10000).astype(int) /100
    return df_def


def create_offense_plot(df):
    '''
        Generates the barchart from the given offense data.

        Args:
            df: offense dataframe
        Returns:
            The offense figure to be displayed.
    '''
    fig = go.Figure()
    fig = px.bar(data_frame=df, x="Player", y="value", color="Pass Types",
                title="Offensive Passes", 
                hover_data=["percentages","Pass Types"],
                text_auto=True)
    fig.update_traces(hovertemplate="<b>Player:</b> %{x}<br><b>%{customdata[1]} Completed: </b>%{y} (%{customdata[0]}%)<extra></extra>") 
    fig.update_layout(yaxis={'title': "Offensive Passes Completed"},
                      height=600,
                      legend=dict(title='<span style="font-size: 18px"><b>Pass Types</b></span>',
                                  font_size=13)
    )
    return fig


def create_defense_plot(df):
    '''
        Generates the barchart from the given offense data.

        Args:
            df: offense dataframe
        Returns:
            The defense figure to be displayed.
    '''
    fig = px.bar(data_frame=df, x="Player", y="value", color="Defensive Actions",
                title="Key Defensive Actions", 
                hover_data=["percentages","Defensive Actions"],
                text_auto=True)
    fig.update_traces(hovertemplate="<b>Player:</b> %{x}<br><b>%{customdata[1]} Completed: </b>%{y} (%{customdata[0]}%)<extra></extra>") 
    fig.update_layout(yaxis={'title': "Defensive Actions"},
                      height=660,
                      legend=dict(title='<span style="font-size: 18px"><b>Defensive Actions</b></span>',
                                  font_size=13)
    )    
    return fig


def get_fig():
    '''
        Prepares the data and gets the figures for offense and defense bar charts.

        Returns:
            The offense and defense figures to be displayed.
    '''
    df_offense, df_defense = load_data()

    df_offense_prep = prep_offense_data(df_offense)
    df_defense_prep = prep_defense_data(df_defense)
    fig_offense = create_offense_plot(df_offense_prep)
    fig_defense = create_defense_plot(df_defense_prep)
    return fig_offense, fig_defense