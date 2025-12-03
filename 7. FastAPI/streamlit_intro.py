import streamlit as st
import pandas as pd
import requests


# st.title("st.title()")

# st.subheader("st.subheader()")

# st.text("st.text()")

# st.write("st.write(" ")")

# chai = st.selectbox("Your favourite Chai: ", ["Masala Chai", "Lemon Tea", "Adrak Chai", "Kesar Chai"])
# st.write(f"Your Choose {chai}")
# st.success("Your chai has been Brewed!")

# ------------------------------------

# st.title("Chai Maker App")

# if st.button("Make Chai"):
#     st.success("Your Chai is Brewed.")

# add_masala = st.checkbox("Add Masala")

# if add_masala:
#     st.write("Masala added to your chai!")

# tea_type = st.radio("Pick your chai base: ", ["Milk", "Water", "Almond Milk"])

# st.write(f"Selected base {tea_type}")
# flavour = st.selectbox("Choose Flavor", ["Adrak", "Kesar", "Tulsi"])

# sugar = st.slider("Sugar level (spoon)", 0,5,2)
# st.write(f'selected sugar level {sugar}')

# cups = st.number_input("How many cups", min_value=1, max_value=10, step=1)
# st.write(f"Selected sugar level {cups}")

# name = st.text_input("Enter your name")
# if name:
#     st.write(f"You name is {name}")

# dob = st.date_input("Select your date of birth")
# st.write(dob)

# ------------------------------------

# st.title("Chai Taste Poll")

# col_1, col_2 = st.columns(2)

# with col_1:
#     st.header("Masala Chai")
#     st.image("url", width=200)
#     vote_1 = st.button("Vote", key="vote_1")

# with col_2:
#     st.header("Addrak Chai")
#     st.image("url", width=200)
#     vote_2 = st.button("Vote", key="vote_2")

# if vote_1:
#     st.success("Thanks for voting Masala Chai")
# elif vote_2:
#     st.success("Thanks for voting Adrak Chai")

# name = st.sidebar.selectbox("Choose your chai", ["Masala", "Kesar", "Adrak"])
# st.sidebar.write(f"Welcome {name} and your chai will be ready")

# with st.expander("Show Chai Making Instructions"):
#     st.write("""
#         1. Boil water with tea leaves
#         2. Add milk with and spices
#         3. Serve hot
# """)

# st.markdown('### Welcome to Chai app')
# st.markdown('> Blockquote')

# ------------------------------------

# st.title("Chai Sales Dashboard")

# file = st.file_uploader("Upload your csv file", type=["csv"])

# if file:
#     df = pd.read_csv(file)
#     st.subheader("Data Preview")
#     st.dataframe(df)

# if file:
#     st.subheader("Summary States")
#     st.write(df.describe())

# if file:
#     cities = df["City"].unique()
#     selected_city = st.selectbox("Filter by cities", cities)
#     filtered_data = df[df["City"] == selected_city]
#     st.dataframe(filtered_data)

# ------------------------------------

# st.title("Live Currency Converter")
# amount = st.number_input("Enter the amount INR", min_value=1)
# currency = st.selectbox("Covert to ", ["USD", "EUR", "GBP", "JPY"])
# if st.button("Convert"):
#     url = "https://api.exchangerate-api.com/v4/latest/INR"
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()
#         rate = data['rates'][currency]
#         converted = rate * amount
#         st.success(f"{amount} INR = {converted: .2f} {currency}")
#     else: 
#         st.error("Failed to fetch conversion rate.")
