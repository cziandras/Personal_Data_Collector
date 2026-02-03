CREATE TABLE personal (
    id serial primary key,
    first_name varchar(100),
    middle_name varchar(100),
    last_name varchar(100),
    date_of_birth Date,
    gender varchar(50),
    phone_number varchar (30),
    email varchar (254)
);

CREATE TABLE address (
    personal_id int references personal(id),
    address_line_1 varchar (100),
    address_line_2 varchar (100),
    city varchar (100),
    state varchar(100),
    zip_code varchar(50),
    country varchar(100)
);


CREATE TABLE education (
    personal_id int references personal(id),
    highest_level_of_education varchar(100),
    institution varchar (200),
    year_of_graduation INT
);


CREATE TABLE employment (
    personal_id int references personal(id),
    current_employment_status varchar (100),
    current_job_title varchar (100),
    company varchar(100)
);









