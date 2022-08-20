import pandas as pd
import json
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import no_update

df=pd.read_excel(r"C:\Users\User\Desktop\Machine Learning Project\globalterrorismdb_0522dist.xlsx")
df.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','provstate':'state',
                   'region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed',
                   'nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type',
                   'weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
df=df[['Year','Month','Day','Country','state','Region','city','latitude','longitude','AttackType','Killed',
       'Wounded','suicide','Target','Summary','Group','Target_type','Weapon_type','Motive',"success"]]
df_nigeria=df[df["Country"]=="Nigeria"]

# data to be used
dash_data =  df_nigeria.copy()
year_list = [i for i in (dash_data['Year'].unique())]
# Create a dash application
app = dash.Dash(__name__)
# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

app.layout= html.Div(children=[html.H1(
    'TERRORISM IN NIGERIA INFORMATION DASHBOARD',
    style={'textAlign':'center','color':'#503D36','font-size': 24}),
    html.Div([
        # Add a division
        html.Div([
            # Create a division for adding dropdown helper text for choosing year
            html.Div(
                [
                    html.H2('Choose Year:', style={'margin-right': '2em'})
                    ]
                ),
            dcc.Dropdown(id='input-year', 
                         # Update dropdown values using list comphrehension
                         options=[{'label': i, 'value': i} for i in year_list],
                         placeholder="Select a year",
                         style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),
            # Place them next to each other using the division style
            ], style={'display': 'flex'}),
        ]),
    # Add Computed graphs
    # Add empty divisions providing an id that will be updated during callback
    html.Div([
        html.Div(dcc.Graph(id='plot1')),
        html.Div(dcc.Graph(id='plot2'))
        ], style={'display': 'flex'}),
                               
    html.Div([
        html.Div(dcc.Graph(id='plot3')),
        html.Div(dcc.Graph(id='plot4'))
        ], style={'display': 'flex'}),
                                
    # Add another division with two empty divisions inside.                                  
    html.Div([
        html.Div(dcc.Graph(id='plot5')),
        html.Div(dcc.Graph(id='plot6'))
        ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='plot7')),
        html.Div(dcc.Graph(id='plot8'))
        ], style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='plot9')),
        html.Div(dcc.Graph(id='plot10'))
        ], style={'display': 'flex'})
    ])

@app.callback(
    [Output(component_id='plot1', component_property='figure'),
     Output(component_id='plot2', component_property='figure'),
     Output(component_id='plot3', component_property='figure'),
     Output(component_id='plot4', component_property='figure'),
     Output(component_id='plot5', component_property='figure'),
     Output(component_id='plot6', component_property='figure'),
     Output(component_id='plot7', component_property='figure'),
     Output(component_id='plot8', component_property='figure'),
     Output(component_id='plot9', component_property='figure'),
     Output(component_id='plot10', component_property='figure')],
    [Input(component_id='input-year', component_property='value')])
# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select data
    dash_data=df_nigeria[df_nigeria["Year"]==int(entered_year)]
    # Number of People attacks in each state per year
    bar_data1 = dash_data.groupby(["state"])["Year"].count().sort_values(ascending=False).reset_index()
    bar_fig1 = px.bar(bar_data1, x='state', y='Year', color='state', title='Total Yearly Number of attacks')
    bar_fig1.update_layout(xaxis_title="State",yaxis_title="Number of Attacks")
    
    # Number of people Killed per year
    bar_data2 = dash_data.groupby(["state"])["Killed"].sum().sort_values(ascending=False).reset_index()
    bar_fig2 = px.bar(bar_data2, x='state', y='Killed', color='state', title='Total Yearly Number of deaths')
    bar_fig2.update_layout(xaxis_title="State",yaxis_title="Number of Deaths")
            
    # Success Rate of Attacks
    pie_data = dash_data.groupby(['success']).agg(Total_attacks=('Killed', 'count'),Total_killed=('Killed', 'sum'),Total_wound=('Wounded', 'sum')).sort_values(by="Total_attacks", ascending=False).reset_index()
    pie_data[["Total_killed","Total_wound"]]=pie_data[["Total_killed","Total_wound"]].astype(int)
    labels=pie_data["success"].replace(1,"SUCCESS").replace(0, "UNSUCCESSFUL")
    pie_fig = px.pie(pie_data, values='Total_attacks', names=labels, title='SUCCESS RATE(%) OF TERRORIST ATTACKS')
    
    # Percentage of attacks by zone
    pie_data1 = dash_data.groupby(['zone']).agg(Total_attacks=('Killed', 'count'),Total_killed=('Killed', 'sum'),Total_wound=('Wounded', 'sum')).sort_values(by="Total_attacks", ascending=False).reset_index()
    pie_data1[["Total_killed","Total_wound"]]=pie_data1[["Total_killed","Total_wound"]].astype(int)
    label1=dash_data["zone"].unique()
    pie_fig1 = px.pie(pie_data1, values='Total_attacks', names=label1, title='% OF ATTACKS BY GEOPOLITICAL ZONE')
    
    # Percentage of Death by Geopolitical zone
    pie_data2 = dash_data.groupby(['zone']).agg(Total_attacks=('Killed', 'count'),Total_killed=('Killed', 'sum'),Total_wound=('Wounded', 'sum')).sort_values(by="Total_attacks", ascending=False).reset_index()
    pie_data2[["Total_killed","Total_wound"]]=pie_data2[["Total_killed","Total_wound"]].astype(int)
    label2=dash_data["zone"].unique()
    pie_fig2 = px.pie(pie_data2, values='Total_killed', names=label2, title='% OF DEATHS BY GEOPOLITICAL ZONE')
    
    #Terrorist Groups
    bar_data3 = dash_data.groupby(["Group"])["Year"].count().sort_values(ascending=False).reset_index()
    bar_fig3 = px.bar(bar_data3, x='Group', y='Year', color='Group', title='Terrorist Group attacks')
    bar_fig3.update_layout(xaxis_title="Terrorist Group",yaxis_title="Number of Attacks")
    
    #Most Targetted type of victims
    bar_data4 = dash_data.groupby(['Target_type'])['Year'].count().sort_values(ascending=False).reset_index()
    bar_fig4 = px.bar(bar_data4, x='Target_type', y='Year', color='Target_type', title='Most Targetted Class of Victims')
    bar_fig4.update_layout(xaxis_title="Targeted Class",yaxis_title="Number of Attacks")
    
    #Most used type of weapon
    bar_data5= dash_data.groupby(['Weapon_type'])['Year'].count().sort_values(ascending=False).reset_index()
    bar_fig5 = px.bar(bar_data5, x='Weapon_type', y='Year', color='Weapon_type', title='Most used Weapons for Terrorism')
    bar_fig5.update_layout(xaxis_title="Weapon Type",yaxis_title="Number of Attacks")
    
    #Most common type of attack
    bar_data6=dash_data.groupby(['AttackType'])['Year'].count().sort_values(ascending=False).reset_index()
    bar_fig6 = px.bar(bar_data6, x='AttackType', y='Year', color='AttackType', title='Methods of Terrorist Attacks')
    bar_fig6.update_layout(xaxis_title="Attack Type",yaxis_title="Number of Attacks")
    
    # distribution of attacks from each state using choropleth
    nigeria_geo=pd.DataFrame({"state":dash_data["state"].value_counts().index,"Number-of-attacks":dash_data["state"].value_counts().values})
    path=open(r"C:\Users\User\Desktop\Machine Learning Project\Boundary_states.json")
    state_geo=json.load(path)
    max_count = nigeria_geo['Number-of-attacks'].max()
    map_fig = px.choropleth_mapbox(nigeria_geo,
                               geojson=state_geo,
                               locations='state',
                               color='Number-of-attacks',
                               color_continuous_scale="YlGnBu",
                               range_color=(0, max_count),
                               featureidkey="properties.StateName",
                               mapbox_style="carto-positron",
                               opacity=0.5,
                               center = {"lat": 9.0820, "lon": 8.6753}, 
                               zoom=5)
    map_fig.update_geos(fitbounds="locations",visible=False)
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},)
    # Return dcc.Graph component to the empty division
    return bar_fig1, bar_fig2, pie_fig1, pie_fig2, bar_fig3, bar_fig4, bar_fig5, bar_fig6,pie_fig, map_fig

if __name__ == '__main__':
    app.run_server(debug=False)