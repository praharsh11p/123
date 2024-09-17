from flask import Flask, redirect,url_for,render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key ="hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html",values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        found_user = users.query.filter_by(name=user).all()
        if found_user:
            session["email"]=found_user.email
        
        else:
            usr = users(user,"")
            db.session.add(usr)
            db.session.commit()

        flash("Login Seccuessful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        
        return render_template("login.html")
    
# @app.route("/delete/<name>")
# def delete(name):
    # found_user = users.query.filter_by(name=name).first()
    # if found_user:
        # db.session.delete(found_user)
        # db.session.commit()
        # flash(f"User '{name}' has been deleted!","info")
    # else:
        # flash(f"User '{name}' not found","error")
    
@app.route("/user",methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"]=email
            found_user = users.query.filter_by(name=user).first()
            found_user.email=email
            db.session.commit()
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html",email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    flash(f"You have been logged out!","info")
    session.pop("user",None)
    session.pop("email",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



# @app.route("/<name>")
# def user(name):
    # return f"Hello {name}!"
# @app.route("/admin")
# def admin():
    # return redirect(url_for("user" , name="Admin!"))    