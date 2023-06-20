import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# DATA LOADING AND PROCESSING
def load_data():
    df_offense = pd.read_csv("./assets/data/Passing.csv", sep=",")
    df_defense = pd.read_csv("./assets/data/DefensiveActions.csv", sep=",")
    return df_offense, df_defense

def prep_offense_data(df):
    df_offense = df[df['Player'].isin(['Youssef EnNesyri', 'Sofiane Boufal','Azzedine Ounahi','Hakim Ziyech','Achraf Hakimi'])]
    df_offense = df_offense.rename(columns={"Short-Cmp": "Short Pass", "Medium-Cmp": "Medium Pass", "Long-Cmp": "Long Pass"})
    df_offense['Total'] = df_offense[["Short Pass", "Medium Pass", "Long Pass"]].sum(axis=1)
    df_offense = df_offense.sort_values('Total', ascending=False)
    df_offense.drop('Total', axis=1, inplace=True)
    return df_offense

def prep_defense_data(df):
    df_defense = df[df['Player'].isin(['Romain Saiss', 'Noussair Mazraoui', 'Nayef Aguerd', 'Achraf Hakimi', 'Sofyan Amrabat'])]
    df_defense = df_defense.rename(columns={"Tackles-Tkl": "Tackles", "Int": "Interceptions"})
    df_defense['Total'] = df_defense[["Tackles", "Blocks", "Interceptions"]].sum(axis=1)
    df_defense = df_defense.sort_values('Total', ascending=False)
    df_defense.drop('Total', axis=1, inplace=True)
    return df_defense

def prep_data_barchart_off_def():
    df_offense, df_defense = load_data()

    df_offense_prep = prep_offense_data(df_offense)
    df_defense_prep = prep_defense_data(df_defense)
    fig_offense = create_offense_plot(df_offense_prep)
    fig_defense = create_defense_plot(df_defense_prep)
    return fig_offense,fig_defense

def get_fig():
    df_offense, df_defense = load_data()

    df_offense_prep = prep_offense_data(df_offense)
    df_defense_prep = prep_defense_data(df_defense)
    fig_offense = create_offense_plot(df_offense_prep)
    fig_defense = create_defense_plot(df_defense_prep)
    return fig_offense,fig_defense

# FIGURES
def create_offense_plot(df):
    total_passes = df[["Short Pass", "Medium Pass", "Long Pass"]].sum(axis=1)
    percentages = df[["Short Pass", "Medium Pass", "Long Pass"]].div(total_passes, axis=0) * 100

    fig = go.Figure()

    for col, percent in zip(["Short Pass", "Medium Pass", "Long Pass"], percentages.columns):
        fig.add_trace(go.Bar(
            x=df["Player"],
            y=df[col],
            customdata=percentages[percent].round(1),
            hovertemplate="<b>Player :</b> %{x}<br><b>%{text} Completed:</b> %{y} (<b>%{customdata}%</b>)<extra></extra>",
            name=col,
            text=col
        ))

    fig.update_layout(
        title="Offensive Passes",
        legend_title_text='Pass Types',
        yaxis_title="Offensive Passes Completed",
        xaxis_title="Player"
    )

    return fig

def create_defense_plot(df):
    fig = px.bar(df, 
                 x="Player", 
                 y=["Tackles", "Blocks", "Interceptions"], 
                 labels={
                     "variable": "Defensive Actions",
                     "value": "Key Defensive Actions"
                 },
                 title="Defensive Actions")

    fig.update_traces(hovertemplate="<b>Player :</b> %{label}<br><b>%{variable} Completed:</b> %{value}<extra></extra>")
    fig.update_layout(legend_title_text='Defensive Actions')
    
    return fig
