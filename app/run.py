from flask import Flask, redirect, url_for, render_template, request, session, flash
from database import db, GeneralUser, UserType

app = Flask(__name__)

app.secret_key = 'thisBeMySecretKeyYungBlud' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///general_user.db'
db.init_app(app)

@app.route("/")
def home():
    if session.pop("delete_user_flag", False):
        # Clear the entire session to log the user out
        session.clear()
        # Redirect to the home page after deletion
        return redirect(url_for("home"))

    return render_template("index.html")

def get_admin_users():
    # Query the database to retrieve admin users
    admin_users = GeneralUser.query.filter_by(user_type=UserType.ADMIN).all()
    
    # Create a list of dictionaries containing user_id and name
    admin_user_list = [{"user_id": user.user_id, "name": user.name} for user in admin_users]

    return admin_user_list

def get_student_users():
    # Query the database to retrieve admin users
    student_users = GeneralUser.query.filter_by(user_type=UserType.GENERAL_USER).all()
    
    # Create a list of dictionaries containing user_id and name
    student_user_list = [{"user_id": user.user_id, "name": user.name} for user in student_users]

    return student_user_list


def get_librarian_users():
    librarian_users = GeneralUser.query.filter_by(user_type=UserType.LIBRARIAN).all()
    librarian_user_list = [{"user_id": user.user_id, "name": user.name} for user in librarian_users]
    return librarian_user_list


@app.route("/delete_admin_user", methods=["POST"])
def delete_admin_user():
    if request.method == "POST":
        # Get the user_id from the form
        entered_user_id = request.form["user_id_hidden_admin"]
        entered_password = request.form["deletePassword"]

        # Perform deletion logic for admin users
        admin_user = GeneralUser.query.filter_by(user_id=entered_user_id, user_type=UserType.ADMIN).first()

        if admin_user and admin_user.check_password(entered_password):
            # Check if the admin being deleted is the currently logged-in user
            if "user" in session and session["user"] == entered_user_id:
                # Set a flag in the session indicating that the user is being deleted
                session["delete_user_flag"] = True

            # Delete the admin user
            db.session.delete(admin_user)
            db.session.commit()
            flash(f"Admin user with ID {entered_user_id} has been deleted.", "success")
        else:
            flash("Invalid credentials. Admin user deletion failed.", "error")

    # Redirect to the admin base page after deletion or on GET request
    return redirect(url_for("admin_home_admin"))

@app.route("/delete_student_user_admin", methods=["POST"])
def delete_student_user_admin():
    if request.method == "POST":
        # Get the user_id from the form
        entered_user_id = request.form["user_id_hidden_stu"]
        entered_password = request.form["deletePassword"]

        print(f"Entered User ID: {entered_user_id}")
        print(f"Entered Password: {entered_password}")

        # Perform deletion logic for student users
        student_user = GeneralUser.query.filter_by(user_id=entered_user_id, user_type=UserType.GENERAL_USER).first()

        if student_user and student_user.check_password(entered_password):
            db.session.delete(student_user)
            db.session.commit()
            flash(f"Student user with ID {entered_user_id} has been deleted.", "success")
        else:
            flash("Invalid credentials. Student user deletion failed.", "error")

    # Redirect to the admin base page after deletion or on GET request
    return redirect(url_for("admin_home_admin"))

@app.route("/delete_librarian_user_admin", methods=["POST"])
def delete_librarian_user_admin():
    if request.method == "POST":
        print(request.form)
        # Get the user_id from the form
        entered_user_id = request.form["user_id_hidden_lib"]
        entered_password = request.form["deletePassword"]

        # Perform deletion logic for librarian users
        librarian_user = GeneralUser.query.filter_by(user_id=entered_user_id, user_type=UserType.LIBRARIAN).first()

        if librarian_user and librarian_user.check_password(entered_password):
            db.session.delete(librarian_user)
            db.session.commit()
            flash(f"Librarian user with ID {entered_user_id} has been deleted.", "success")
        else:
            flash("Invalid credentials. Librarian user deletion failed.", "error")

    # Redirect to the admin base page after deletion or on GET request
    return redirect(url_for("admin_home_admin"))

