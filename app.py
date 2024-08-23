import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials



# Set up the 90s hacker theme using Streamlit's theme options
st.set_page_config(
    page_title="Freedom Food Tour",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Load Google Sheets credentials from the Streamlit secrets
creds_dict = {
    "type": st.secrets["google_sheets"]["type"],
    "project_id": st.secrets["google_sheets"]["project_id"],
    "private_key_id": st.secrets["google_sheets"]["private_key_id"],
    "private_key": st.secrets["google_sheets"]["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["google_sheets"]["client_email"],
    "client_id": st.secrets["google_sheets"]["client_id"],
    "auth_uri": st.secrets["google_sheets"]["auth_uri"],
    "token_uri": st.secrets["google_sheets"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google_sheets"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google_sheets"]["client_x509_cert_url"],
}

# Convert the dictionary to a JSON string and then to credentials object
creds = Credentials.from_service_account_info(creds_dict)

# Authorize the client
CLIENT = gspread.authorize(creds)

# Google Sheets setup (when autorizing from local configuration .json file)
#SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#CREDS = Credentials.from_service_account_file("dat/google_sheets_credentials.json", scopes=SCOPE)
#CLIENT = gspread.authorize(CREDS)

# Open your Google Sheet by name
SHEET_NAME = "FreedomFoodTourData"
sheet = CLIENT.open(SHEET_NAME).sheet1

# Fetch the data from Google Sheets
data = sheet.get_all_records()

df = pd.DataFrame(data)

# Custom CSS for 90s hacker theme
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

# Display the title
st.title("🍴 Freedom Food Tour 🍜")

# Display the sortable table
st.write("### Score Board")
st.dataframe(df)

# Suggestion box for user input
st.write("### Have any suggestions or feedback? Let us know!")
suggestion = st.text_area("Your suggestion:", height=100)
if st.button("Submit"):
    if suggestion:
        # Write the new suggestion to Google Sheets
        #sheet.append_row([suggestion])
        st.success("Thank you for your suggestion!")
    else:
        st.warning("Please enter a suggestion before submitting.")

# Display some additional information
st.write("### Additional Information")
st.write("This table lists some of the finest restaurants catering to the hacker community. Whether you're in the mood for debugging your hunger or scripting a perfect meal, these restaurants have got you covered.")

# Display stored suggestions
st.write("### Previous Suggestions")
suggestions = sheet.col_values(1)  # Fetch the suggestions from the first column
for s in suggestions:
    st.write(f"- {s}")
