import pandas as pd
import numpy as np
import dash
from dash import html 
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input ,Output
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
from dash import dcc, html, callback, Output
import pathlib
import os 

# load the data ------------------------------------------------------------------------


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()
df= pd.read_excel(DATA_PATH.joinpath("unemplo_figures_1991.xlsx") )
                  
YEARS=[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
       2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
       1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]
# set the layout for the application----------------------------------------------
app=dash.Dash(external_stylesheets=[dbc.themes.CYBORG],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],suppress_callback_exceptions=True)
server=app.server
app.layout=dbc.Container([
                dbc.Row(dbc.Col(html.H3("Unemployement Rate Worldwide Since 1991",className='text-center mb-4'),width=12)), 
                dbc.Row([dbc.Col([html.H6(['Choose Years to view Unemployment Rate :']),]),
                                      html.Div(dcc.RangeSlider(id='yearslider',
                                                 marks={str(year):{'label':str(year),'style':{"color": "#7fafdf"},} for year in YEARS},
                                                        step=1
                                                        ,
                                                 min=min(YEARS),
                                                 max=max(YEARS),
                                                 value=[2010,2020],
                                                 dots=True, 
                                                 allowCross=False, 
                                                 disabled=False, 
                                                 pushable=2, updatemode='drag', 
                                                 included=True,vertical=False,
                                                 verticalHeight=900, className='None', 
                                                 tooltip={'always_visible':False, 'placement':'bottom'}),

                                                 style={'width':'90%'})]),
              dbc.Row([dbc.Col([dcc.Graph(id="map",figure={})],xs=12, sm=12, md=12, lg=5, xl=5),dbc.Col(html.Div(id='show_data'),xs=12, sm=12, md=12, lg=5, xl=5)]),
              html.Br(),
              dbc.Row(html.Div(id='marquee'))
             
              


              ],fluid=True)

              
                                                 
                                                                                        
                                                                                       

# the call back functions------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output('map','figure'),
    Input('yearslider','value')
)
def update_map(years):
    year_0 ,year_1=years
    filtered_df=df[(df['Year']>=year_0)&(df['Year']<=year_1)]
    grouped_df=filtered_df.groupby(['Country','Year','Countrycode'])['Unemployment'].mean().reset_index()
    fig1=px.choropleth(grouped_df,locations='Countrycode',hover_data=['Unemployment','Country'],color='Unemployment',
                  hover_name='Country', color_continuous_scale=px.colors.sequential.Plasma,projection='orthographic')
    fig1.update_layout(plot_bgcolor='#000000',paper_bgcolor='#000000', height=600,margin=dict(l=0,r=0,t=0,b=0) ,geo=dict(bgcolor= '#000000'), )
    fig1.layout.template='plotly_dark'
    return fig1
