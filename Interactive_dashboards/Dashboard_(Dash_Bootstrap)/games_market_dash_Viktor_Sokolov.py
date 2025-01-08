import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from numpy import random 
import plotly.express as px
from dash.dependencies import Input, Output

# Preparing the data 
df = pd.read_csv("games.csv")

"""
The code snippet below is doing the following:
1. Deleting missing values
2. Correcting data types and replacing some values
3. Filtering the data
4.Extracting some values into lists for the use in the App
"""
# delete rows with at least one missing value
df.dropna(inplace = True)
# ensuring that the data types are interpreted correctly
df[["Year_of_Release", "Critic_Score"]] = df[["Year_of_Release", "Critic_Score"]].astype("int") # replacing tbd (to be determined) User_Score with 0s
df["User_Score"].replace("tbd","-1", inplace = True) # to be determined (tbd) user scores replaced to drop them when plotting Scatter plot
df[["User_Score"]] = df[["User_Score"]].astype("float")
df[["Name", "Platform", "Genre", "Rating"]] = df[["Name", "Platform", "Genre", "Rating"]].astype("str")
# droping games that were released earlier 2000 year
df = df[df["Year_of_Release"]>=2000]
df.reset_index(drop=True, inplace=True)
df.drop_duplicates(inplace = True) # drop duplicate rows
# extracting values
genres_list = df["Genre"].unique()
dic_genres = [{"label":x,"value":x} for x in genres_list]
rating_list = df["Rating"].unique()
dic_rating = [{"label":x,"value":x} for x in rating_list]
min_year = df["Year_of_Release"].min()
max_year = df["Year_of_Release"].max()


# CSS formatting
corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}
corporate_font_family = "Dosis"

# Building the layout of the App
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.Row([ # Header row
        dbc.Col(html.H1("Review of Game Industry", style={"textAlign":"center", 'padding-top' : '1%', 'color':corporate_colors['white']}), width = 8),
    ], justify= "center", style={'background-color' : corporate_colors['superdark-green']}
    ), # Header row
    dbc.Row([ # Description row
        dbc.Col(html.H4("Gives information on the number of game releases per year for different platforms and correlation between User Score and Critic Score of the game", style={"textAlign":"center", 'color':corporate_colors['white']}),width = 8),
    ], justify="center", style = {'background-color' : "transparent"}
    ), # Description row

    
    # Empty row
    dbc.Row([], style={"height": "10px","background-color" : corporate_colors['light-green']}),
     
    dbc.Row( # Filters row
        [
            dbc.Col(dbc.FormGroup(
            [
                dbc.Label("Filters by Genres: "),
                dcc.Dropdown(
                    id="genres",
                    options= dic_genres,
                    value= random.choice(genres_list,1), multi =True)
                    
            ]), width = 4),
            dbc.Col(dbc.FormGroup(
            [
                dbc.Label("Filters by Ratings: "),
                dcc.Dropdown(
                    id="rating",
                    options=dic_rating,
                    value= random.choice(rating_list,1), multi = True)
            ]), width = 4),
            
    ], justify="center", style = {"background-color" : corporate_colors['light-green']}
    ), # Filters row
           

    dbc.Row([ # Searching results row
            dbc.Col(html.H4("Number of Games Found: ", style={"padding-left":"245px"}), width = "auto", style ={"position":"relative", "right":"225px" }),
            dbc.Col(html.H3( id = "input1", style={"textAlign":"center","color":"white", 'border-radius' : '3px', "backgroundColor" : corporate_colors['superdark-green'] , "width" : "60px"}), width = "auto",style ={"position":"relative", "right":"248px" })
    ], justify = "center", align = "center", style={"background-color" : corporate_colors['light-green']}
    ), # Searching results row
    
    dbc.Row( # Alert row
        [  dbc.Col(        
            dbc.Alert(
            "There are no matching games!",
            id="alert",
            is_open= False,
            color="danger",
            style = {"width":"50%","margin":"auto", "height": "30px", "fontSize":"14px", 'padding-top' : '5px', "textAlign":"center" },
            duration=4000, fade = True)
        )
        ], style={"height": "30px"}
    ), # Alert row
    dbc.Row( # Graphs row
        [
            dbc.Col(dcc.Graph(id = "plot1"), width = 6),
            dbc.Col(dcc.Graph(id = "plot2"),width = 6)
        ], justify="center"
            
    ), # Graphs row

    # Empty Row
    dbc.Row([], style={"height": "10px"}),

