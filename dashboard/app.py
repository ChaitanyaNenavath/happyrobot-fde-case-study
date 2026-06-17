import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="HappyRobot Carrier Dashboard",
    layout="wide"
)

st.title("🚚 HappyRobot Carrier Sales Dashboard")
st.caption("Inbound carrier sales automation metrics and call outcomes")

metrics = requests.get(f"{API_URL}/metrics").json()
calls = requests.get(f"{API_URL}/calls").json()

success_rate = 0
if metrics["total_calls"] > 0:
    success_rate = round(
    (metrics["booked_loads"] /
     (metrics["booked_loads"] + metrics["failed_negotiations"])) * 100,
    2
)
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Calls", metrics["total_calls"])
col2.metric("Booked Loads", metrics["booked_loads"])
col3.metric("Failed Negotiations", metrics["failed_negotiations"])
col4.metric("Success Rate", f"{success_rate}%")
col5.metric("Average Final Rate", f"${metrics['average_final_rate']}")

st.divider()

if len(calls) > 0:
    df = pd.DataFrame(calls)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Call Outcomes")
        outcome_counts = df["outcome"].value_counts().reset_index()
        outcome_counts.columns = ["Outcome", "Count"]

        fig_outcome = px.bar(
            outcome_counts,
            x="Outcome",
            y="Count",
            text="Count",
            title="Outcome Distribution"
        )
        st.plotly_chart(fig_outcome, use_container_width=True)

    with chart_col2:
        st.subheader("Carrier Sentiment")
        sentiment_counts = df["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        fig_sentiment = px.pie(
            sentiment_counts,
            names="Sentiment",
            values="Count",
            title="Sentiment Distribution"
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)

    st.subheader("Load Performance")
    load_perf = df.groupby("load_id").agg(
        calls=("load_id", "count"),
        final_rate=("final_rate", "max"),
        outcome=("outcome", "first")
    ).reset_index()

    st.dataframe(load_perf, use_container_width=True)

    st.subheader("Call Records")
    st.dataframe(df, use_container_width=True)

else:
    st.info("No call records found.")