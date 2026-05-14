import streamlit as st

st.title("FinBook - Financial Book")

# Form login dengan email dan password
with st.form("login_form"):
    email = st.text_input(
        "Email",
        key="email",
        placeholder="Masukkan email Anda"
    )
    password = st.text_input(
        "Password",
        key="password",
        type="password",
        placeholder="Masukkan password Anda"
    )
    
    submitted = st.form_submit_button(
        ":material/lock_outline: Login",
        type="primary",
        use_container_width=True
    )
    
    if submitted:
        if email and password:
            if password == st.secrets["login_password"]:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"Login berhasil dengan email: {email}")
                st.switch_page("app/app.py")
            else:
                st.error("Password salah")
        else:
            st.error("Email dan password tidak boleh kosong")
