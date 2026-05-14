import streamlit as st
from loguru import logger

st.set_page_config(
    page_title="Finbook App",
    page_icon="✨",
    initial_sidebar_state="collapsed",
)

# Define app pages
landing_page = st.Page("./app/landing.py", title="Landing", icon=":material/lock_outline:")
# app_page = st.Page("./app/app.py", title="Home", icon=":material/home:")
venue_page = st.Page("./app/venue.py", title="Venue", icon=":material/location_on:")
admin_email = st.secrets["admin_email"]
allowed_emails = st.secrets["allowed_emails"]

# Enables switch_page behaviour
try:
    is_logged_in = bool(st.user.email)
except (AttributeError, KeyError):
    is_logged_in = False

if not is_logged_in:
    logger.info("User is not logged in, showing landing page")
    pg = st.navigation(
        [landing_page],
        position="hidden",
    )
elif st.user.email not in allowed_emails and st.user.email != admin_email:
    logger.warning(f"User {st.user.email} is not allowed to access the app, showing landing page")
    st.warning("You are not authorized to access this app. Please contact the administrator.")
    pg = st.navigation(
        [landing_page],
        position="hidden",
    )
else:
    logger.info(f"User {st.user.email} is logged in, showing app pages")
    pg = st.navigation(
        # [app_page, venue_page],
        [venue_page],
        position="sidebar",
    )

# Head to first page of navigation
pg.run()