html.Div([ # Years range filter
    html.Label("Select a Year Range: ", style={"padding-right":"10px"}),
    html.Div([
            dcc.Input(id = "input2", type='number', value=min_year, min = min_year, max = max_year),
            html.Div([
            dcc.RangeSlider(
                id='year_range',
                min= min_year,
                max= max_year,
                value=[min_year, max_year],
                allowCross=False,
                updatemode='drag',
                
            )
            ],style = {"position":"relative", "top": "10px"}),
            dcc.Input(id = "input3", type='number', value=max_year, min = min_year, max = max_year)
        ],
        style={"display": "grid", "grid-template-columns": "15% 40% 15%"})
       ],className = "row", style = {'align-items': 'center', "justify-content":"center","background-color" : corporate_colors['light-green']}
    )  # Years range filter
        
       
],fluid=True)

# Adding interactivity
@app.callback(
    Output("year_range", "value"),
    Input("input2", "value"),
    Input("input3", "value")
)
def update_slider(min_year, max_year):
    """
    Updates slider handles' position
    """
    return [min_year, max_year]

@app.callback(
    Output("plot1", "figure"),
    Output("plot2", "figure"),
    Output("alert", "is_open"),
    Output("input1", "children"),
    Output("input2", "value"),
    Output("input3", "value"),
    Input("genres", "value"),
    Input("rating", "value"),
    Input("year_range", "value")
)
def update_layout(genres, ratings, year_range):
    # applying the filters
    df_filtered1 = df[df['Year_of_Release'].between(year_range[0], year_range[1])]
    df_filtered2 = df_filtered1.loc[df_filtered1['Genre'].isin(genres)]
    df_filtered3 = df_filtered2.loc[df_filtered2['Rating'].isin(ratings)]
    # Update interactive texts
    number_of_games_selected  = len(df_filtered3)
    update_min_year = year_range[0]
    update_max_year = year_range[1]
    # Stacked Area Plots
    df_area_plots = df_filtered3.groupby(['Year_of_Release', 'Platform']).size().reset_index(name='Counts')
    fig1 = px.area(df_area_plots, x="Year_of_Release", y= "Counts", color="Platform", title = "Number of Game Releases per Year for Different Platforms",
    labels = {"Year_of_Release": "Release Year", "Counts": "Number of Game Releases"})
    fig1.update_layout( title_x=0.5, paper_bgcolor = 'rgba(41, 56, 55,100)', font = {'family' : corporate_font_family, "color":"white"})
    # Scatter Plots
    df_filtered4 = df_filtered3[~(df_filtered3["User_Score"]==-1)]
    fig2 = px.scatter(df_filtered4, x="User_Score", y="Critic_Score", color="Genre", title="Correlation: Critic Score VS User Score",
                 hover_data=['Year_of_Release', 'Platform'], labels ={"User_Score":"User Score", "Critic_Score":"Critic Score"})
    fig2.update_layout( title_x=0.5, paper_bgcolor = 'rgba(41, 56, 55,100)', font = {'family' : corporate_font_family},
    font_color="white")
    if number_of_games_selected  == 0 :
        alert_state = True
    else:
        alert_state = False

    return fig1, fig2, alert_state, number_of_games_selected, update_min_year, update_max_year

if __name__ == '__main__':
    app.run_server(debug = False)