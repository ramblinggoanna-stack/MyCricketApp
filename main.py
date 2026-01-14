import streamlit as st
import random

# Page Config
st.set_page_config(page_title="Dice Cricket", page_icon="🏏")

st.title("🏏 Dice Cricket: 1v1 Battle")

# --- 1. SESSION STATE INITIALIZATION ---
if 'runs_p1' not in st.session_state:
    st.session_state.runs_p1 = 0
    st.session_state.wickets_p1 = 0
    st.session_state.balls_p1 = 0
    st.session_state.runs_p2 = 0
    st.session_state.wickets_p2 = 0
    st.session_state.balls_p2 = 0
    st.session_state.current_player = 1  # Track whose turn it is
    st.session_state.game_over = False
    st.session_state.history = []

# --- 2. HELPER FUNCTIONS ---
def play_turn():
    roll = check_roll(random.randint(0, 10))
    
    # Logic for Player 1
    if st.session_state.current_player == 1:
        st.session_state.balls_p1 += 1
        if roll == 5:
            st.session_state.wickets_p1 += 1
            st.session_state.history.insert(0, f"P1: ❌ OUT!")
        else:
            st.session_state.runs_p1 += roll
            st.session_state.history.insert(0, f"P1: ✅ {roll} runs")
        
        # End P1 Innings if 10 wickets down
        if st.session_state.wickets_p1 >= 10:
            st.session_state.current_player = 2
            st.session_state.history = ["--- PLAYER 2 START ---"]

    # Logic for Player 2
    else:
        st.session_state.balls_p2 += 1
        if roll == 5:
            st.session_state.wickets_p2 += 1
            st.session_state.history.insert(0, f"P2: ❌ OUT!")
        else:
            st.session_state.runs_p2 += roll
            st.session_state.history.insert(0, f"P2: ✅ {roll} runs")

        # Check Win/Loss Conditions for Player 2
        if st.session_state.runs_p2 > st.session_state.runs_p1:
            st.session_state.game_over = True
        elif st.session_state.wickets_p2 >= 10:
            st.session_state.game_over = True

def check_roll(roll):
    match roll:
        case 0 | 1: return 0
        case 2 | 3: return 1
        case 4 | 5: return 2
        case 6: return 3
        case 7: return 4
        case 8: return 6
        case 9 | 10: return 5


# --- 3. UI DISPLAY ---
# Scoreboard
c1, c2 = st.columns(2)
with c1:
    st.subheader("Player 1")
    st.metric("Runs", st.session_state.runs_p1, delta=None if st.session_state.current_player == 1 else "Innings Done")
    st.caption(f"Wickets: {st.session_state.wickets_p1}")

with c2:
    st.subheader("Player 2")
    st.metric("Runs", st.session_state.runs_p2, delta=st.session_state.runs_p2 - st.session_state.runs_p1 if st.session_state.current_player == 2 else 0)
    st.caption(f"Wickets: {st.session_state.wickets_p2}")

st.divider()

# Gameplay Controls
if not st.session_state.game_over:
    player_text = f"Player {st.session_state.current_player}'s Turn"
    if st.button(f'Next Ball ({player_text})', use_container_width=True, type="primary"):
        play_turn()
else:
    # Final Result Logic
    if st.session_state.runs_p2 > st.session_state.runs_p1:
        st.success(f"🏆 Player 2 Wins by {10 - st.session_state.wickets_p2} wickets!")
    elif st.session_state.runs_p1 > st.session_state.runs_p2:
        st.success(f"🏆 Player 1 Wins by {st.session_state.runs_p1 - st.session_state.runs_p2} runs!")
    else:
        st.info("🤝 It's a Draw!")

# History & Reset
st.write("### Match History")
for log in st.session_state.history[:6]:
    st.text(log)

if st.button('Reset Match'):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
