from google.oauth2 import service_account
import gspread
from typing import Any, List
from gspread.client import Client
import streamlit as st



SCOPES = ['https://www.googleapis.com/auth/drive'] 

gcp_credentials = {
  "type": st.secrets["gcp_credentials"]["gcp_type"],
  "project_id": st.secrets["gcp_credentials"]["project_id"],
  "private_key_id": st.secrets["gcp_credentials"]["private_key_id"],
  "private_key": st.secrets["gcp_credentials"]["private_key"],
  "client_email": st.secrets["gcp_credentials"]["client_email"],
  "client_id": st.secrets["gcp_credentials"]["gcp_client_id"],
  "auth_uri": st.secrets["gcp_credentials"]["auth_uri"],
  "token_uri": st.secrets["gcp_credentials"]["token_uri"],
  "auth_provider_x509_cert_url": st.secrets["gcp_credentials"]["auth_provider_x509_cert_url"],
  "client_x509_cert_url": st.secrets["gcp_credentials"]["client_x509_cert_url"],
  "universe_domain": st.secrets["gcp_credentials"]["universe_domain"]
}

credentials = service_account.Credentials.from_service_account_info(
    gcp_credentials, scopes=SCOPES
)

gspread_client = gspread.authorize(credentials)

class GoogleSpreadsheet:
    def __init__(self, gspread_client: Client = gspread_client):
        self.client = gspread_client

    def read_data(self, spreadsheet_name: str) -> list:
        """Read all data from the spreadsheet (including headers at row 1)."""
        data = self.client.open(spreadsheet_name).sheet1
        return data.get_all_values()

    def get_columns(self, spreadsheet_name: str) -> List[str]:
        """Get the column headers from the spreadsheet."""
        sheet = self.client.open(spreadsheet_name).sheet1
        return sheet.row_values(1)
    
    def add_row(self, spreadsheet_name: str, row_data: List[Any]) -> None:
        """Add a new row of data to the spreadsheet."""
        sheet = self.client.open(spreadsheet_name).sheet1
        # validate row_data length matches the number of columns
        columns = self.get_columns(spreadsheet_name)
        if len(row_data) != len(columns):
            raise ValueError("Row data length does not match number of columns in the spreadsheet.")
        sheet.append_row(row_data)
