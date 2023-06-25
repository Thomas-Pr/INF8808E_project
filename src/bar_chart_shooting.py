#import and data load
import plotly.express as px
import pandas as pd


# Preprocessing 
def prep_data():
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    df_init = pd.read_csv("./assets/data/Shooting.csv")
    df_all = clean_split_concat(df_init)
    return df_all


def clean_split_concat(df_init):
    '''
        Selects and preprocesses needed columns 
        Args :
            dataframe : dataframe to process
        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    #selects and renames needed columns
    df_init = df_init[["Squad","Gls", 'Sh', 'SoT']].rename(columns={"Gls":"Goals","SoT":"Shots on Target","Sh":"All Shots"}).groupby("Squad", as_index =False).sum()
    # creates the first dataframe for the first view
    dfa = df_init.copy()[["Squad"]]
    dfa["Missed Shots not on Target"] = df_init["All Shots"] - df_init["Goals"] - df_init["Shots on Target"]
    dfa["Missed Shots on Target"] = df_init["Shots on Target"] - df_init["Goals"]
    dfa["Goals"] = df_init["Goals"]
    # creates the first dataframe for the second view
    dfmatch = dfa.copy()
    dfmatch["Missed Shots not on Target"] = ((dfmatch["Missed Shots not on Target"])/7).round(0).astype(int)
    dfmatch["Missed Shots on Target"] = ((dfmatch["Missed Shots on Target"])/7).round(0).astype(int)
    dfmatch["Goals"] = ((df_init["Goals"])/7).round(0).astype(int)

    # Adapts the dataframes in order to have the wanted format and creates column Percent and View
    dfar = pd.melt(dfa, id_vars=['Squad'], var_name=['Shots']).sort_values(by = ["value"], ascending=True).copy()
    dfar["Percent"] =  ((dfar["value"] / dfar['value'].groupby(dfar['Squad']).transform('sum'))*10000).astype(int) /100
    dfar["View"] = "Overall"
    dfar2 =pd.melt(dfmatch, id_vars=['Squad'], var_name=['Shots']).sort_values(by = ["value",'Squad'], ascending=[True,False]).copy()
    dfar2["Percent"] =  ((dfar2["value"] / dfar2['value'].groupby(dfar2['Squad']).transform('sum'))*10000).astype(int) /100
    dfar2["View"] = "Per Match"
    #concat the dataframes
    df_all = pd.concat([dfar,dfar2])
    return df_all


#Figure
def mask_data(mask):
    '''
        Selects only the rows of the chosen view and its title
        Args :
            mask : string representing the chosen view 
        Returns:
            A pandas dataframe with the rows corresponding to the view.
            The title of the figure
    '''
    df = prep_data() 
    mask_title = "Efficiency in offensive actions during the competition" if mask == "Overall" else "Average efficiency in offensive actions per match"
    df = df[df["View"]==mask]
    return df, mask_title

def get_figure(df, mask_title):
    '''
        Generates a figure based on a dataframe and its title.
        Args :
            dataframe : dataframe to use for the figure
            mask_title : title of the figure
        Returns:
            figure based on the dataframe
    '''
    fig = px.bar(data_frame=df, x="Squad", y="value", color='Shots',
                 color_discrete_map={"Missed Shots on Target":"#dbd822" ,"Missed Shots not on Target":'rgb(235, 59, 59)',"Goals":'#4F7942'},
                 title=mask_title, 
                 hover_data = ["Percent","Shots"],
                 labels={'Shots':'Type of Shots','value':'nb of Shots','Percent':"% of Shots over All Shots"},
                 text_auto=True)
    fig.update_traces(hovertemplate="<b>Squad:</b> %{label}<br><b>Type of Shots:</b> %{customdata[1]}<br><b>Nb of Shots:</b> %{value}<br><b>% of Shots over All Shots:</b> %{customdata[0]}%<extra></extra>") 
    fig.update_layout(yaxis={'title': 'Number of shots'})
    fig.update_layout(height=600)
    return fig
