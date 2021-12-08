import streamlit as st
import numpy as np

from code.trajectory import get_trajectory, fig_from_list, check_solution

# Gravity constants by planet
GRAVITY_DICT = {'Earth': 9.8, 'Moon': 1.6, 'Mars': 3.7, 'Jupiter': 24.8}

# Setup the session_state variables
if "remaining_guesses" not in st.session_state:
    st.session_state["remaining_guesses"] = 3

if "trayectory_list" not in st.session_state:
    st.session_state["trayectory_list"] = []

if "game_gravity_index" not in st.session_state:
    st.session_state["game_gravity_index"] = np.random.randint(0, len(GRAVITY_DICT))
planet_list = list(GRAVITY_DICT.keys())
game_planet = planet_list[st.session_state["game_gravity_index"]]
game_gravity = GRAVITY_DICT[game_planet]

if "solution" not in st.session_state:
    v0_sol = np.random.randint(30, 60)
    print(v0_sol)
    theta_deg_sol = 45
    theta_rad_sol = np.radians(theta_deg_sol)
    t_max_sol = 2*v0_sol*np.sin(theta_rad_sol)/game_gravity
    x_max_sol = 2*v0_sol*np.cos(theta_rad_sol)*t_max_sol
    pig_position = [x_max_sol, 0]
    st.session_state["solution"] = {
                                    "pig_position":pig_position, 
                                    "v0_sol": v0_sol, 
                                    "theta_deg_sol": theta_deg_sol,
                                    }

# Fill up the page
st.title("The Game")
st.subheader(f"Can you hit the target on planet {game_planet}?")
# Pig position
x_text = f"x = {st.session_state.solution['pig_position'][0]:.3f} meters"
y_text = f"y = {st.session_state.solution['pig_position'][1]:.3f} and meters"
st.write(f"The target is at {x_text} and {y_text}")
# Remaining guesses
text = f"You have {st.session_state['remaining_guesses']} guesses remaining."
st.write(text)
# Get the parameters
st.subheader("Enter the parameters")
c1, c2, c3 = st.columns(3)
dv0 = 1
v0 = c1.slider("Initial Velocity [meters/second]", 
                        min_value=dv0, max_value=100*dv0, 
                        value=50, step=dv0, help="Initial velocity for the projectile")
dtheta = 1
theta_deg = c2.slider("Initial Angle [degrees]", 
                        min_value=5, max_value=90, 
                        value=30, step=5, help="Initial velocity for the projectile")
# options for gravity: earth, moon, mars, jupiter
c3.metric(value=game_gravity, label=f"{game_planet}'s gravity in m/s^2")

# Shoooooot
st.subheader("Hit the pig!")
c1, c2 = st.columns([.5, .1])
if st.session_state["remaining_guesses"] > 0:
    if c1.button("Shoot!"):
        st.session_state["remaining_guesses"] -= 1
        theta_rad = theta_deg * np.pi / 180
        traj_dict = get_trajectory(v0, theta_rad, game_gravity, game_planet)
        st.session_state["trayectory_list"].append(traj_dict)

# Always plot, to show the target
fig = fig_from_list(st.session_state["trayectory_list"], st.session_state.solution["pig_position"])
st.pyplot(fig)

# We check if we hit the pig after the shoot we have guesses left
if check_solution(st.session_state.solution["pig_position"], st.session_state["trayectory_list"]):
    st.success("You hit the pig!")
elif st.session_state["remaining_guesses"] == 0:
    st.error("You're out of guesses! :(")
    v0_sol = st.session_state.solution["v0_sol"]
    theta_deg_sol = st.session_state.solution["theta_deg_sol"]
    st.write(f"One possible solution was $v_0$={v0_sol} [m/s^2] and $\\theta$={theta_deg_sol} [deg]")
else:
    # Say to keep trying, but only if at least tried once
    if len(st.session_state["trayectory_list"]) > 0:
        st.warning("Keep trying!")