@app.route("/delete_student_user_librarian", methods=["POST"])
def delete_student_user_librarian():
    if request.method == "POST":
        # Get the user_id from the form
        entered_user_id = request.form["user_id_hidden_stu"]
        entered_password = request.form["deletePassword"]

        print(f"Entered User ID: {entered_user_id}")
        print(f"Entered Password: {entered_password}")

        # Perform deletion logic for student users
        student_user = GeneralUser.query.filter_by(user_id=entered_user_id, user_type=UserType.GENERAL_USER).first()

        if student_user and student_user.check_password(entered_password):
            db.session.delete(student_user)
            db.session.commit()
            flash(f"Student user with ID {entered_user_id} has been deleted.", "success")
        else:
            flash("Invalid credentials. Student user deletion failed.", "error")

    # Redirect to the admin base page after deletion or on GET request
    return redirect(url_for("librarian_home"))

@app.route("/delete_librarian_user_librarian", methods=["POST"])
def delete_librarian_user_librarian():
    if request.method == "POST":
        # Get the user_id from the form
        entered_user_id = request.form["user_id_hidden_lib"]
        entered_password = request.form["deletePassword"]

        # Perform deletion logic for librarian users
        librarian_user = GeneralUser.query.filter_by(user_id=entered_user_id, user_type=UserType.LIBRARIAN).first()

        if librarian_user and librarian_user.check_password(entered_password):
            # Check if the librarian being deleted is the currently logged-in user
            if "user" in session and session["user"] == entered_user_id:
                # Clear the session to log the user out
                session.clear()
                # Redirect to the home page after deletion
                return redirect(url_for("home"))

            # Delete the librarian user
            db.session.delete(librarian_user)
            db.session.commit()
            flash(f"Librarian user with ID {entered_user_id} has been deleted.", "success")
        else:
            flash("Invalid credentials. Librarian user deletion failed.", "error")

    # Redirect to the librarian home page after deletion or on GET request
    return redirect(url_for("librarian_home"))

@app.route("/admin_home_admin")
def admin_home_admin():
    librarian_users = get_librarian_users()
    admin_users = get_admin_users()
    student_users = get_student_users()
    return render_template("admin_home.html", admin_users=admin_users, librarian_users=librarian_users, student_users=student_users)

@app.route("/librarian_home")
def librarian_home():
    librarian_users = get_librarian_users()
    student_users = get_student_users()
    return render_template("librarian_home.html", librarian_users=librarian_users, student_users=student_users)

@app.route("/logout")
def logout():
    session.pop("user", None)  # Clear the user session
    return render_template("base.html")

from flask import flash, redirect, url_for

@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        user_id_admin = request.form["user_id_admin"]
        password = request.form["password"]

        # Check if the provided credentials are correct
        admin_user = GeneralUser.query.filter_by(user_id=user_id_admin, user_type=UserType.ADMIN).first()

        if admin_user and admin_user.check_password(password):
            session.permanent = True
            session["user"] = user_id_admin

            # Redirect to admin_home_admin if login is successful
            return redirect("/admin_home_admin")
        else:
            # Invalid credentials
            return render_template("admin_login.html", error="Invalid credentials")
    else:
        if "user" in session:
            # Get the list of admin users
            admin_users = get_admin_users()

            return render_template("admin_base.html", admin_users=admin_users)  # Redirect to admin_base if already logged in

        return render_template("admin_login.html")


