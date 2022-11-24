from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    redirect,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_manager, UserMixin
from static.yolo_structure.Inference import Detector
from static.yolo_structure.Inference.Detector import n_times

import DB as db

app = Flask(__name__)
app.config["SECRET_KEY"] = "7a8f7359407fa2d4d7134666"


@app.route("/skin-consult")
def market():
    return render_template("skin_consult.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not db.check_document(
            str(request.form["email"]), str(request.form["password"])
        ):
            db.insert_document(
                str(request.form["name"]),
                str(request.form["email"]),
                str(request.form["password"]),
            )
            return render_template("skin_consult.html")
        else:
            return render_template("login.html", error="User Already Registered")
    else:
        return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if db.check_document(
            str(request.form["username"]), str(request.form["password"])
        ):
            return render_template("skin_consult.html")
        else:
            return render_template("login.html", error="Incorrect Username or PAssword")


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        global n_times
        n_times += 1
        print("n times", n_times)
        print(request.form)
        img = request.files["img"]
        path_save = (
            "D:\\IBM_Assignments\\PyLogin\\static\\yolo_structure\\Data\\Source_Images\\Real_Time_Images\\"
            + img.filename
        )
        path_result = (
            "D:\\IBM_Assignments\\PyLogin\\static\\yolo_structure\\Data\\Source_Images\\Real_Time_Images_Detection_Results\\"
            + img.filename
        )
        img.save(path_save)
        Detector.predict(n_times)
        original_img = (
            "./../static/yolo_structure/Data/Source_Images/Real_Time_Images/"
            + img.filename
        )
        predicted_img = (
            "./../static/yolo_structure/Data/Source_Images/Real_Time_Images_Detection_Results/"
            + img.filename
        )
        curr_img = img.filename
        print(
            "path_save",
            path_save,
            "path_res",
            path_result,
            "img_file_name",
            img.filename,
        )
        return render_template("results.html", imgs=[original_img, predicted_img])
    else:
        return render_template("results.html")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    a = 0
    app.run()
