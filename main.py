import streamlit as st
import random

# Page Config
st.set_page_config(page_title="Dice Cricket", page_icon="🏏")

st.title("🏏 Dice Cricket Prototype")

# Game Logic Function
def play_turn():
    roll = check_roll(random.randint(0, 10))
    st.session_state.balls += 1
    st.session_state.overs = int(st.session_state.balls/6) + "." + (st.session_state.balls - (int(st.session_state.balls)*6))
    if roll == 5:
        st.session_state.wickets += 1
        st.session_state.history.insert(0, "❌ OUT!")
    else:
        st.session_state.runs += roll
        st.session_state.history.insert(0, f"✅ Scored {roll} runs")


def check_roll(roll):
    match roll:
        case 0 | 1 :
            return 0
        case 2 | 3:
            return 1
        case 4 | 5:
            return 2
        case 6:
            return 3
        case 7: 
            return 4
        case 8:
            return 6
        case 9 | 10:
            return 5

# Initialize Session State (This keeps the score stored in the browser)
if 'runs' not in st.session_state:
    st.session_state.runs = 0
    st.session_state.wickets = 0
    st.session_state.balls = 0
    st.session_state.overs = ""
    st.session_state.history = []

if st.button('Next Ball', use_container_width=True):
    if st.session_state.wickets < 10:
        play_turn()
    else:
        st.error("Game Over! You've lost 10 wickets.")

# UI Layout
col1, col2, col3 = st.columns(3)
col1.metric("Total Runs", st.session_state.runs)
col2.metric("Wickets", st.session_state.wickets)
col3.metric("Overs", st.session_state.overs)

# Display Roll History
st.write("### Over History")
for log in st.session_state.history[:6]: # Show last 6 rolls
    st.text(log)

if st.button('Reset Game'):
    st.session_state.runs = 0
    st.session_state.wickets = 0
    st.session_state.balls = 0
    st.session_state.history = []
    st.rerun()
