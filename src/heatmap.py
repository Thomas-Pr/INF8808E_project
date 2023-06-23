'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import pandas as pd
import numpy as np

import template

# Define the statistics used in the heatmap
stats = ["G", "AG", "onG", "onGA", "PlusMinus", "OnOff"]

'''
    Functions to preprocess the data used in the visualisation.
'''

def filter_columns(dataframe):
    '''
        Selects and renames only the useful columns for the visualization.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with standardized names.
    '''
    # Select only part of the columns
    selected_keys = ["Squad", "Player", "Pos", "Min", "MP",
                    "Gls", "Ast", 
                    "xG", "xAG",
                    "TeamSuccess-onG", "TeamSuccess-onGA", "TeamSuccess-PlusMinus/90", "TeamSuccess-OnOff", 
                    "TeamSuccess(xG)-onxG", "TeamSuccess(xG)-onxGA", "TeamSuccess(xG)-PlusMinus/90", "TeamSuccess(xG)-OnOff"
                    ]
    dataframe = dataframe[selected_keys]
    # One missing value will be replaced by 0
    dataframe = dataframe.fillna(0)
    # Rename some of the columns for better visibility
    new_columns = {"TeamSuccess-onG":"actual_onG",
                    "TeamSuccess-onGA":"actual_onGA",
                    "TeamSuccess-PlusMinus/90":"actual_PlusMinus",
                    "TeamSuccess-OnOff":"actual_OnOff",
                    "TeamSuccess(xG)-onxG":"expected_onG", 
                    "TeamSuccess(xG)-onxGA":"expected_onGA",
                    "TeamSuccess(xG)-PlusMinus/90":"expected_PlusMinus", 
                    "TeamSuccess(xG)-OnOff":"expected_OnOff",
                    "Gls":"actual_G",
                    "Ast":"actual_AG",
                    "xG":"expected_G",
                    "xAG":"expected_AG"
                    }
    dataframe.rename(columns=new_columns, inplace=True)
    # Detail the positions for the hover tooltip
    dataframe = dataframe.replace("DF", "Defender")
    dataframe = dataframe.replace("MF", "Midfielder")
    dataframe = dataframe.replace("FW", "Forward")
    return dataframe


def filter_players(dataframe):
    '''
        Filters the elements of the dataframe by squad, position, and minutes, 
        to keep only the 10 non-goalkeeper players with the most playing time 
        in the Moroccan national team.

        Args:
            dataframe: The dataframe to process
        Returns:
            The dataframe filtered by squad, position, and minutes played.
    '''
    # Filter for only Morocco
    dataframe = dataframe.loc[dataframe["Squad"] == "Morocco"]
    # Remove the goalkeepers
    dataframe = dataframe.loc[dataframe["Pos"] != "GK"]
    # Keep the 10 players who played most minutes
    dataframe = dataframe.sort_values(by=["Min"], ascending=False).head(10)
    dataframe = dataframe.set_index(["Player"])
    return dataframe


def add_minus_exp(dataframe):
    '''
        Standardize the statistics which are not already per 90 minutes played,
        and adds the actual minus expected values to the data.

        Args:
            dataframe: The dataframe to process
            stats: The statistics used in the display
        Returns:
            The processed dataframe with columns named for the statistics,
            which correspond to the difference between the actual and expected values,
            except for the "onGA" statistic which needs to be the opposite 
            to respect the color signification.
    '''
    for stat_name in stats:
        # Normalize all the variables per 90 minutes played if not done already
        if stat_name not in ["PlusMinus", "OnOff"]:
            dataframe[f"actual_{stat_name}"] = dataframe[f"actual_{stat_name}"] / dataframe["MP"]
            dataframe[f"expected_{stat_name}"] = dataframe[f"expected_{stat_name}"] / dataframe["MP"]
        # Create the actual minus expected columns for the selected variables
        dataframe = dataframe.round(decimals=2)
        dataframe[stat_name] = dataframe[f"actual_{stat_name}"] - dataframe[f"expected_{stat_name}"]
        # Take the opposite for onGA to respect the color code from negative to positive
        if stat_name == "onGA":
            dataframe[stat_name] = - dataframe[stat_name]
    # Round the raw data to two decimals to display the values more clearly
    dataframe = dataframe.round(decimals=2)
    return dataframe


