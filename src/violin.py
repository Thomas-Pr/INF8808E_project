import plotly.express as px
import pandas as pd

def draw_figure(df, column):
    df['HoverInfo'] = '<b>Player:</b> ' + df['Player'] + '<br>' + '<b>Age:</b> ' + df['Age'].astype(str) + '<br>' + '<b>MP:</b> ' + df['MP'].astype(str) + '<br>' + '<b>Mins:</b> ' + df['Min'].astype(str)
    fig = px.violin(df, color="Squad", x="Squad", y=column, box=True, points="all",
                 title=f"Violin Plot - {column} per Squad", 
                 hover_data={"HoverInfo": "|%{customdata[0]}"})
    fig.update_traces(hovertemplate='<br>%{customdata[0]}<extra></extra>')
    return fig

def prep_data_violin():
    dataframe = pd.read_csv('./assets/data/StandardStats.csv')
    dataframe = dataframe[["Squad","Player","Age","Min", "MP"]]
    return dataframe