@app.route("/admin_reg", methods=["POST", "GET"])
def admin_reg():
    if request.method == "POST":
        user_id_admin = request.form["user_id_admin"]
        name = request.form["name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Perform registration logic
        if len(user_id_admin) != 9:
            return render_template("admin_reg.html", error="User ID must be 9 digits")

        if password != confirm_password:
            return render_template("admin_reg.html", error="Passwords do not match")

        # Check if user_id_admin is already taken
        existing_user = GeneralUser.query.filter_by(user_id=user_id_admin).first()
        if existing_user:
            return render_template("admin_reg.html", error="User ID already taken")

        # Create a new admin user
        admin_user = GeneralUser(name=name, user_id=user_id_admin, password=password, user_type=UserType.ADMIN)
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()

        return render_template("admin_reg.html", success="Admin user has been added and can be used to login")
    
    else:

        return render_template("admin_reg.html")

@app.route("/librarian_login", methods=["POST", "GET"])
def librarian_login():
    if request.method == "POST":
        user_id_librarian = request.form["user_id_librarian"]
        password = request.form["password"]

        # Check if the provided credentials are correct
        librarian_user = GeneralUser.query.filter_by(user_id=user_id_librarian, user_type=UserType.LIBRARIAN).first()

        if librarian_user and librarian_user.check_password(password):
            session.permanent = True
            session["user"] = user_id_librarian

            # Redirect to admin_home_admin if login is successful
            return redirect("/librarian_home")
        else:
            # Invalid credentials
            return render_template("librarian_login.html", error="Invalid credentials")
    else:
        if "user" in session:
            # Get the list of admin users
            librarian_users = get_librarian_users()

            return render_template("librarian_base.html", librarian_users=librarian_users)  # Redirect to admin_base if already logged in

        return render_template("librarian_login.html")
    
@app.route("/student_login", methods=["POST", "GET"])
def student_login():
    if request.method == "POST":
        user_id_student = request.form["user_id_stu"]
        password = request.form["password"]

        # Check if the provided credentials are correct
        student_user = GeneralUser.query.filter_by(user_id=user_id_student, user_type=UserType.GENERAL_USER).first()

        if student_user and student_user.check_password(password):
            session.permanent = True
            session["user"] = user_id_student
            return render_template("student_base.html")
        else:
            # Invalid credentials, you might want to show an error message
            return render_template("student_login.html", error="Invalid credentials")
    else:
        if "user" in session:
            return render_template("student_base.html")  # Redirect to student_base if already logged in

        return render_template("student_login.html")

@app.route("/student_registration", methods=["POST", "GET"])
def student_registration():
    if request.method == "POST":
        user_id_stu = request.form["user_id_stu"]
        name = request.form["name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Perform registration logic
        if len(user_id_stu) != 9:
            return render_template("student_registration.html", error="User ID must be 9 digits")

        if password != confirm_password:
            return render_template("student_registration.html", error="Passwords do not match")

        # Check if user_id_stu is already taken
        existing_user = GeneralUser.query.filter_by(user_id=user_id_stu).first()
        if existing_user:
            return render_template("student_registration.html", error="User ID already taken")

        # Create a new student user
        student_user = GeneralUser(name=name, user_id=user_id_stu, password=password, user_type=UserType.GENERAL_USER)
        student_user.set_password(password)
        db.session.add(student_user)
        db.session.commit()

        session.permanent = True
        session["user"] = user_id_stu
        return redirect(url_for("student_base"))
    else:
        if "user" in session:
            # Check if the user in session is a student
            user_id_in_session = session["user"]
            user_in_session = GeneralUser.query.filter_by(user_id=user_id_in_session).first()

            if user_in_session.user_type == UserType.GENERAL_USER:
                # If student is in session, redirect to student_base
                return redirect(url_for("student_base"))
        
        # If no user is in session or if the user in session is not a student, render the registration page
        return render_template("student_registration.html")

@app.route("/student_registration_lib", methods=["POST", "GET"])
def student_registration_lib():
    if request.method == "POST":
        name = request.form["name"]
        user_id_stu = request.form["user_id_stu"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Perform registration logic
        if len(user_id_stu) != 9:
            return render_template("student_registration_lib.html", error="Student UserID must be 9 digits")

        if password != confirm_password:
            return render_template("student_registration_lib.html", error="Passwords do not match")

        # Check if user_id_stu is already taken
        existing_user = GeneralUser.query.filter_by(user_id=user_id_stu).first()
        if existing_user:
            return render_template("student_registration_lib.html", error="Student UserID already taken")

        # Create a new student user
        student_user = GeneralUser(name=name, user_id=user_id_stu, password=password, user_type=UserType.GENERAL_USER)
        student_user.set_password(password)
        db.session.add(student_user)
        db.session.commit()


        return render_template("student_registration_lib.html", success="Student user has been added and can be used to login")
    else:
        if "user" in session:
            # Check if the user in session is a librarian
            user_id_in_session = session["user"]
            user_in_session = GeneralUser.query.filter_by(user_id=user_id_in_session).first()

            if user_in_session.user_type == UserType.LIBRARIAN:
                # If librarian is in session, render the registration page
                return render_template("student_registration_lib.html")
        
        # If no user is in session or if the user in session is not a librarian, render the registration page
        return render_template("student_registration.html")
    
@app.route("/student_registration_admin", methods=["POST", "GET"])
def student_registration_admin():
    if request.method == "POST":
        name = request.form["name"]
        user_id_stu = request.form["user_id_stu"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Perform registration logic
        if len(user_id_stu) != 9:
            return render_template("student_registration_admin.html", error="Student UserID must be 9 digits")

        if password != confirm_password:
            return render_template("student_registration_admin.html", error="Passwords do not match")

        # Check if user_id_stu is already taken
        existing_user = GeneralUser.query.filter_by(user_id=user_id_stu).first()
        if existing_user:
            return render_template("student_registration_admin.html", error="Student UserID already taken")

        # Create a new student user
        student_user = GeneralUser(name=name, user_id=user_id_stu, password=password, user_type=UserType.GENERAL_USER)
        student_user.set_password(password)
        db.session.add(student_user)
        db.session.commit()


        return render_template("student_registration_admin.html", success="Student user has been added and can be used to login")
    else:

        return render_template("student_registration_admin.html")
    
@app.route("/librarian_registration", methods=["POST", "GET"])
def librarian_registration():
    if request.method == "POST":
        name = request.form["name"]
        user_id_lib = request.form["user_id_lib"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Perform registration logic
        if len(user_id_lib) != 9:
            return render_template("librarian_registration.html", error="Librarian UserID must be 9 digits")

        if password != confirm_password:
            return render_template("librarian_registration.html", error="Passwords do not match")

        # Check if user_id_lib is already taken
        existing_user = GeneralUser.query.filter_by(user_id=user_id_lib).first()
        if existing_user:
            return render_template("librarian_registration.html", error="Librarian UserID already taken")

        # Create a new librarian user
        librarian_user = GeneralUser(name=name, user_id=user_id_lib, password=password, user_type=UserType.LIBRARIAN)
        librarian_user.set_password(password)
        db.session.add(librarian_user)
        db.session.commit()

        return render_template("librarian_registration.html", success="Librarian user has been added and can be used to login")
    else:

        return render_template("librarian_registration.html")

@app.route("/librarian_registration_lib", methods=["POST", "GET"])
def librarian_registration_lib():
    if request.method == "POST":
        name = request.form["name"]
        user_id_lib = request.form["user_id_lib"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Perform registration logic
        if len(user_id_lib) != 9:
            return render_template("librarian_registration_lib.html", error="Librarian UserID must be 9 digits")

        if password != confirm_password:
            return render_template("librarian_registration_lib.html", error="Passwords do not match")

        # Check if user_id_lib is already taken
        existing_user = GeneralUser.query.filter_by(user_id=user_id_lib).first()
        if existing_user:
            return render_template("librarian_registration_lib.html", error="Librarian UserID already taken")

        # Create a new librarian user
        librarian_user = GeneralUser(name=name, user_id=user_id_lib, password=password, user_type=UserType.LIBRARIAN)
        librarian_user.set_password(password)
        db.session.add(librarian_user)
        db.session.commit()


        return render_template("librarian_registration_lib.html", success="Librarian user has been added and can be used to login")
    else:
        if "user" in session:
            # Check if the user in session is a librarian
            user_id_in_session = session["user"]
            user_in_session = GeneralUser.query.filter_by(user_id=user_id_in_session).first()

            if user_in_session.user_type == UserType.LIBRARIAN:
                # If librarian is in session, render the registration page
                return render_template("librarian_registration_lib.html")
        
        # If no user is in session or if the user in session is not a librarian, render the registration page
        return render_template("librarian_registration_lib.html")

@app.route("/librarian_base")
def librarian_base():
    return render_template("librarian_base.html")

@app.route("/user")
def user():
    if "user" in session:
        user_id = session["user"]
        user = GeneralUser.query.filter_by(user_id=user_id).first()

        if user.user_type == UserType.STUDENT:
            return redirect(url_for("student_base"))
        elif user.user_type == UserType.LIBRARIAN:
            return redirect(url_for("librarian_base"))
        elif user.user_type == UserType.ADMIN:
            return redirect(url_for("admin_base"))
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run(debug=False)