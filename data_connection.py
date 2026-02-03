import psycopg2
import streamlit as st

def get_connection():
    connection = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=st.secrets["DB_PORT"]
    )
    return connection


def insert_personal(first_name, middle_name, last_name, date_of_birth,
                    gender, phone_number, email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO personal (first_name, middle_name, last_name, date_of_birth, gender, phone_number, email) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;',
        [first_name, middle_name, last_name, date_of_birth, gender, phone_number, email]
    )
    id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    return id


def insert_address(personal_id, address_line_1, address_line_2, city, state, zip_code, country):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO address (personal_id, address_line_1, address_line_2, city, state, zip_code, country) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s);',
        [personal_id, address_line_1, address_line_2, city, state, zip_code, country]
    )
    connection.commit()
    cursor.close()
    connection.close()


def insert_education(personal_id, highest_level_of_education, institution, year_of_graduation):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO education (personal_id, highest_level_of_education, institution, year_of_graduation) '
        'VALUES (%s, %s, %s, %s);',
        [personal_id, highest_level_of_education, institution, year_of_graduation]
    )
    connection.commit()
    cursor.close()
    connection.close()


def insert_employment(personal_id, current_employment_status, current_job_title, company):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO employment (personal_id, current_employment_status, current_job_title, company) '
        'VALUES (%s, %s, %s, %s);',
        [personal_id, current_employment_status, current_job_title, company]
    )
    connection.commit()
    cursor.close()
    connection.close()


def delete(personal_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM address WHERE personal_id = %s;", (personal_id,))
    cursor.execute("DELETE FROM education WHERE personal_id = %s;", (personal_id,))
    cursor.execute("DELETE FROM employment WHERE personal_id = %s;", (personal_id,))
    cursor.execute("DELETE FROM personal WHERE id = %s;", (personal_id,))
    connection.commit()
    cursor.close()
    connection.close()


def return_data():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            personal.id,
            personal.first_name,
            personal.middle_name,
            personal.last_name,
            personal.date_of_birth,
            personal.gender,
            personal.phone_number,
            personal.email,

            address.address_line_1,
            address.address_line_2,
            address.city,
            address.state,
            address.zip_code,
            address.country,

            education.highest_level_of_education,
            education.institution,
            education.year_of_graduation,

            employment.current_employment_status,
            employment.current_job_title,
            employment.company
        FROM personal
        LEFT JOIN address ON address.personal_id = personal.id
        LEFT JOIN education ON education.personal_id = personal.id
        LEFT JOIN employment ON employment.personal_id = personal.id
        ORDER BY personal.id DESC;
    """)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
