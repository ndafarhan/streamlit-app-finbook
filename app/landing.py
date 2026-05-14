import streamlit as st

st.title("FinBook - Financial Book")


if st.button(
    ":material/lock_outline: Sign up",
    type="primary",
    key="checkout-button",
    use_container_width=True,
):
    st.login("google")
