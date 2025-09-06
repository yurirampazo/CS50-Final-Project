from datetime import datetime
from flask import flash
from flask import Flask, render_template, request, redirect, session
from flask import url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from helpers import apology, login_required
from passlib.hash import bcrypt

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///yulearn.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    routines = db.relationship("Routine", backref="user", lazy=True)
    study_logs = db.relationship("StudyLog", backref="user", lazy=True)

class Routine(db.Model):
    __tablename__ = "routine"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subjects = db.relationship("RoutineSubject", backref="routine", lazy=True)

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    estimated_study_minutes = db.Column(db.Integer)
    routine_subjects = db.relationship("RoutineSubject", backref="subject", lazy=True)
    study_logs = db.relationship("StudyLog", backref="subject", lazy=True)

class RoutineSubject(db.Model):
    __tablename__ = "routine_subject"
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey("routine.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    __table_args__ = (db.UniqueConstraint("routine_id", "subject_id", name="unique_routine_subject"),)

class StudyLog(db.Model):
    __tablename__ = "study_log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    time_spent = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String)

with app.app_context():
    db.create_all()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("layout.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("missing fields", 403)
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.verify(password, user.password):
            return apology("invalid username and/or password", 403)
        session["user_id"] = user.id
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            return apology("missing fields", 400)
        if password != confirmation:
            return apology("passwords don't match", 400)
        if User.query.filter_by(username=username).first():
            return apology("username taken", 400)
        hash_pw = bcrypt.hash(password)
        new_user = User(username=username, password=hash_pw)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return redirect("/")
    return render_template("register.html")

@app.route("/planner", methods=["GET", "POST"])
@login_required
def planner():
    USER_ID = session["user_id"]

    if request.method == "POST":
        routine_title = request.form.get("routine")

        routineObject = Routine(title=routine_title, user_id=USER_ID)
        db.session.add(routineObject)
        db.session.commit()

        subjects = request.form.getlist("subject")
        descriptions = request.form.getlist("description")

        for name, desc in zip(subjects, descriptions):
            subjectObject = Subject.query.filter_by(name=name).first()
            if not subjectObject:
                subjectObject = Subject(name=name, description=desc)
                db.session.add(subjectObject)
                db.session.commit()

            existing_link = RoutineSubject.query.filter_by(
                routine_id=routineObject.id,
                subject_id=subjectObject.id
            ).first()

            if not existing_link:
                routine_subject = RoutineSubject(
                    routine_id=routineObject.id,
                    subject_id=subjectObject.id
                )
                db.session.add(routine_subject)
                db.session.commit()

        return redirect(url_for("plan", id=routineObject.id))

    routines = Routine.query.filter_by(user_id=USER_ID).all()
    return render_template("planner.html", routines=routines)

@app.route("/plan")
@login_required
def plan():
    routine_id = request.args.get("id", type=int)
    if not routine_id:
        return apology("Missing routine ID", 400)
    routine = Routine.query.get(routine_id)
    if not routine or routine.user_id != session["user_id"]:
        return apology("Routine not found or access denied", 403)
    return render_template("plan.html", routine=routine)

@app.route("/plan/<int:routine_id>/edit", methods=["GET", "POST"])
@login_required
def edit_routine(routine_id):
    routine = Routine.query.get(routine_id)
    if not routine or routine.user_id != session["user_id"]:
        return apology("Routine not found or access denied", 403)

    if request.method == "POST":
        routine.title = request.form.get("routine_title")

        for rs in routine.subjects:
            desc = request.form.get(f"subject_desc_{rs.subject.id}")
            if desc is not None:
                rs.subject.description = desc
        
        new_subject_name = request.form.get("new_subject_name")
        new_subject_desc = request.form.get("new_subject_desc")

        if new_subject_name:
            subject = Subject.query.filter_by(name=new_subject_name).first()
            if not subject:
                subject = Subject(name=new_subject_name, description=new_subject_desc)
                db.session.add(subject)
                db.session.commit()

            link = RoutineSubject.query.filter_by(routine_id=routine.id, subject_id=subject.id).first()
            if not link:
                new_link = RoutineSubject(routine_id=routine.id, subject_id=subject.id)
                db.session.add(new_link)
        
        db.session.commit()
        flash("Routine updated successfully!", "success")
        return redirect(url_for("plan", id=routine.id))

    return render_template("edit.html", routine=routine)


@app.route("/plan/<int:routine_id>/delete", methods=["POST"])
def delete_routine(routine_id):
    
    if not routine_id:
        return apology("Missing routine ID", 400)

    routine = Routine.query.get_or_404(routine_id)

    if routine.user_id != session["user_id"]:
        return apology("Access denied", 403)

    for rs in routine.subjects:
        db.session.delete(rs)

    db.session.delete(routine)
    db.session.commit()

    return redirect("/planner")


@app.route("/progress")
def progress():
    return apology("TODO", 500)


@app.route("/profile", methods=["POST", "GET"])
def profile():
    return apology("TODO", 418)



if __name__ == "__main__":
    app.run(debug=True)
