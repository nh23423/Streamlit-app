import streamlit as st
import plotly.express as px
import pandas as pd
import os
from datetime import datetime

def build(file):
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

  year_now = df[df['Year'] == datetime.today().year]
  number = year_now['Sum of Price'].sum()

  st.markdown(f"""<div style='border:1px solid black; padding: 10px'><h1 style='text-align: center; color: black;'>Sum of Prices</h1></div>""", unsafe_allow_html=True)
  st.markdown(f"""<div style='border:0px solid black; padding: 10px'><h2 style='text-align: center; color: black;'>The Current Sum of Prices for {datetime.today().year} is: \n£{number:,.2f} </h2></div>""", unsafe_allow_html=True)