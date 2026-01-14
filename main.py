import streamlit as st
import random

st.set_page_config(page_title="Dice Cricket", page_icon="🏏")
st.title("🏏 Dice Cricket: 1v1 Battle")

# --- 1. DEFINITIONS ---
def check_roll(roll):
    match roll:
        case 0 | 1: return 0
        case 2 | 3: return 1
        case 4 | 5: return 2
        case 6: return 3
        case 7: return 4
        case 8: return 6
        case 9 | 10: return 5

def play_turn():
    roll = check_roll(random.randint(0, 10))
    st.session_state.balls += 1
    st.session_state.overs = str(int(st.session_state.balls/6)) + "." + str((st.session_state.balls - (int(st.session_state.balls/6)*6)))    if st.session_state.current_player == 1:
        st.session_state.balls_p1 += 1
        if roll == 5:
            st.session_state.wickets_p1 += 1
            st.session_state.history.insert(0, f"P1: ❌ OUT!")
        else:
            st.session_state.runs_p1 += roll
            st.session_state.history.insert(0, f"P1: ✅ {roll} runs")
        if st.session_state.wickets_p1 >= 10:
            st.session_state.current_player = 2
            st.session_state.history = ["--- PLAYER 2 START ---"]
    else:
        st.session_state.balls_p2 += 1
        if roll == 5:
            st.session_state.wickets_p2 += 1
            st.session_state.history.insert(0, f"P2: ❌ OUT!")
        else:
            st.session_state.runs_p2 += roll
            st.session_state.history.insert(0, f"P2: ✅ {roll} runs")
        if st.session_state.runs_p2 > st.session_state.runs_p1 or st.session_state.wickets_p2 >= 10:
            st.session_state.game_over = True

# --- 2. INITIALIZE SESSION STATE ---
if 'runs_p1' not in st.session_state:
    st.session_state.runs_p1 = 0
    st.session_state.wickets_p1 = 0
    st.session_state.balls_p1 = 0
    st.session_state.runs_p2 = 0
    st.session_state.wickets_p2 = 0
    st.session_state.balls_p2 = 0
    st.session_state.current_player = 1
    st.session_state.game_over = False
    st.session_state.balls = 0
    st.session_state.overs = ""
    st.session_state.history = []

# --- 3. LOGIC BLOCK (MUST COME BEFORE DISPLAY) ---
if not st.session_state.game_over:
    if st.button(f'Next Ball (Player {st.session_state.current_player})', use_container_width=True, type="primary"):
        play_turn()
        # This update happens BEFORE the code continues to the metrics below
else:
    if st.session_state.runs_p2 > st.session_state.runs_p1:
        st.success(f"🏆 Player 2 Wins!")
    elif st.session_state.runs_p1 > st.session_state.runs_p2:
        st.success(f"🏆 Player 1 Wins!")
    else:
        st.info("🤝 Draw!")

# --- 4. DISPLAY BLOCK ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.subheader("Player 1")
    st.metric("Runs", st.session_state.runs_p1)
    st.caption(f"Wickets: {st.session_state.wickets_p1}")

with c2:
    st.subheader("Player 2")
    st.metric("Runs", st.session_state.runs_p2)
    st.caption(f"Wickets: {st.session_state.wickets_p2}")

st.write("Over: {st.session_state.overs}")

# Display Roll History
# History and Reset
st.write("### Match History")
for log in st.session_state.history[:6]:
    st.text(log)

if st.button('Reset Match'):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
