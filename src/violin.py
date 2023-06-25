import plotly.express as px
import pandas as pd

# Function to draw a violin plot for a specific column in a dataframe
def draw_figure(df, column):
    # Add a new column 'HoverInfo' for hover data in the plot
    df['HoverInfo'] = '<b>Player:</b> ' + df['Player'] + '<br>' + '<b>Age:</b> ' + df['Age'].astype(str) + '<br>' + '<b>MP:</b> ' + df['MP'].astype(str) + '<br>' + '<b>Mins:</b> ' + df['Min'].astype(str)
    
    # Create a violin plot with hover info and return the figure
    fig = px.violin(df, color="Squad", x="Squad", y=column, box=True, points="all",
                 title=f"Violin Plot - {column} per Squad", 
                 hover_data={"HoverInfo": "|%{customdata[0]}"})
    fig.update_traces(hovertemplate='<br>%{customdata[0]}<extra></extra>')
    return fig

# Function to prepare data for violin plot
def prep_data_violin():
    # Load the csv data
    dataframe = pd.read_csv('./assets/data/StandardStats.csv')
    
    # Filter out needed columns
    dataframe = dataframe[["Squad","Player","Age","Min", "MP"]]
    
    # Return the processed dataframe
    return dataframe