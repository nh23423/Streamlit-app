import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import os
from datetime import datetime

def build(file):
    st.markdown("""<div style='border:1px solid black; padding: 10px'><h1 style='text-align: center; color: black;'>Historic Data </h1></div>""", unsafe_allow_html=True)

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

    df = df[(df['Year'])<datetime.today().year]
    df = df[(df['Year'])>2013]

    df_sum = df.groupby(['Year', 'Month'])['Sum of Price'].sum().reset_index()
    df_sum['Year-Month'] = df_sum['Year'].astype(str) + '-' + df_sum['Month'].astype(str)

    df_year = df.groupby(['Year'])['Sum of Price'].sum().reset_index()
    df_by_month = df.groupby('Month')['Sum of Price'].sum().reset_index()

    fig = px.bar(df_sum, x='Year-Month', y='Sum of Price')
    fig2 = px.bar(df_sum, x='Month', y='Sum of Price', color='Year')
    fig3 = px.bar(df_year, x='Year', y='Sum of Price')

    import plotly.graph_objects as go
    figall = go.Figure()
    buttons = []

    frames = len(df_sum['Month'].unique())
    for i, month in enumerate(sorted(df_sum['Month'].unique()[:])):
        if i == 0:
            vis = True
        else:
            vis = False
        df_month = df_sum[df_sum['Month'] == month]
        figall.add_trace(go.Bar(x=df_month['Year'], y=df_month['Sum of Price'], name=f'Month {month}', visible=vis))
        #figall = px.bar(df_month, x='Year', y='Sum of Price')
        frames = len(df_sum['Month'].unique())
        bars = 1
        scenarios = [list(s) for s in [e==1 for e in np.eye(frames)]]
        visibility = [list(np.repeat(e,bars)) for e in scenarios]
        button = dict(label=f'Month {month}', method="restyle", args=[{"visible": visibility[i]}])
        buttons.append(button)

    figall.update_layout(
        title = "Total Sales (Separated into Months)",
        xaxis_title="Year",
        yaxis_title="Total Sales",
        title_font=dict(size=20, family="Arial", color="black"),  # Title font
        title_x = 0.4,
        margin=dict(l=60, r=50, t=80, b=50),  # Adjust margins
        paper_bgcolor='rgb(240, 240, 240)',  # Background color
        font=dict(size=14, family="Arial", color="black"),
        updatemenus=[
            dict(
                type='dropdown',
                direction = 'down',
                buttons = buttons,
                x= -0.2,  # Adjust the x-coordinate to position the dropdown menu horizontally
                y= 1.2,  # Adjust the y-coordinate to position the dropdown menu vertically
                xanchor = "left",  # Anchor the x-coordinate to the center of the plot
                yanchor = "top",  # Anchor the y-coordinate to the bottom of the plot
                bordercolor = "black",  # Border color of the dropdown menu
                borderwidth = 1  # Border width of the dropdown menu
            )])

    fig.update_layout(
        title = f"Total Sales in {df['Year'].min()} - {df['Year'].max()}",
        title_font=dict(size=20, family="Arial", color="black"),  # Title font
        title_x = 0.4,
        xaxis_title="Year",
        yaxis_title="Total Sales",

        margin=dict(l=60, r=50, t=80, b=50),  # Adjust margins
        paper_bgcolor='rgb(240, 240, 240)',  # Background color
        font=dict(size=14, family="Arial", color="black"),
    )

    fig2.update_layout(
        title = "Total Sales in Each Month",
        xaxis_title="Year",
        yaxis_title="Total Sales",
        title_font=dict(size=20, family="Arial", color="black"),  # Title font
        title_x = 0.4,
        margin=dict(l=60, r=50, t=80, b=50),  # Adjust margins
        paper_bgcolor='rgb(240, 240, 240)',  # Background color
        font=dict(size=14, family="Arial", color="black"),
    )

    fig3.update_layout(
        title = f"Total Sales in {df['Year'].min()} - {df['Year'].max()} (grouped by year)",
        title_font=dict(size=20, family="Arial", color="black"),  # Title font
        title_x = 0.4,
        xaxis_title="Month of the Year",
        yaxis_title="Total Sales",
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=50, t=80, b=50),  # Adjust margins
        paper_bgcolor='rgb(240, 240, 240)',  # Background color
        font=dict(size=14, family="Arial", color="black"),
    )

    st.markdown(title_alignment, unsafe_allow_html=True)
    st.plotly_chart(fig)
    st.plotly_chart(fig3)
    st.plotly_chart(fig2)
    st.plotly_chart(figall)