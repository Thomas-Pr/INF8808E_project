import plotly.express as px
import pandas as pd

def draw_figure(df, column):
    '''
        Draw a violin plot for a specific column in a dataframe

        Args:
            df: The dataframe to use for the figure
            column: The column used (Min or Age)
        Returns:
            figure based on the dataframe
    '''
    # Add a new column 'HoverInfo' for hover data in the plot
    df['HoverInfo'] = '<b>Player:</b> ' + df['Player'] + '<br>' + '<b>Age:</b> ' + df['Age'].astype(str) + '<br>' + '<b>MP:</b> ' + df['MP'].astype(str) + '<br>' + '<b>Mins:</b> ' + df['Min'].astype(str)
    
    # Create a violin plot with hover info and return the figure
    fig = px.violin(df, color="Squad", x="Squad", y=column, box=True, points="all",
                 title=f"Violin Plot - {column} per Squad", 
                 hover_data={"HoverInfo": "|%{customdata[0]}"})
    fig.update_traces(hovertemplate='<br>%{customdata[0]}<extra></extra>')
    fig.update_layout(height=600,
                      legend=dict(title='<span style="font-size: 18px"><b>Squad</b></span>',
                                  font_size=13)
    )
    return fig


def prep_data_violin():
    '''
        Prepare data for violin plot

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    # Load the csv data
    dataframe = pd.read_csv('./assets/data/StandardStats.csv')
    
    # Filter out needed columns
    dataframe = dataframe[["Squad","Player","Age","Min", "MP"]]
    
    # Return the processed dataframe
    return dataframe