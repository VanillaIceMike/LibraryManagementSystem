User Management System
# Overview

Welcome to the User Management System, a web application built with Flask, a micro web framework for Python. This application facilitates user registration, login, and deletion, accommodating various roles such as administrators, librarians, and general users (students).
Features

    User Roles:
        Administrators (ADMIN)
        Librarians (LIBRARIAN)
        General Users (STUDENT)

    User Actions:
        Login:
            Administrators, librarians, and students can log in using their credentials.
        Registration:
            Students can register for a new account.
            Administrators and librarians can register new users (students).

    User Deletion:
        Administrators and librarians can delete users.
        Deleting a logged-in administrator or librarian results in automatic logout.

    Session Management:
        User sessions are managed using Flask's session mechanism.

    Password Security:
        Passwords are securely hashed using the Werkzeug library.

# Project Structure

    app/:
        Main directory containing the Flask application setup and route definitions.

    app/run.py:
        Main file containing the Flask application setup and route definitions.
        Routes for home, login, registration, deletion, and user-specific home pages.

    app/database.py:
        Defines the database model (GeneralUser) using SQLAlchemy.
        Enum (UserType) for user roles (ADMIN, LIBRARIAN, GENERAL_USER).

    app/templates/:
        HTML templates for rendering different views.

Sign in as admin:
The database has one admin user available for you to use:
Admin user - UserID:000000001 - Password:adminpass

# Run the Application:

bash

    python run.py

    Access the Application:
    Open a web browser and go to http://127.0.0.1:5000/.

# Project Heriarchy:
.:
app/

./app:
__pycache__/  database.py  instance/  README.md  run.py  templates/

./app/__pycache__:
__init__.cpython-310.pyc  database.cpython-310.pyc  run.cpython-310.pyc

./app/instance:
general_user.db

./app/templates:
admin_base.html  admin_login.html  base.html   librarian_base.html  librarian_login.html         librarian_registration_lib.html  student_login.html         student_registration_admin.html
admin_home.html  admin_reg.html    index.html  librarian_home.html  librarian_registration.html  student_base.html                student_registration.html  student_registration_lib.html



Run the run.py file when stpped into Library/app and not just Library/ in your IDE!!!!!

# Dependencies

    Flask
    SQLAlchemy
    Werkzeug


# Acknowledgments

    Flask: https://flask.palletsprojects.com/
    SQLAlchemy: https://www.sqlalchemy.org/
    Werkzeug: https://werkzeug.palletsprojects.com/

