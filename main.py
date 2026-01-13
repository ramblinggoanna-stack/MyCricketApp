import streamlit as st
import random

# Page Config
st.set_page_config(page_title="Dice Cricket", page_icon="🏏")

st.title("🏏 Dice Cricket Prototype")

# Initialize Session State (This keeps the score stored in the browser)
if 'runs' not in st.session_state:
    st.session_state.runs = 0
    st.session_state.wickets = 0
    st.session_state.history = []

# Game Logic Function
def play_turn():
    roll = random.randint(1, 6)
    if roll == 5:
        st.session_state.wickets += 1
        st.session_state.history.insert(0, "❌ Rolled a 5: OUT!")
    else:
        st.session_state.runs += roll
        st.session_state.history.insert(0, f"✅ Rolled a {roll}: +{roll} runs")

# UI Layout
col1, col2 = st.columns(2)
col1.metric("Total Runs", st.session_state.runs)
col2.metric("Wickets", st.session_state.wickets)

if st.button('Roll the Dice', use_container_width=True):
    if st.session_state.wickets < 10:
        play_turn()
    else:
        st.error("Game Over! You've lost 10 wickets.")

# Display Roll History
st.write("### Roll History")
for log in st.session_state.history[:5]: # Show last 5 rolls
    st.text(log)

if st.button('Reset Game'):
    st.session_state.runs = 0
    st.session_state.wickets = 0
    st.session_state.history = []
    st.rerun()
