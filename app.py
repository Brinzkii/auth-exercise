from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hashing_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "password"

connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def red_to_reg():
    if "user" in session:
        user = session["user"]
        return redirect(f"/users/{user}")
    else:
        return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        u = User.register(username, password, first_name, last_name, email)

        db.session.add(u)
        db.session.commit()
        session["user"] = u.username

        return redirect("/secret")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)

        if user:
            session["user"] = user.username
            return redirect(f"/users/{user.username}")
    else:
        return render_template("login.html", form=form)


@app.route("/users/<username>")
def show_user(username):
    if "user" in session:
        u = User.query.filter_by(username=username).first()
        f = Feedback.query.filter_by(username=username).all()

        return render_template("user.html", u=u, f=f)
    else:
        return redirect("/")


@app.route("/users/<username>/delete", methods=["GET", "POST"])
def del_user(username):
    form = DeleteForm()

    if form.delete.data == False:
        return redirect(f"/users/{username}")

    if form.validate_on_submit():
        if "user" in session:
            u = User.query.filter_by(username=username).first()
            feedback = Feedback.query.filter_by(username=username).all()

            db.session.delete(u)
            for f in feedback:
                db.session.delete(f)
            db.session.commit()
            session.pop("user")

            return redirect("/")
        else:
            return redirect("/")
    else:
        return render_template("delete.html", form=form, u=username)


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def submit_feedback(username):
    form = FeedbackForm()
    user = User.query.filter_by(username=username).first()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user = User.query.filter_by(username=username).first()

        f = Feedback(title=title, content=content, username=user.username)
        db.session.add(f)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template("feedback.html", form=form, u=user.username)


@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def update_feedback(id):
    f = Feedback.query.filter_by(id=id).first()
    user = User.query.filter_by(username=f.username).first()
    form = FeedbackForm(obj=f)

    if form.validate_on_submit():
        f.title = form.title.data
        f.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{user.username}")
    else:
        return render_template("feedback.html", form=form, u=user.username)


@app.route("/feedback/<int:id>/delete")
def del_feedback(id):
    f = Feedback.query.filter_by(id=id).first()

    db.session.delete(f)
    db.session.commit()

    return redirect(f"/users/{f.username}")


@app.route("/secret")
def show_secrets():
    if "user" in session:
        return render_template("secret.html")
    else:
        return redirect("/")


@app.route("/logout")
def logout_user():
    session.pop("user")
    return redirect("/")
