from flask import Flask, render_template, request, redirect, url_for, session
from forms import *
from Users import *
import shelve

app = Flask(__name__)
app.secret_key = "email"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUp(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('users.db', 'c')
        try:
            if "Users" in db:  # is key exist?
                user_dict = db["Users"]  # retrieve data
            else:
                db["Users"] = user_dict  # start with empty
        except:
            print("Error in opening users.db.")
        new_user = Users(name=form.name.data, email=form.email.data.lower(), password=form.password.data)
        user_dict[f"{new_user.get_email()}"] = new_user
        db["Users"] = user_dict
        db.close()

        return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('users.db', 'c')
        try:
            if "Users" in db:  # is key exist?
                user_dict = db["Users"]  # retrieve data
            else:
                db["Users"] = user_dict  # start with empty
        except:
            print("Error in opening users.db.")
        db.close()
        if form.email.data in user_dict:
            if form.password.data == user_dict[form.email.data].get_password():
                session["user"] = form.email.data
                return redirect(url_for('profile'))
            else:
                print('Incorrect password, please try again.')
        else:
            print("There is no such email registered with us.")

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    user_dict = {}
    db = shelve.open('users.db', 'c')
    try:
        if "Users" in db:  # is key exist?
            user_dict = db["Users"]  # retrieve data
        else:
            db["Users"] = user_dict  # start with empty
    except:
        print("Error in opening users.db.")
    db.close()
    if "user" in session:
        user_email = session["user"]
        user = user_dict[user_email]
        return render_template('profile.html', user=user)
    return render_template('failure.html')

if __name__ == '__main__':
    app.run()