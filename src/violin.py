import plotly.express as px
import pandas as pd

def draw_figure(df, column):
    df['HoverInfo'] = 'Player name: ' + df['Player'] + '<br>' + 'Age: ' + df['Age'].astype(str) + '<br>' + 'MP: ' + df['MP'].astype(str) + '<br>' + 'Mins: ' + df['Min'].astype(str)
    fig = px.violin(df, color="Squad", x="Squad", y=column, box=True, points="all",
                 title=f"Violin Plot - {column} per Squad", 
                 hover_name="HoverInfo")
    return fig

def prep_data_violin():
    dataframe = pd.read_csv('./assets/data/StandardStats.csv')
    dataframe = dataframe[["Squad","Player","Age","Min", "MP"]]
    return dataframe
