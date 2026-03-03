import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

st.set_page_config(layout="wide")

st.title("🔴 Hapoel Beer Sheva Youth - Match Dashboard")

# Load data
df = pd.read_excel("HBS_Youth_Sample_Match_Data.xlsx")

# Sidebar
st.sidebar.header("Filters")
player = st.sidebar.selectbox("Select Player", df["player"].unique())

col1, col2 = st.columns(2)

# -------- Shot Map --------
with col1:
    st.subheader("Shot Map")

    shots = df[(df["event_type"] == "Shot") & (df["player"] == player)]

    pitch = Pitch(pitch_type='statsbomb')
    fig, ax = pitch.draw()

    goals = shots[shots["outcome"] == "Goal"]
    saved = shots[shots["outcome"] == "Saved"]
    blocked = shots[shots["outcome"] == "Blocked"]
    off_target = shots[shots["outcome"] == "Off Target"]

    # Off target
    pitch.scatter(
        off_target["x"], off_target["y"],
        ax=ax,
        s=400,
        color='red',
        edgecolor='white',
        label='Off Target'
    )

    # Saved
    pitch.scatter(
        saved["x"], saved["y"],
        ax=ax,
        s=400,
        color='green',
        edgecolor='white',
        label='Saved'
    )

    # Blocked
    pitch.scatter(
        blocked["x"], blocked["y"],
        ax=ax,
        s=400,
        color='orange',
        edgecolor='white',
        label='Blocked'
    )

    # Goals ⭐
    pitch.scatter(
        goals["x"], goals["y"],
        ax=ax,
        s=700,
        marker='*',
        color='gold',
        edgecolor='black',
        label='Goal'
    )

    ax.legend(loc='upper left')
    st.pyplot(fig)

# -------- Pass Map --------
with col2:
    st.subheader("Pass Map")

    passes = df[
        (df["event_type"] == "Pass") &
        (df["player"] == player) &
        (df["outcome"] == "Complete")
    ]

    pitch = Pitch(pitch_type='statsbomb')
    fig2, ax2 = pitch.draw()

    pitch.arrows(
        passes["x"], passes["y"],
        passes["end_x"], passes["end_y"],
        ax=ax2
    )

    st.pyplot(fig2)

# -------- Heatmap --------
st.subheader("Team Heatmap")

pitch = Pitch(pitch_type='statsbomb')
fig3, ax3 = pitch.draw()

bin_statistic = pitch.bin_statistic(
    df["x"], df["y"],
    statistic='count',
    bins=(6,4)
)

pitch.heatmap(bin_statistic, ax=ax3, cmap='Reds')

st.pyplot(fig3)

# -------- Basic Stats --------
st.subheader("Basic Stats")

total_shots = df[df["event_type"] == "Shot"].shape[0]
total_passes = df[df["event_type"] == "Pass"].shape[0]

col3, col4 = st.columns(2)
col3.metric("Total Shots", total_shots)
col4.metric("Total Passes", total_passes)

#http://localhost:8501/#shot-map

