import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Berlin Weather Dashboard", layout="wide")

st.title("Berlin Weather Dashboard")
st.write("Explore daily weather patterns in Berlin. Data is collected hourly from the Bright Sky API and aggregated by day.")

conn = duckdb.connect("/Users/sanawarsi/dev/data-pulse/bright_sky_weather.duckdb")
df = conn.execute("SELECT * FROM gold_weather_daily ORDER BY date").df()

st.divider()

today = df[df["date"] == df["date"].max()].iloc[0]
overall_avg = df["avg_temp_c"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Today's Temperature", f"{today['avg_temp_c']}°C", f"{round(today['avg_temp_c'] - overall_avg, 1)}°C vs average")
col2.metric("Today's Rainfall", f"{today['total_precipitation_mm']} mm")
col3.metric("Today's Max Wind", f"{today['max_wind_speed_kmh']} km/h")

st.divider()

st.subheader("Temperature Trend")
st.write("Shows how temperature changed over the past days. The three lines represent the daily average, highest and lowest recorded temperature.")
st.line_chart(df, x="date", y=["avg_temp_c", "max_temp_c", "min_temp_c"])

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Daily Rainfall")
    st.write("Total amount of rain that fell each day in millimetres. Taller bars mean heavier rainfall. Useful for spotting rainy spells or dry periods.")
    st.bar_chart(df, x="date", y="total_precipitation_mm")

with col_right:
    st.subheader("Wind Speed")
    st.write("Shows how windy each day was. The two bars show average and peak wind speed in km/h. A higher peak means strong gusts occurred during the day.")
    st.bar_chart(df, x="date", y=["avg_wind_speed_kmh", "max_wind_speed_kmh"])

st.divider()

st.subheader("Cloud Cover")
st.write("Percentage of the sky covered by clouds each day. 0% means a completely clear sky, 100% means fully overcast. Higher values typically mean less sunshine.")
st.bar_chart(df, x="date", y="avg_cloud_cover_pct")