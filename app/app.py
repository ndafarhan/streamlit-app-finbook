import streamlit as st
from src.google_spreadsheet import GoogleSpreadsheet
import pandas as pd

import plotly.express as px
from PIL import Image
import requests

gsheet = GoogleSpreadsheet()
trx_spreadsheet_name = st.secrets["transaction_spreadsheet_name"] 
trx_data = gsheet.read_data(trx_spreadsheet_name)
budget_spreadsheet_name = st.secrets["budget_spreadsheet_name"]
budget_data = gsheet.read_data(budget_spreadsheet_name)
mission_spreadsheet_name = st.secrets["mission_spreadsheet_name"]
mission_data = gsheet.read_data(mission_spreadsheet_name)

trx_df = pd.DataFrame(trx_data[1:], columns=trx_data[0]) if trx_data else pd.DataFrame()
budget_df = pd.DataFrame(budget_data[1:], columns=budget_data[0]) if budget_data else pd.DataFrame()
mission_df = pd.DataFrame(mission_data[1:], columns=mission_data[0]) if mission_data else pd.DataFrame()

st.title("👰🏻‍♀️🤵🏻‍♂️ Welcome Bride & Groom")
st.write("This is Finbook App, your financial companion to help you manage your wedding budget and track your expenses. Let's make your special day financially stress-free and memorable! 🎉💍")

with st.sidebar:
    # Show user email from session state
    user_email = st.session_state.get("user_email", "User")
    st.write(f"👤 {user_email}")
    
    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.rerun()


budget_df["Amount"] = pd.to_numeric(budget_df["Amount"], errors='coerce')
not_yet_ammount = budget_df["Amount"].sum()
trx_df["Amount"] = pd.to_numeric(trx_df["Amount"], errors='coerce')
done_ammount = trx_df["Amount"].sum()
# Create a DataFrame for the pie chart
pie_chart_data = pd.DataFrame(data=[["Done", done_ammount], ["Not Yet", not_yet_ammount]], columns=["Status", "Amount"])

## Merge detailed_budget_df with agg_detailed_trx_df
agg_trx_df = trx_df.groupby(["Category", "Name"], as_index=False).agg({"Amount": "sum"})
detailed_budget_df = pd.merge(budget_df, agg_trx_df[["Category", "Name","Amount"]], on=["Category","Name"], how="left", suffixes=("_Budget", "_Transaction"))
## Change Amount_Transaction name to Progress
detailed_budget_df["Progress"] = detailed_budget_df["Amount_Transaction"]
detailed_budget_df["Progress"] = detailed_budget_df["Progress"].fillna(0)
detailed_budget_df["Progress"] = pd.to_numeric(detailed_budget_df["Progress"], errors='coerce')
detailed_budget_df["Progress"] = 100 * detailed_budget_df["Progress"]/detailed_budget_df["Amount_Budget"]
detailed_budget_df = detailed_budget_df.drop(columns=["Amount_Transaction"])
detailed_budget_df = detailed_budget_df.sort_values(by="Progress", ascending=False)

detailed_trx_df = trx_df.sort_values(by=["Transaction Date", "Transaction Time"], ascending=False)

mission_df["Is Done"] = mission_df["Is Done"].apply(lambda x: True if str(x).lower() == "true" else False)

# Display Columns for Budgeting Progress, Your Mission, and Summary Progress
col1, col2, col3 = st.columns(3)
with col1:
    #create pie chart
    st.subheader("Budgeting Progress")
    fig = px.pie(pie_chart_data, names="Status", values="Amount", hole=0.8, color="Status", color_discrete_map={"Done": "rgb(175,256,175)", "Not Yet": "rgb(256,200,200)"})
    fig.update_layout(legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.subheader("Wallet 💰")
    initial_amount = 124250000
    current_amount = initial_amount - done_ammount
    st.metric(label="Available Budget", value=f"Rp {current_amount:,.0f}")
# Initialize session state for mission input and missions list
if "mission_input_field" not in st.session_state:
    st.session_state.mission_input_field = ""

if "missions_list" not in st.session_state:
    # Initialize from the dataframe
    missions_data = []
    for idx, row in mission_df.iterrows():
        missions_data.append({
            "Name": row["Name"],
            "Is Done": row["Is Done"]
        })
    st.session_state.missions_list = missions_data

def add_new_mission() -> None:
    #add new mission to data
    new_mission_name = st.session_state.mission_input_field
    if new_mission_name:
        new_mission = {
            "Name": new_mission_name,
            "Is Done": False
        }
        # Add to google spreadsheet
        gsheet.add_row(mission_spreadsheet_name, [new_mission_name, False])
        # Reload mission data to session_state
        mission_data = gsheet.read_data(mission_spreadsheet_name)
        mission_df = pd.DataFrame(mission_data[1:], columns=mission_data[0]) if mission_data else pd.DataFrame()
        mission_df["Is Done"] = mission_df["Is Done"].apply(lambda x: True if str(x).lower() == "true" else False)
        missions_data = []
        for idx, row in mission_df.iterrows():
            missions_data.append({
                "Name": row["Name"],
                "Is Done": row["Is Done"]
            })
        st.session_state.missions_list = missions_data
    # Clear the input field after adding
    st.session_state.mission_input_field = ""

with col3:
    st.subheader("Your Mission 🎯")
    col3_1, col3_2 = st.columns(2)
    with col3_1:
        st.text_input("Mission Name", key="mission_input_field")
    with col3_2:
        st.button("➕ Add Mission", key="add-mission-button", on_click=add_new_mission)
    if st.session_state.missions_list:
        for idx, mission in enumerate(st.session_state.missions_list):
            st.checkbox(mission["Name"], value=mission["Is Done"], key=f"mission_checkbox_{idx}")
# with col3:
#     st.subheader("Summary Progress")
#     st.metric(label="Not Yet", value=f"Rp {not_yet_ammount:,.0f}", delta=f"Rp {not_yet_ammount:,.0f}")
    


#show data from google spreadsheet in table

# Prepare display dataframe with formatted Amount_Budget
detailed_budget_df_display = detailed_budget_df.copy()
detailed_budget_df_display["Amount_Budget"] = detailed_budget_df_display["Amount_Budget"].apply(
    lambda x: f"Rp {x:,.0f}" if pd.notna(x) else "0"
)

st.subheader("Detailed Budgeting")
st.dataframe(
    detailed_budget_df_display, 
    column_config={
        "Progress": st.column_config.ProgressColumn(
            "Progress",
            help="The percentage of the budget that has been spent",
            format="%.1f%%",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True
)

st.subheader("Detailed Transaction")
# Prepare display dataframe with formatted Amount
detailed_trx_df_display = detailed_trx_df.copy()
detailed_trx_df_display["Amount"] = detailed_trx_df_display["Amount"].apply(
    lambda x: f"Rp {x:,.0f}" if pd.notna(x) else "0"
)
st.dataframe(detailed_trx_df_display, hide_index=True)