@app.callback(
    Output('show_data','children'),
    [Input('map','clickData')],
    Input('yearslider','value')

)
def update_line_chart(clickdata,years):
    if clickdata:
        df['AnnualChange']=df['Unemployment']/df['Unemployment'].shift()-1
        df.dropna(inplace=True)
        points=clickdata['points'][0]['location']
        year_0,year_1=years
        filtered_df=df[(df['Year']>=year_0)&(df['Year']<=year_1)]
        filtered_df=filtered_df[filtered_df['Countrycode']==points]
        filtered_df["Color"] = np.where(filtered_df["AnnualChange"]<0, 'green', 'red')
        clickedcountry=filtered_df.Country.unique()[0]
        fig4=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
                        y_title='Changes      Unemployment Rate',
                        row_heights=[0.7,0.3] )

        fig4.layout.template="plotly_dark"

        fig4.add_trace(go.Scatter(x=filtered_df['Year'],y=filtered_df['Unemployment'],line=dict(color='#00FFFF'),line_shape='spline',fill='tonexty' ,fillcolor='rgba(0,255,255,0.1)',name="unemployment Rate",mode='lines'),row=1,col=1,secondary_y=False)

        fig4.add_trace(go.Bar( x=filtered_df['Year'],y=filtered_df['AnnualChange'],marker_color=filtered_df['Color'],name='change%'),row=2,col=1,secondary_y=False)
        fig4.update_layout(title=f"Unemployment Rate in {clickedcountry}  Since {year_0}",xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),
                        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=False,height=600,width=1000)
        fig4.update_traces(xaxis='x2' )
        return dcc.Graph(figure=fig4)
    else:
        df['AnnualChange']=df['Unemployment']/df['Unemployment'].shift()-1
        df.dropna(inplace=True)
        year_0,year_1=years
        filtered_df2=df[(df['Year']>=year_0)&(df['Year']<=year_1)]
        filtered_df2=filtered_df2[filtered_df2['Country']=='Africa Eastern and Southern']
        filtered_df2["Color"] = np.where(filtered_df2["AnnualChange"]<0, 'green', 'red')
        fig5=make_subplots(rows=2,cols=1,shared_xaxes=True,shared_yaxes=False ,vertical_spacing=0.02,
                        y_title='Changes      Unemployment Rate',
                        row_heights=[0.7,0.3] )

        fig5.layout.template="plotly_dark"

        fig5.add_trace(go.Scatter(x=filtered_df2['Year'],y=filtered_df2['Unemployment'],line=dict(color='#00FFFF'),line_shape='spline',fill='tonexty' ,fillcolor='rgba(0,255,255,0.1)',name="unemployment Rate",mode='lines'),row=1,col=1,secondary_y=False)

        fig5.add_trace(go.Bar( x=filtered_df2['Year'],y=filtered_df2['AnnualChange'],marker_color=filtered_df2['Color'],name='change%'),row=2,col=1,secondary_y=False)
        fig5.update_layout(title=f"Unemployment Rate in Africa Eastern and Southern Since {year_0}",xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),
                        hovermode='x unified', plot_bgcolor='#000000',paper_bgcolor='#000000' ,showlegend=False,height=600)
        fig5.update_traces(xaxis='x2' )
        return dcc.Graph(figure=fig5)
    
@app.callback(
    Output('marquee','children'),
    [Input('map','clickData')],
    Input('yearslider','value')

)
def update_marquee(clickdata,years):
    if clickdata:
        points=clickdata['points'][0]['location']
        year_0,year_1=years
        filtered_df=df[(df['Year']>=year_0)&(df['Year']<=year_1)]
        filtered_df=filtered_df[filtered_df['Countrycode']==points]
        clickedcountry=filtered_df.Country.unique()[0]
        unemploymentclickedcountry=round(filtered_df['Unemployment'].mean(),0)
        return dbc.Row( html.Marquee(f"Average Annual Unemployment Rate in { clickedcountry} is {unemploymentclickedcountry} % 🌍 🌍  Please Click on Any Country on the Map to Gain Insight about Unemployment   🌍 Unemployment Rates Worldwide Since 1991  🌍 Bahageel Dashboard 🌍Data Compiled from  The World Bank  🌍 Top 10 Countries With Highest Average Annual Unemployment Rates are : 🌍 North Macedonia -30%  🌍  Lesotho -29%  🌍 South Africa -28%  🌍  Djibouti-27%  🌍 Bosnia Herzegovia -25%  🌍 Estwatini -25%  🌍 Montenegro-22%  🌍 Namibia-21%  🌍 Democratic Republic Of Congo -20%  🌍 West Bank and Gaza -20% "), style = {'color':'cyan'})
    else:
        return dbc.Row( html.Marquee("Pleasee Click on Any Country on the Map to Gain Insight about Unemployment Rate Countrywise-  🌍🌍-The Figures are provided By  The World Bank 🌍 Top 10 Countries With Highest Average Annual Unemployment Rates are : 🌍 North Macedonia -30%  🌍  Lesotho -29%  🌍 South Africa -28%  🌍  Djibouti-27%  🌍 Bosnia Herzegovia -25%  🌍 Estwatini -25%  🌍 Montenegro-22%  🌍 Namibia-21%  🌍 Democratic Republic Of Congo -20%  🌍 West Bank and Gaza -20% "), style = {'color':'red'})




        


if __name__=='__main__':
    app.run_server(debug=True, port=8000)
    
         
