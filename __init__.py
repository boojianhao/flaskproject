from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import SignUp, Login
from customer import Users
from admin import Admin
from driver import Driver
import shelve

app = Flask(__name__)
app.secret_key = "your_secret_key"

admin_email = "admin@admin.com"
admin_password = "adminpassword"
admin_user = Admin(
    email=admin_email,
    password=admin_password,
    name="Admin",
    security_question_1="badminton",
    security_question_2="brown"
)

def ensure_admin_account():
    db = shelve.open('users.db', 'c')
    user_dict = db.get("Users", {})

    if admin_email not in user_dict:
        user_dict[admin_email] = admin_user
        db["Users"] = user_dict
        print("Admin account created and saved to the database.")
    db.close()


# Ensure the admin account is created when the application starts
ensure_admin_account()


@app.route('/')
def home():
    return render_template("home.html")


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
        user_dict[f"{new_user.get_email()}"] = new_user
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
            user = user_dict[form.email.data]
            if not user.is_active():
                flash('This account has been deactivated.', 'danger')
                return redirect(url_for('login'))
            if form.password.data == user.get_password():
                session["user"] = form.email.data
                if user.is_admin():
                    session["role"] = 'admin'
                    return redirect(url_for('admin_dashboard'))
                elif user.is_driver():
                    session["role"] = 'driver'
                    return redirect(url_for('driver_dashboard'))
                else:
                    session["role"] = 'user'
                    return redirect(url_for('profile'))
            else:
                flash('Incorrect password, please try again.')
        else:
            flash("There is no such email registered with us.")

    return render_template('login.html', form=form)

@app.route('/driver', methods=['GET'])
def driver_dashboard():
    if session.get("role") != 'driver':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    user_dict = {}
    db = shelve.open('users.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
    except:
        print("Error in opening users.db.")
    db.close()

    user_email = session.get("user")
    user = user_dict.get(user_email)

    return render_template('driver_dashboard.html', user=user)


@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    user_dict = {}
    db = shelve.open('users.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
    except:
        print("Error in opening users.db.")
    db.close()

    return render_template('admin_dashboard.html', users=user_dict)


@app.route('/create_driver', methods=['GET', 'POST'])
def create_driver():
    if session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

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
        new_driver = Driver(
            email=form.email.data.lower(),
            password=form.password.data,
            name=form.name.data,
            security_question_1=form.security_question_1.data,
            security_question_2=form.security_question_2.data
        )
        user_dict[f"{new_driver.get_email()}"] = new_driver
        db["Users"] = user_dict
        db.close()

        flash('Driver account created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template("driver_signup.html", form=form)


@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

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
        new_admin = Admin(
            email=form.email.data.lower(),
            password=form.password.data,
            name=form.name.data,
            security_question_1=form.security_question_1.data,
            security_question_2=form.security_question_2.data
        )
        user_dict[f"{new_admin.get_email()}"] = new_admin
        db["Users"] = user_dict
        db.close()

        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template("admin_signup.html", form=form)


@app.route('/edit_user/<email>', methods=['GET', 'POST'])
def edit_user(email):
    if session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

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
        return redirect(url_for('admin_dashboard'))

    user = user_dict.get(email)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        user._Users__name = request.form['name']
        user._Users__email = request.form['email']
        user._Users__password = request.form['password']
        db["Users"] = user_dict
        db.close()
        flash('User information updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    db.close()
    return render_template('edit_user.html', user=user)


@app.route('/delete_user/<email>', methods=['POST'])
def delete_user(email):
    if session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

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
        return redirect(url_for('admin_dashboard'))

    if email in user_dict:
        del user_dict[email]
        db["Users"] = user_dict
        db.close()
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('admin_dashboard'))


@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("role", None)
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
        if session["role"] == 'driver':
            return render_template('driver_profile.html', user=user)
        return render_template('profile.html', user=user)
    return render_template('failure.html')


@app.route('/verify_security_questions', methods=['POST'])
def verify_security_questions():
    email = request.form['email']
    user_dict = {}
    try:
        db = shelve.open('users.db', 'c')
        if "Users" in db:
            user_dict = db["Users"]
        db.close()
    except Exception as e:
        flash('Error accessing the database. Please try again later.', 'danger')
        return redirect(url_for('security_questions'))

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
    try:
        db = shelve.open('users.db', 'c')
        if "Users" in db:
            user_dict = db["Users"]
        db.close()
    except Exception as e:
        flash('Error accessing the database. Please try again later.', 'danger')
        return redirect(url_for('security_questions'))

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


@app.route('/security_questions', methods=['GET', 'POST'])
def security_questions():
    return render_template('security_questions.html')


@app.route('/deactivate', methods=['POST'])
def deactivate():
    if "user" in session:
        user_email = session["user"]
        user_dict = {}
        db = shelve.open('users.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening users.db.")

        if user_email in user_dict:
            user = user_dict[user_email]
            user.deactivate()
            db["Users"] = user_dict
            db.close()
            session.pop("user", None)
            flash('Account deactivated successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('User not found.', 'danger')
            db.close()
    else:
        flash('No user is logged in.', 'danger')

    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(debug=True)