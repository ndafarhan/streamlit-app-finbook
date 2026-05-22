import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Finbook App",
    page_icon="✨",
    initial_sidebar_state="collapsed",
)

# Define app pages
root_dir = Path(__file__).parent
print(f"Root directory: {root_dir}")
landing_page = st.Page(str(root_dir / "app" / "landing.py"), title="Landing", icon=":material/lock_outline:")
app_page = st.Page(str(root_dir / "app" / "app.py"), title="Home", icon=":material/home:")
venue_page = st.Page(str(root_dir / "app" / "venue.py"), title="Venue", icon=":material/location_on:")
admin_email = st.secrets["admin_email"]
allowed_emails = st.secrets["allowed_emails"]

# Check login status from session state
is_logged_in = st.session_state.get("logged_in", False)
user_email = st.session_state.get("user_email", None)

if not is_logged_in:
    pg = st.navigation(
        [landing_page],
        position="hidden",
    )
elif user_email and user_email not in allowed_emails and user_email != admin_email:
    st.warning("You are not authorized to access this app. Please contact the administrator.")
    pg = st.navigation(
        [landing_page],
        position="hidden",
    )
else:
    pg = st.navigation(
        [app_page, venue_page],
        position="sidebar",
    )

# Head to first page of navigation
pg.run()