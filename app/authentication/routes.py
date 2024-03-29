from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from models import User, db, check_password_hash
from forms import CreateNewAccount, LoginAccount

auth = Blueprint("auth", __name__, template_folder="auth_templates")

@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    form = CreateNewAccount()

    try:
        if request.method == "POST" and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            print(first_name, last_name, username, email, password)
            
            user = User(first_name, last_name, username, email, password=password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a new account. Welcome {username} to the memes :)")
            return redirect(url_for("site.welcome"))
    except:
        raise Exception("Sorry, invalid form data")
    
    return render_template("sign_up.html", form=form)

@auth.route("/signin", methods = ["GET", "POST"])
def signin():
    form = LoginAccount()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You are successfully logged in.")
                return redirect(url_for("site.home"))
            else:
                flash("Access Denied")
    except:
        raise Exception("Sorry invalid form data")
    
    return render_template("sign_in.html", form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("site.logoff"))