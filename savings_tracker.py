# import streamlit as st
# import random

# def generate_savings_options():
#     """Generates random small denominations for users to check off as they save."""
#     return sorted(random.choices([10, 20, 50, 100, 200, 500], k=15))

# st.set_page_config(page_title="Smart Saving Assistant", layout="wide")

# st.title("🎯 Goal-Based Investment Planner")

# # Input field for the savings goal
# goal_amount = st.number_input("Enter your savings goal (₹):", min_value=100, step=100)

# # Store the generated savings options only once
# if 'savings_options' not in st.session_state:
#     st.session_state.savings_options = generate_savings_options()

# # Render savings grid with the denominations
# def render_savings_grid():
#     """Displays a grid of small savings denominations."""
#     savings_options = st.session_state.savings_options
#     cols = st.columns(5)
#     total_saved = 0

#     # Initialize session state for checkbox states if not already done
#     if 'checked_values' not in st.session_state:
#         st.session_state.checked_values = {i: False for i in range(len(savings_options))}

#     # Create checkboxes for each savings option
#     for i, amount in enumerate(savings_options):
#         with cols[i % 5]:
#             # Set the state of each checkbox based on session state
#             checked = st.checkbox(f"₹{amount}", key=f"save_{i}", value=st.session_state.checked_values[i])
#             if checked:
#                 total_saved += amount
#             st.session_state.checked_values[i] = checked  # Store the checkbox state in session state

#     return total_saved

# # Calculate the total saved by the user based on selected checkboxes
# total_saved = render_savings_grid()

# # Display total saved and goal
# st.markdown(f"### ✅ Total Saved: ₹{total_saved} / ₹{goal_amount}")

# # Check if the user has reached their savings goal
# if total_saved >= goal_amount:
#     st.success("Congratulations! You've reached your savings goal! 🎉")
# else:
#     st.warning("Keep saving, you're doing great! 💪")


import streamlit as st
import random

def generate_savings_options():
    """Generates random small denominations for users to check off as they save."""
    # Generate 15 random denominations from the available values
    return sorted(random.choices([10, 20, 50, 100, 200, 500], k=15))

st.set_page_config(page_title="Smart Saving Assistant", layout="wide")

st.title("🎯 Goal-Based Investment Planner")

# Input field for the savings goal
goal_amount = st.number_input("Enter your savings goal (₹):", min_value=100, step=100)

# Store the generated savings options only once in session state
if 'savings_options' not in st.session_state:
    st.session_state.savings_options = generate_savings_options()

# Render savings grid with the denominations
def render_savings_grid():
    """Displays a grid of small savings denominations."""
    savings_options = st.session_state.savings_options
    cols = st.columns(5)
    total_saved = 0

    # Initialize session state for checkbox states if not already done
    if 'checked_values' not in st.session_state:
        st.session_state.checked_values = {i: False for i in range(len(savings_options))}

    # Create checkboxes for each savings option
    for i, amount in enumerate(savings_options):
        with cols[i % 5]:
            # Set the state of each checkbox based on session state
            checked = st.checkbox(f"₹{amount}", key=f"save_{i}", value=st.session_state.checked_values[i])
            if checked:
                total_saved += amount
            st.session_state.checked_values[i] = checked  # Store the checkbox state in session state

    return total_saved

# Calculate the total saved by the user based on selected checkboxes
total_saved = render_savings_grid()

# Display total saved and goal
st.markdown(f"### ✅ Total Saved: ₹{total_saved} / ₹{goal_amount}")

# Check if the user has reached their savings goal
if total_saved >= goal_amount:
    st.success("Congratulations! You've reached your savings goal! 🎉")
else:
    st.warning("Keep saving, you're doing great! 💪")

# Debug: Show the list of denominations for the user's understanding
st.write("Denominations: ", st.session_state.savings_options)
