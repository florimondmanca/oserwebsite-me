# Database schema specification
---
OSER internal website

## Logical model

- A tutoree is a high school student signed up for the OSER tutoring program. A tutoree has a first name, a last name, a birthday, an email address, a phone number, an address, a high school and a grade and is a member of a tutoring group.
- A tutor is a member of OSER that gives tutoring classes. A tutor has a first name, a last name, a birthday, an email address, a phone number, an address and is a member of a tutoring group.
- A tutoring group is a set of tutoree and tutors. A tutoring group meets in a high school.
- A tutoring class is a temporal instance of a tutoring group, i.e. an event when tutorees and tutors meet to perform several activities together. A tutoring class is specific to a tutoring group, has a date and takes place in a high school.
- An address is represented by two lines (typically describing the street and house number), a city, a post code and a country.
- A grade is a combination of a year (Seconde, Première, Terminale) with a curriculum (S, ES, L, Pro, ...).
- Users of the internal website can login with an email address and a password. Users of the internal website are tutorees and tutors.

## Physical model

Below are defined the tables of the OSER website database and their respective attributes.

### Tutoree

- id : Integer [PK]
- first_name : VarChar(100)
- last_name : VarChar(100)
- birthday : Date
- email : VarChar(100)
- phone : VarChar(50)
- password : VarChar(50)
- id_address : Integer [FK]
- id_high_school : Integer [FK]
- id_grade : Integer [FK]
- id_tutoring_group : Integer [FK]

### Tutor

- id : Integer [PK]
- first_name : VarChar(100)
- last_name : VarChar(100)
- birthday : Date
- email : VarChar(100)
- phone : VarChar(50)
- password : VarChar(50)
- id_address : Integer [FK]

### HighSchool

- id : Integer [PK]
- name : VarChar(100)
- id_address : Integer [FK]

### Address

- id : Integer [PK]
- line1 : VarChar(200)
- line2 : VarChar(200)
- city : VarChar(100)
- post_code : VarChar(20)
- id_country : Integer [FK]
- id_owner : Integer [FK]

### Country

- id : Integer [PK]
- name : VarChar(100)

### Grade

- id : Integer [PK]
- id_year : Integer [FK]
- id_curriculum : Integer [FK]

### Year

- id : Integer [PK]
- name : VarChar(20)

### Curriculum

- id : Integer [PK]
- name : VarChar(10)