def prep_data():
    '''
    Applies all the data preprocessing.

    Returns:
        The processed dataframe with standardized names and desired statistics.
    '''
    dataframe_pt = pd.read_csv('./assets/data/PlayingTime.csv')
    dataframe_ss = pd.read_csv('./assets/data/StandardStats.csv')
    dataframe = pd.merge(dataframe_pt, dataframe_ss, on=['Squad', 'Player', 'Pos', 'Age', 'MP', 'Min', '90s'], how='outer')

    dataframe = filter_columns(dataframe)
    dataframe = filter_players(dataframe)
    dataframe = add_minus_exp(dataframe)
    
    return dataframe


'''
   Functions related to the creation of the heatmap.
'''

def get_display_data(dataframe):
    # Get only the raw statistics columns from the dataframe
    raw_data = dataframe[stats]
    # Change onGA name because its opposite is displayed to respect the color code from negative to positive
    raw_data = raw_data.rename(columns={"onGA": "-onGA"})

    # Create the hover data to display the position, actual value, and expected value
    df_pos = pd.concat([dataframe["Pos"]] * len(raw_data.columns), axis=1)
    df_actual = dataframe[[key for key in dataframe.keys() if (key not in list(raw_data.keys()) + ["Squad", "Min", "MP", "Pos"] and "actual" in key)]]
    df_expected = dataframe[[key for key in dataframe.keys() if (key not in list(raw_data.keys()) + ["Squad", "Min", "MP", "Pos"] and "expected" in key)]]

    hoverdata = np.stack([df_pos, df_actual, df_expected], axis=-1)

    # Normalize each column between -1 and 1
    norm_data = raw_data.copy()
    for stat_name in raw_data.keys():
        norm_data[stat_name] = raw_data[stat_name] / raw_data[stat_name].abs().max()
    
    return hoverdata, raw_data, norm_data


def get_heatmap_hover_template(customdata):
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon: position, actual value and
        expected value.
    '''
    hover_temp = "<b>Position:</b> %{customdata[0]}<br>"
    hover_temp += "<b>Actual value:</b> %{customdata[1]}<br>"
    hover_temp += "<b>Expected value:</b> %{customdata[2]}<br>"
    hover_temp += '<extra></extra>'
    return hover_temp


def get_figure(dataframe):
    '''
        Generates the heatmap from the given dataset.

        Args:
            dataframe: The full data with additional hover information
            raw_data: The data to display
            norm_data: The data to set the color values
        Returns:
            The figure to be displayed.
    '''
    hoverdata, raw_data, norm_data = get_display_data(dataframe)

    # Create the heatmap
    fig = px.imshow(img=norm_data,
                    x=norm_data.keys(), # columns also works
                    y=norm_data.index,
                    color_continuous_midpoint=0,
                    title = "Actual minus expected value per 90 minutes played",
                    aspect="auto"
                    )
        
    fig.update_layout(
                      yaxis_title="Player",
                      dragmode=False,
                    #   coloraxis_colorbar_title_text="Impact",
                    #   coloraxis_colorbar_tickmode="array",
                    #   coloraxis_colorbar_ticktext=["Min", "Max"],
                      coloraxis_showscale=False,
                      xaxis_side="top",
                      yaxis_autorange="reversed",
                      colorscale_sequential='RdBu'
                      )
    
    # Include the hover template and change displayed text to raw values (not normalized)
    fig.update_traces(hovertemplate=get_heatmap_hover_template(hoverdata),
                      customdata=hoverdata,
                      text=raw_data, texttemplate="%{text}"
                      )
    
    return fig
