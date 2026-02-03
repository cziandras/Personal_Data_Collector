import streamlit as st
import pandas as pd
import data_connection as dc
import matplotlib.pyplot as plt

st.set_page_config(page_title="List data", layout="centered")
st.title("Stored personal data")

#visszalink a fő oldalra
st.page_link("data_push.py", label="Back")


# Egyszerű jelszavas védelem az oldalhoz
PASSWORD = "admin"             # st.secrets["ADMIN_PASSWORD"]

# Ellenőrizzük, hogy van-e már hitelesítési állapot a session-ben
# Ha nincs, alapértelmezetten False-ra állítjuk
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Ha a felhasználó még nincs bejelentkezve
if not st.session_state["authenticated"]:
    # Jelszó bekérése (rejtett mező)
    password = st.text_input("Password", type="password")

    # Bejelentkezés gomb
    if st.button("Login"):
        # Ha a megadott jelszó helyes
        if password == PASSWORD:
            # Elmentjük a session_state-be, hogy hitelesítve van
            st.session_state["authenticated"] = True
            # Oldal újratöltése, hogy megjelenjen a védett tartalom
            st.rerun()
        else:
            st.error("Wrong password")

    # Amíg nincs bejelentkezve, az oldal további része nem fut le
    st.stop()

#refresh
if st.button("Refresh"):
    st.rerun()


data = dc.return_data()
df = pd.DataFrame(
    data,
    columns=[
        "id","first_name","middle_name","last_name","date_of_birth","gender","phone_number","email",
        "address_line_1","address_line_2","city","state","zip_code","country",
        "highest_level_of_education","institution","year_of_graduation",
        "current_employment_status","current_job_title","company"
    ]
)


st.dataframe(df, use_container_width=True,height=600)
st.subheader("Gender distribution")

gender_counts = df["gender"].fillna("Unknown").value_counts()

fig, ax = plt.subplots()
ax.pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")

st.pyplot(fig)
st.subheader("Delete record")

person_id_to_delete = st.number_input(
    "Personal ID to delete",
    min_value=1,
    step=1
)

if st.button("Delete"):
    dc.delete(person_id_to_delete)  
    st.success("Record deleted")
st.rerun()

