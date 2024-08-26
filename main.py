from src.App import App
from PIL import Image
import streamlit as st
import pandas as pd



st.set_page_config(
    page_title="Fibonacci Food Tour",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="expanded",
)

def main():
    st.session_state.setdefault('app_instance', App())
    #try:
    run(st.session_state.app_instance)
    #except:
    #    st.error('ERROR: The program crashed unexpectedly!')

def run(app):
    initialize_session()
    if not st.session_state.logged_in:
        display_login(app)
    else:
        display_header()
        display_body(app)
        if st.session_state.username == app.params["valid_admin_username"]:
            display_add_entry(app)
        display_sidebar(app)

def initialize_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

def display_login(app):
    if not st.session_state.logged_in:
        with st.form(key="login_form"):
            st.title("Login")
            st.session_state.username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Login"):
                if (st.session_state.username == app.params["valid_admin_username"] and password == app.params["valid_admin_password"]) or (
                    st.session_state.username == app.params["valid_guest_username"] and password == app.params["valid_guest_password"]):
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

def display_header():
    st.markdown(
        """
        <style>
        body {
            background-color: black;
            color: #33FF00;
            font-family: 'Courier New', Courier, monospace;
        }
        .stButton button {
            background-color: #333;
            color: #33FF00;
            border: 2px solid #33FF00;
        }
        .stTextInput input {
            background-color: #333;
            color: #33FF00;
            border: 2px solid #33FF00;
        }
        .stTextArea textarea {
            background-color: #333;
            color: #33FF00;
            border: 2px solid #33FF00;
        }
        .css-18e3th9 {
            color: #33FF00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🍴 Fibonacci Food Tour 🍜")
    st.write("This scoreboard showcases some of the finest dining experiences, with ratings meticulously calibrated by skilled professionals to ensure immaculate precision.\n")
    pad(1)

def display_body(app):
    st.write("### Score Board")
    st.session_state.container_body = st.container()
    st.session_state.body_df = st.session_state.container_body.dataframe(app.data, hide_index=True, use_container_width=True)
    pad(2)

def display_add_entry(app):
    st.write("### Add an Entry")
    with st.form("add_row_form"):
        restaurant = st.text_input("Restaurant")
        style = st.text_input("Style")
        date = st.date_input("Date")
        rating1 = st.number_input("Jerrito", min_value=1.0, max_value=10.0, step=0.1, format="%0.1f")
        rating2 = st.number_input("Krillito", min_value=1.0, max_value=10.0, step=0.1, format="%0.1f")
        rating3 = st.number_input("Karlos", min_value=1.0, max_value=10.0, step=0.1, format="%0.1f")
        guest_rating = st.number_input("Special Guest", min_value=1.0, max_value=10.0, value=None, step=0.1, format="%0.1f")
        guest_name = st.text_input("Guest Name", value=None)
        submitted = st.form_submit_button("Add Entry")

        if submitted:
            if restaurant and style and date and rating1 and rating2 and rating3:
                # Add new row to Google Sheets
                new_row = pd.DataFrame({
                'Date': [date.strftime("%y/%m/%d")],
                'Restaurant': [restaurant],
                'Style': [style],
                'Jerrito': [rating1],
                'Krillito': [rating2],
                'Karlos': [rating3],
                'Average' : [(rating1 + rating2 + rating3 + guest_rating) / 4 if guest_rating else (rating1 + rating2 + rating3) / 3],
                'Special Guest' : [guest_rating],
                'Guest Name' : [guest_name]
                })
                list_data = new_row.values.flatten().tolist()
                app.score_board.append_row(list_data)
                app.data = pd.concat([app.data, new_row.fillna("")], ignore_index=True)
                st.success("New entry added successfully!")
                st.session_state.body_df.empty()
                st.session_state.body_df = st.session_state.container_body.dataframe(app.data, hide_index=True, use_container_width=True)
            else:
                st.warning("Please fill in the required fields before submitting.")

def display_sidebar(app):
    image = Image.open('dat/img.jfif')
    st.sidebar.image(image)
    if st.session_state.username == app.params["valid_admin_username"]:
        st.sidebar.write("### Received Suggestions")
        st.sidebar.dataframe(app.suggestion_data, hide_index=True, use_container_width=True)
    else:
        st.sidebar.write("### Have any suggestions for restaurants? Let us know!")
        suggestion = st.sidebar.text_area("Your suggestion:", height=100)

        if st.sidebar.button("Submit"):
            if suggestion:
                # Write the new suggestion to Google Sheets
                app.suggestions.append_row([suggestion])
                new_suggestion_row = pd.DataFrame({"Suggestions": [suggestion]})
                app.suggestion_data = pd.concat([app.suggestion_data, new_suggestion_row.fillna("")], ignore_index=True)
                st.sidebar.success("Thank you for your suggestion!")
            else:
                st.sidebar.warning("Please enter a suggestion before submitting.")

    pad(padding=5, sidebar=True)
    display_logout()

def display_logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

def pad(padding=3, sidebar=False):
    for _ in range(padding):
        if sidebar:
            st.sidebar.text("")
        else:
            st.text("")



# Run the app
if __name__ == '__main__':
    main()
