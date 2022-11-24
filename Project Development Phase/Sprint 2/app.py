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

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "7a8f7359407fa2d4d7134666"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password(self, user_password):
        return bcrypt.check_password_hash(self.password_hash, user_password)

    def __repr__(self) -> str:
        return f"Username {self.username} Email {self.email} password_hash {self.password_hash}"


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please Try with a different name"
            )

    def validate_username(self, email_to_check):
        email = User.query.filter_by(username=email_to_check.data).first()
        if email:
            raise ValidationError(
                "Email already exists! Please Try with a different name"
            )

    username = StringField(
        label="Username", validators=[Length(min=2, max=30), DataRequired()]
    )
    email = StringField(label="Email Address", validators=[Email()])
    password = PasswordField(
        label="Password",
        validators=[
            Length(
                min=6,
            ),
            DataRequired(),
        ],
    )
    confirm_password = PasswordField(
        label="Confirm Password", validators=[EqualTo("password"), DataRequired()]
    )
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return "Hi"
    else:
        return render_template("index.html")


@app.route("/market")
def market():
    return render_template("market.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            print(user)
            db.session.add(user)
            db.session.commit()
            return "Correct"
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(
                    f"There was an error with creating a user: {err_msg}",
                    category="danger",
                )
        return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                print("Success")
                login_user(user)
                flash(
                    f"Success ! You are logged In as : {user.username}",
                    category="sucess",
                )
                return redirect(url_for("market"))
            else:
                print("Failure")
                flash(
                    "Username or Password is incorrect Please Try Again",
                    category="danger",
                )
                return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
