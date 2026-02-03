import data_connection as dc
import streamlit as st
import pandas as pd
from datetime import date
from countries import country_list
import re

st.set_page_config(page_title="Personal Data Collector")
st.title('Personal Data Collector')
st.subheader('Please complete the questionnaire below!')
st.caption("* Fields marked with * are required")


with st.form("personal_data_form"):

#personal
    first_name = st.text_input('First Name *', key="first_name")
    middle_name = st.text_input('Middle Name (Optional)')
    last_name = st.text_input('Last Name *', key="last_name")
    date_of_birth = st.date_input('Date of Birth',min_value=date(1900, 1, 1),max_value=date.today())
    gender = st.radio(label='Gender',options=['Female','Male','Other'])
    phone_number = st.text_input('Phone Number: "0612 345 6789"')
    email = st.text_input('Email *', key="email") 
#email ellenorzes
    #a kotelezo karakterek és formátum megadása van legalább egy karakter az @ előtt van @ van . nincs szoköz
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    email_ok = True

    if email:
        if not re.match(email_pattern, email):
            st.warning("Invalid email format")
            email_ok = False

#address
    address_line_1 = st.text_input('Address *', key="address")
    address_line_2 = st.text_input('Address (Optional)')
    city = st.text_input('City *', key="city")
    state = st.text_input ('State / Province')
    zip_code = st.text_input ('Postal Code')
    country = st.selectbox (label='Country', options=country_list())

#education

    highest_level_of_education = st.selectbox (label='Highest Education', options=['Highschool',"Bacherol's",'Master','PhD','Postgradue','No education','other'])
    institution = st.text_input('Institute')
    year_of_graduation = st.selectbox(label='Graduation Year', options=list(range(date.today().year, 1949, -1)))

#employment

    current_employment_status = st.selectbox(label='Current Employment Status',options=['Employed','Unemployed','Student','Other'])
    current_job_title = st.text_input('Current Position')
    company = st.text_input('Company')
    
    submitted = st.form_submit_button(
    "Submit / Save",
    disabled=not st.session_state.get("consent", False)
)
# Kötelező mezők ellenőrzése mentés előtt ( akkor is ha ujrafrissul az oldal mert a memoriabol olvassuk ki az adatot)
# ( ez a session_state)
required_ok = (
    st.session_state.get("first_name", "") != "" and
    st.session_state.get("last_name", "") != "" and
    st.session_state.get("email", "") != "" and
    st.session_state.get("address", "") != "" and
    st.session_state.get("city", "") != "" and
    email_ok
)   

# ha a mentés gombra kattint, de nem minden kötelező mező van kitöltve
if submitted and not required_ok:
    st.error("Please complete all required fields (*) and enter a valid email address.")
# ha minden ok, mentjük az adatokat ( Personal id egy egyedi azonosito szam)szoval personal id = azt jelenti 1 = 
if submitted and required_ok: 
        personal_id = dc.insert_personal(first_name, middle_name, last_name, date_of_birth, gender, phone_number, email)
        dc.insert_address(personal_id, address_line_1, address_line_2, city, state, zip_code, country)
        dc.insert_education(personal_id, highest_level_of_education, institution, year_of_graduation)
        dc.insert_employment(personal_id, current_employment_status, current_job_title, company)

        st.success("Data saved")
        st.rerun()


# A checkbox a formon kívül van,mert így kattintáskor az oldal frissul,
# és a Submit gomb állapota frissülni fog
consent = st.checkbox("I consent to storing my personal data", key="consent")
#Data list page linkelese
st.page_link("pages/01_List_data.py", label="Data List")








