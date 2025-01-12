from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import SignUp, Login
from Users import Users
import shelve

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('users.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening users.db.")

        new_user = Users(
            name=form.name.data,
            email=form.email.data.lower(),
            password=form.password.data,
            security_question_1=form.security_question_1.data,
            security_question_2=form.security_question_2.data
        )
        user_dict[new_user.get_email()] = new_user
        db["Users"] = user_dict
        db.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('users.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening users.db.")
        db.close()
        if form.email.data in user_dict:
            if form.password.data == user_dict[form.email.data].get_password():
                session["user"] = form.email.data
                return redirect(url_for('profile'))
            else:
                flash('Incorrect password, please try again.')
        else:
            flash("There is no such email registered with us.")

    return render_template('login.html', form=form)


@app.route('/security_questions', methods=['GET', 'POST'])
def security_questions():
    return render_template('security_questions.html')


@app.route('/verify_security_questions', methods=['POST'])
def verify_security_questions():
    email = request.form['email']
    user_dict = {}
    db = shelve.open('users.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
    except:
        print("Error in opening users.db.")
    db.close()

    if email in user_dict:
        user = user_dict[email]
        session['email'] = email
        return render_template('verify_security_questions.html', user=user)
    else:
        flash('Email not found. Please try again.', 'danger')
        return redirect(url_for('security_questions'))


@app.route('/check_security_answers', methods=['POST'])
def check_security_answers():
    answer1 = request.form['security_question_1']
    answer2 = request.form['security_question_2']
    email = session.get('email')

    user_dict = {}
    db = shelve.open('users.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
    except:
        print("Error in opening users.db.")
    db.close()

    if email in user_dict:
        user = user_dict[email]
        if user.get_security_question_1() == answer1 and user.get_security_question_2() == answer2:
            flash('Security questions answered correctly. Please change your password.', 'success')
            return redirect(url_for('change_password'))
        else:
            flash('Incorrect answers. Please try again.', 'danger')
            return redirect(url_for('security_questions'))
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('security_questions'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            user_dict = {}
            db = shelve.open('users.db', 'c')
            try:
                if "Users" in db:
                    user_dict = db["Users"]
            except:
                print("Error in opening users.db.")

            email = session.get('email')
            if email in user_dict:
                user = user_dict[email]
                user._Users__password = new_password
                db["Users"] = user_dict
                db.close()

                flash('Password changed successfully!', 'success')
                return redirect(url_for('login'))
            else:
                flash('User not found.', 'danger')
        else:
            flash('Passwords do not match. Please try again.', 'danger')

    return render_template('change_password.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    user_dict = {}
    db = shelve.open('users.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
        else:
            db["Users"] = user_dict
    except:
        print("Error in opening users.db.")
    db.close()
    if "user" in session:
        user_email = session["user"]
        user = user_dict[user_email]
        return render_template('profile.html', user=user)
    return render_template('failure.html')


if __name__ == '__main__':
    app.run(debug=True)