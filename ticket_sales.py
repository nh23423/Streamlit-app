import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import os
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

def build(file):
    st.markdown("""<div style='border:1px solid black; padding: 10px'><h1 style='text-align: center; color: black;'>Future Events </h1></div>""", unsafe_allow_html=True)

    title_alignment= """
    <style>
    h1 {
      text-align: center;
    }
    </style>
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join(current_dir, "raw", "EventSalesReportDetailed-2024-04-29T07_50_50.csv")
    df = pd.read_csv(file)

    df['Event Date/Time'] = pd.to_datetime(df['Event Date/Time'], format = 'mixed')
    df['Event Date'] = df['Event Date/Time'].dt.date
    df['Year'] = df['Event Date/Time'].dt.year
    df['Month'] = df['Event Date/Time'].dt.month
    df['Event Name-Date'] = df['Event Name'] + df['Event Date/Time'].dt.strftime(' (%Y-%m-%d %H:%M)')

    from datetime import datetime

    df_future = df[(df['Event Date/Time'])>=datetime.now()]
    df_max = df_future[df_future['Seat Status'] !='Locked']
    df_current_unchanged = df_future[df_future['Seat Status'] =='Sold']

    df_current = df_current_unchanged.groupby(['Event Date/Time', 'Event Name', 'Event Name-Date']).agg({'Count': 'sum'}).reset_index()
    df_max = df_max.groupby(['Event Date/Time', 'Event Name', 'Event Name-Date']).agg({'Count': 'sum'}).reset_index()

    df_sales = pd.merge(df_max,df_current, on = ['Event Date/Time', 'Event Name','Event Name-Date'], suffixes = ('_max', '_current'))
    df_sales['Count_avail'] = df_sales['Count_max'] - df_sales['Count_current']
    df_sales['Percent_sold'] = df_sales['Count_current'] / df_sales['Count_max']
    df_sales['Percent_avail'] = df_sales['Count_avail'] / df_sales['Count_max']
    # df_sales['Event Name-Date'] = df_sales['Event Name'] + df_sales['Event Date/Time'].dt.strftime(' (%Y-%m-%d %H:%M)')
    # df_sales.drop_duplicates(subset = ['Event Name'], inplace = True)

    df_sales['Seats Booked'] = df_sales['Count_current']
    df_sales['Seats Available'] = df_sales['Count_avail']
    df_sales['Percentage Seats Booked'] = df_sales['Percent_sold']
    df_sales['Percentage Seats Available'] = df_sales['Percent_avail']

    colors = ['#636EFA', '#EF553B', '#3CB043']

    import plotly.express as px


    # Create a stacked bar chart
    fig1 = px.bar(df_sales, x='Event Name-Date', y=['Seats Booked', 'Seats Available'], color_discrete_sequence=['#636EFA', '#EF553B'],
                 title='Overview of Current and Available Counts by Event (Unscaled)', barmode='relative', text_auto = '.0d')

    change_dic = {i: i.split(' (')[0] for i in df_sales['Event Name-Date'].unique()}

    fig1.update_layout(yaxis_title = 'Number of tickets',
                       margin=dict(l=10, r=10, t=100, b=100),
                       xaxis_tickangle=-75. ,
                       legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1, 
                        title = dict(text = 'Legend:', side = 'left')),
                       #autosize=True,
                       #width=800,
                       #height=600,
                       yaxis_tickformat = '.0d',  # Change to '.0%' for percentage without decimal places
                       xaxis = {'type': 'category',
                                'tickmode' : 'auto',
                                'showtickprefix' : 'none',
                                'labelalias' : change_dic,
                                'title': 'Event Name', 
                                'tickfont' : dict(size = 9)
                                })  # Rename x-axis to 'labels'

    # Create a stacked bar chart
    fig2 = px.bar(df_sales, x='Event Name-Date', y=['Percentage Seats Booked', 'Percentage Seats Available'], color_discrete_sequence=['#636EFA', '#EF553B'],
                 title='Overview of Current and Available Counts by Event (Scaled)', barmode='relative',
                 text_auto='.0%')

    labels = [q.split(' (')[0] for q in df_sales['Event Name-Date'].unique()]
    # Set the x-axis labels to be rotated for better readability
    fig2.update_layout(yaxis_title = 'Percentage of tickets',
                       margin=dict(l=10, r=10, t=100, b=100),
                       xaxis_tickangle=-75. ,
                       legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1, 
                        title = dict(text = 'Legend:', side = 'left')),
                       #autosize=False,
                       #width=800,
                       #height=600,
                       yaxis_tickformat = '.0%',  # Change to '.0%' for percentage without decimal places
                       xaxis = {'type': 'category',
                                'tickmode' : 'auto',
                                'showtickprefix' : 'none',
                                'labelalias' : change_dic,
                                'tickfont' : dict(size = 9),
                                #'tickvals' : np.arange(len(df_sales['Event Name-Date'].unique())),
                                #'ticktext': labels,
                                'title': 'Event Name'})  # Rename x-axis to 'labels'
    # fig2.update_xaxes(tickvals=np.arange(2), ticktext=labels)
    # fig2.update_traces(hoverinfo='x+y')

    palette3 = {'Booked Seats' : '#636EFA', 'Available Seats': '#EF553B'}

    fig3 = go.Figure()
    buttons = []

    frames = len(df_sales['Event Name-Date'].unique())
    for i, name in enumerate(df_sales['Event Name-Date'].unique()[:]):
        if i == 0: 
            vis = True
        else: 
            vis = False
        df_name = df_sales[df_sales['Event Name-Date'] == name]
        fig3.add_trace(go.Pie(labels = ['Booked Seats', 'Available Seats'], values = np.append(df_name['Count_current'].values, df_name['Count_avail'].values), name=f'{name}', visible=vis, rotation=-90, sort=False))
        #fig3 = px.bar(df_month, x='Year', y='Sum of Price')
        frames = len(df_sales['Event Name-Date'].unique())
        bars = 1
        scenarios = [list(s) for s in [e==1 for e in np.eye(frames)]]
        visibility = [list(np.repeat(e,bars)) for e in scenarios]
        button = dict(label=f'{name}', method="restyle", args=[{"visible": visibility[i]}])
        buttons.append(button)

    fig3.update_traces(hoverinfo='label+percent+value', textinfo='label+percent', marker=dict(colors=colors), insidetextorientation='horizontal')

    fig3.update_layout(
        title = "Percentage Tickets Sales by Event",
        title_font=dict(size=20, family="Arial", color="black"),  # Title font
        title_x = 0.4,
        updatemenus=[
            dict(
                type='dropdown',
                direction = 'down',
                buttons = buttons,
                x= -1.25,  # Adjust the x-coordinate to position the dropdown menu horizontally
                y= 1.2,  # Adjust the y-coordinate to position the dropdown menu vertically
                xanchor = "left",  # Anchor the x-coordinate to the center of the plot
                yanchor = "top",  # Anchor the y-coordinate to the bottom of the plot
                bordercolor = "black",  # Border color of the dropdown menu
                borderwidth = 1  # Border width of the dropdown menu
            )],
        margin=dict(l=250, r=0, t=150, b=50, pad = 100),  # Adjust margins
        font=dict(size=14, family="Arial", color="black"),
)

    df_current_unchanged = df_current_unchanged.sort_values('Event Date/Time')

    fig4 = go.Figure()
    buttons = []

    frames = len(df_current_unchanged['Event Name-Date'].unique())
    for i, name in enumerate(df_current_unchanged['Event Name-Date'].unique()[:]):
        if i == 0: 
            vis = True
        else: 
            vis = False
        df_name = df_current_unchanged[df_current_unchanged['Event Name-Date'] == name]
        # Ensure 'Counter', 'Phone', and 'Web' labels are always present
        labels1 = ['Counter', 'Phone', 'Web']

        # Create a dictionary mapping labels to their corresponding values, or 0 if the label doesn't exist
        values_dict = {label: df_name[df_name['Sales Channel'] == label]['Count'].sum()
                    if label in df_name['Sales Channel'].values else 0
                    for label in labels1}

        # Extract the values from the dictionary
        values1 = [values_dict[label] for label in labels1]

        fig4.add_trace(go.Pie(labels = labels1, values = values1, name=f'{name}', visible=vis, rotation = -90, sort=False))
        frames = len(df_current_unchanged['Event Name-Date'].unique())
        bars = 1
        scenarios = [list(s) for s in [e==1 for e in np.eye(frames)]]
        visibility = [list(np.repeat(e,bars))*2 for e in scenarios]
        button = dict(label=f'{name}', method="restyle", args=[{"visible": visibility[i]}])
        buttons.append(button)

    fig4.update_traces(hoverinfo='label+percent+value', textinfo='label+percent', marker=dict(colors=colors), insidetextorientation='horizontal')

    fig4.update_layout(
        title = "Percentage Sales Channel",
        title_font=dict(size=20, family="Arial", color="black"),  # Title font
        title_x = 0.4,
        updatemenus=[
            dict(
                type='dropdown',
                direction = 'down',
                buttons = buttons,
                x= -1.25,  # Adjust the x-coordinate to position the dropdown menu horizontally
                y= 1.2,  # Adjust the y-coordinate to position the dropdown menu vertically
                xanchor = "left",  # Anchor the x-coordinate to the center of the plot
                yanchor = "top",  # Anchor the y-coordinate to the bottom of the plot
                bordercolor = "black",  # Border color of the dropdown menu
                borderwidth = 1  # Border width of the dropdown menu
            )],
        margin=dict(l=250, r=0, t=150, b=50, pad = 100),  # Adjust margins
        font=dict(size=14, family="Arial", color="black"),
)

    fig5 = go.Figure()
    buttons = []

    frames = len(df_current_unchanged['Event Name-Date'].unique())
    for i, name in enumerate(df_current_unchanged['Event Name-Date'].unique()[:]):
        if i == 0:
            vis = True
        else:
            vis = False
        df_name = df_current_unchanged[df_current_unchanged['Event Name-Date'] == name]

        # Ensure 'Price band A', 'Price band B', and 'Price band C' labels are always present
        labels2 = ['Price band A', 'Price band B', 'Price band C']

        # Create a dictionary mapping labels to their corresponding values, or 0 if the label doesn't exist
        values_dict = {label: df_name[df_name['Ticket Band'] == label]['Count'].sum()
                    if label in df_name['Ticket Band'].values else 0
                    for label in labels2}

        # Extract the values from the dictionary
        values2 = [values_dict[label] for label in labels2]

        fig5.add_trace(go.Pie(labels = labels2, values = values2, name=f'{name}', visible=vis, rotation = -90, sort=False))
        frames = len(df_current_unchanged['Event Name-Date'].unique())
        bars = 1
        scenarios = [list(s) for s in [e==1 for e in np.eye(frames)]]
        visibility = [list(np.repeat(e,bars))*2 for e in scenarios]
        button = dict(label=f'{name}', method="restyle", args=[{"visible": visibility[i]}])
        buttons.append(button)

    fig5.update_layout(
        title = "Percentage Ticket Band by Event",
        title_font=dict(size=20, family="Arial", color="black"),  # Title font
        title_x = 0.4,
        updatemenus=[
            dict(
                type='dropdown',
                direction = 'down',
                buttons = buttons,
                x= -1.25,  # Adjust the x-coordinate to position the dropdown menu horizontally
                y= 1.2,  # Adjust the y-coordinate to position the dropdown menu vertically
                xanchor = "left",  # Anchor the x-coordinate to the center of the plot
                yanchor = "top",  # Anchor the y-coordinate to the bottom of the plot
                bordercolor = "black",  # Border color of the dropdown menu
                borderwidth = 1  # Border width of the dropdown menu
            )],
        margin=dict(l=250, r=0, t=150, b=50, pad = 100),  # Adjust margins
        font=dict(size=14, family="Arial", color="black"),
)
    fig5.update_traces(hoverinfo='label+percent+value', textinfo='label+percent', marker=dict(colors=colors), insidetextorientation='horizontal')

    st.markdown(title_alignment, unsafe_allow_html=True)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(fig5)