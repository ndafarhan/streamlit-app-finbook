import streamlit as st

from PIL import Image
import requests

st.title("Venue Selection 🏟️")
if not st.user["email_verified"]:
    st.warning("Please verify your email and login back to unlock all features")

with st.sidebar:
    # Show picture from URL
    if st.user.picture:
        try:
            im = Image.open(requests.get(st.user.picture, stream=True).raw)
            st.image(im, width=50) 
            st.write(st.user.name.title())
        except Exception as e:
            st.warning("Could not load profile picture")
            st.write("🧑‍💼")  # Default avatar emoji
    else:
        st.write("🧑‍💼")  # Default avatar emoji when no picture URL
    if st.button("🔓 Logout"):
        st.logout()

# Display venue selection options
col1, col2, col3 = st.columns(3)
with col1:
    im = Image.open(requests.get("https://lh3.googleusercontent.com/gps-cs-s/APNQkAFoOos4kA2X8X_U_7Cz8ckvUSQ3WTs3-DdwNedq0njeu0O3Jqpy6SKZjjcqSP-9o6wM4DzT7X9oHjMw-RVNVflM4IB415UzUbOXClX-cZBNPb1YkqqaDVL-m9blu8siGB9UyvEVLA=s1360-w1360-h1020-rw", stream=True).raw)
    st.image(im.resize((500, 500)), width=150, caption="Masjid Jami At-Tohir, Depok [:material/location_on:](https://www.google.com/maps/dir//Masjid+Jami'+At-Thohir,+Jl.+Mochamad+Thohir,+RT.01%2FRW.12,+Tapos,+Kec.+Tapos,+Kota+Depok,+Jawa+Barat+16457/@-6.2508504,106.7352587,15z/data=!4m8!4m7!1m0!1m5!1m1!1s0x2e69eb18c904187f:0xe441b8f2eda454d9!2m2!1d106.8947814!2d-6.427274!5m1!1e1?entry=ttu&g_ep=EgoyMDI2MDQyOS4wIKXMDSoASAFQAw%3D%3D)")
with col2:
    im = Image.open(requests.get("https://lh3.googleusercontent.com/p/AF1QipM-P83Ueug9Rc-uPvhaPZmAVfhgiV4hm61IvVMQ=s1360-w1360-h1020-rw", stream=True).raw)
    st.image(im.resize((500, 500)), width=150, caption=" Felfest UI, Depok [:material/location_on:](https://www.google.com/maps/dir//Felfest+UI,+Kampus+UI,+Jl.+Prof.+DR.+Miriam+Budiardjo,+RW.3,+Srengseng+Sawah,+Kec.+Jagakarsa,+Kota+Jakarta+Selatan,+Daerah+Khusus+Ibukota+Jakarta+12640/@-6.2508504,106.7352587,15z/data=!4m8!4m7!1m0!1m5!1m1!1s0x2e69ec3a9517d101:0x895775594e85e9ac!2m2!1d106.8314729!2d-6.3507415!5m1!1e1?entry=ttu&g_ep=EgoyMDI2MDQyOS4wIKXMDSoASAFQAw%3D%3D)")