import streamlit as st

def calculate_savings(price, months):
    return price / months


# Page title and description
st.title("Budget Helper for Your Goals")
st.write("""
This tool helps you plan how to save for your financial goals like a car, house, electronics, or anything else. 
Simply input the price of the item you want to purchase and the duration you want to achieve it within. 
The tool will calculate how much you need to save per month to reach your goal!
""")

# User Inputs Section
st.subheader("Enter Your Information")

# User's financial details
salary = st.number_input("Your Monthly Salary (INR)", min_value=0, step=100, format="%d")
current_savings = st.number_input("Current Savings (INR)", min_value=0, step=100, format="%d")

# Goal details
goal_item = st.text_input("What are you saving for? (e.g., Car, House, Electronics)")
price = st.number_input(f"Price of {goal_item} (INR)", min_value=0, step=100, format="%d")

# Time frame for goal
goal_duration = st.number_input("How many months do you plan to save?", min_value=1, step=1)

# Calculate monthly savings
if price > 0 and goal_duration > 0:
    required_savings = calculate_savings(price, goal_duration)
    st.write(f"To reach your goal of {goal_item} in {goal_duration} months, you need to save **₹{required_savings:.2f}** per month.")

# Extra information
if salary > 0 and required_savings > 0:
    remaining_budget = salary - required_savings
    st.write(f"After saving for your goal, you will have **₹{remaining_budget:.2f}** remaining from your salary each month.")

# Stylish Summary Box
st.markdown("""
    <style>
        .stMarkdown {
            padding: 20px;
            background-color: #f0f4f7;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stMarkdown h3 {
            color: #333;
        }
        .stMarkdown p {
            font-size: 18px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stMarkdown">
    <h3><b>Financial Summary</b></h3>
    <p><b>Your Monthly Salary</b>: ₹{}</p>
    <p><b>Your Current Savings</b>: ₹{}</p>
    <p><b>Your Goal Price</b>: ₹{}</p>
    <p><b>Time to Save</b>: {} months</p>
    <p><b>Amount to Save Per Month</b>: ₹{:.2f}</p>
</div>
""".format(salary, current_savings, price, goal_duration, required_savings))

