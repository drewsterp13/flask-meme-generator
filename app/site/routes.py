from flask import Blueprint, render_template

site = Blueprint("site", __name__, template_folder="site_templates")

@site.route("/")
def welcome():
    return render_template("welcome.html")

@site.route("/home")
def home():
    return render_template("home.html")

@site.route("/profile")
def profile():
    return render_template("profile.html")

@site.route("/logoff")
def logoff():
    return render_template("logged_out.html")