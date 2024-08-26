from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
import gspread



class App:
    def __init__(self):
        self.params = None
        self.scope = None
        self.creds = None
        self.client = None
        self.data = None
        self.suggestion_data = None
        self.score_board = None
        self.suggestions = None
        self.initialize()

    def initialize(self):
        self.get_data()

    def get_data(self):
        self.set_params()
        self.set_scope()
        self.set_creds()
        self.authorize_client()
        self.get_sheet_data()

    def set_params(self):
        # Load Google Sheets credentials from the Streamlit secrets
        self.params = {
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
            "universe_domain": st.secrets["google_sheets"]["universe_domain"],
            "valid_admin_username" : st.secrets["app_login"]["valid_admin_username"],
            "valid_guest_username" : st.secrets["app_login"]["valid_guest_username"],
            "valid_admin_password" : st.secrets["app_login"]["valid_admin_password"],
            "valid_guest_password" : st.secrets["app_login"]["valid_guest_password"]
        }

    def set_scope(self):
        # Define the scope
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # https://www.googleapis.com/auth/spreadsheets.readonly

    def set_creds(self):
        # Convert the dictionary to a credentials object with the scope
        self.creds = Credentials.from_service_account_info(self.params, scopes=self.scope)

    def authorize_client(self):
        # Authorize the client
        self.client = gspread.authorize(self.creds)

    def get_sheet_data(self):
        # Open Google Sheet and fetch data
        spreadsheet_name = "FreedomFoodTourData"
        try:
            spreadsheet = self.client.open(spreadsheet_name)
            self.score_board = spreadsheet.worksheet("score_board")
            self.suggestions = spreadsheet.worksheet("suggestions")
        except Exception as e:
            st.write(f"Authorization failed: {e}")

        # Fetch the data from Google Sheets
        self.data = pd.DataFrame(self.score_board.get_all_records())
        self.suggestion_data = pd.DataFrame(self.suggestions.get_all_records())
