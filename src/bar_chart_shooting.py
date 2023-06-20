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
  df_init = df_init[["Squad","Gls", 'Sh', 'SoT']].rename(columns={"Gls":"Goals","SoT":"Shots on Target","Sh":"All Shots"}).groupby("Squad", as_index =False).sum()
  dfa = df_init.copy()[["Squad"]]
  dfa["Missed Shots not on Target"] = df_init["All Shots"] - df_init["Goals"] - df_init["Shots on Target"]
  dfa["Missed Shots on Target"] = df_init["Shots on Target"] - df_init["Goals"]
  dfa["Goals"] = df_init["Goals"]

  dfmatch = dfa.copy()
  dfmatch["Missed Shots not on Target"] = ((dfmatch["Missed Shots not on Target"])/7).round(0).astype(int)
  dfmatch["Missed Shots on Target"] = ((dfmatch["Missed Shots on Target"])/7).round(0).astype(int)
  dfmatch["Goals"] = ((df_init["Goals"])/7).round(0).astype(int)

  dfar = pd.melt(dfa, id_vars=['Squad'], var_name=['Shots']).sort_values(by = ["value"], ascending=True).copy()
  dfar["Percent"] =  ((dfar["value"] / dfar['value'].groupby(dfar['Squad']).transform('sum'))*10000).astype(int) /100
  dfar["View"] = "Overall"
  dfar2 =pd.melt(dfmatch, id_vars=['Squad'], var_name=['Shots']).sort_values(by = ["value",'Squad'], ascending=[True,False]).copy()
  dfar2["Percent"] =  ((dfar2["value"] / dfar2['value'].groupby(dfar2['Squad']).transform('sum'))*10000).astype(int) /100
  dfar2["View"] = "Per Match"
  df_all = pd.concat([dfar,dfar2])
  return df_all


#Figure
def get_figure(df,mask_title):
    fig = px.bar(data_frame = df, x="Squad", y="value",color='Shots',
                    color_discrete_map= {"Missed Shots on Target":"gold" ,"Missed Shots not on Target":"tomato","Goals":"limegreen"},
                    title=mask_title, 
                    hover_data = ["Percent","Shots"],
                    labels={'Shots':'Type of Shots','value':'nb of Shots','Percent':"% of Shots over All Shots"},
                    text_auto=True)
    fig.update_traces(hovertemplate = "<b>Squad :</b> %{label}<br><b>Type of Shots :</b> %{customdata[1]}<br><b>Nb of Shots :</b> %{value}<br><b>% of Shots over All Shots :</b> %{customdata[0]}%<extra></extra>") 
    fig.update_layout(yaxis={'title': 'Number of shots'})
    fig.update_layout(height=600)
    return fig
