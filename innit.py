from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import SignUp, Login, Availability
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
    address="123 Singapore Road",
    security_question_1="badminton",
    security_question_2="brown"
)

def ensure_admin_account():
    db = shelve.open('customers.db', 'c')
    user_dict = db.get("Users", {})

    if admin_email not in user_dict:
        user_dict[admin_email] = admin_user
        db["Users"] = user_dict
        print("Admin account created and saved to the database.")
    db.close()

# ensure_admin_account()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('customers.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening customers.db.")
        new_user = Users(
            name=form.name.data,
            email=form.email.data.lower(),
            address=form.address.data,
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


@app.route('/')
def home():
    if "user" in session and session["role"] == "user":
        return redirect(url_for('profile'))
    elif "user" in session and session["role"] == "admin":
        return redirect(url_for('admin_dashboard'))
    elif "user" in session and session["role"] == "driver":
        return redirect(url_for('driver_dashboard'))
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user" in session and session["role"] == "user":
        return redirect(url_for('profile'))
    elif "user" in session and session["role"] == "admin":
        return redirect(url_for('admin_dashboard'))
    elif "user" in session and session["role"] == "driver":
        return redirect(url_for('driver_dashboard'))
    form = Login(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('customers.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening customers.db.")
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

@app.route('/driver/driver_dashboard', methods=['GET'])
def driver_dashboard():
    if "user" not in session or session.get("role") != 'driver':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    user_dict = {}
    db = shelve.open('customers.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
    except:
        print("Error in opening customers.db.")
    db.close()

    user_email = session.get("user")
    user = user_dict.get(user_email)

    availability_db = shelve.open('availability.db', 'c')
    availability_dict = availability_db.get('Availability', {})
    user_availability = availability_dict.get(user_email, {})
    availability_db.close()

    return render_template('driver/driver_dashboard.html', user=user, user_availability=user_availability)


@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    user_dict = {}
    db = shelve.open('customers.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
    except:
        print("Error in opening customers.db.")
    db.close()

    return render_template('admin/admin_dashboard.html', users=user_dict)


@app.route('/create_driver', methods=['GET', 'POST'])
def create_driver():
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    form = SignUp(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('customers.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening customers.db.")
        new_driver = Driver(
            email=form.email.data.lower(),
            password=form.password.data,
            name=form.name.data,
            address=form.address.data,
            security_question_1=form.security_question_1.data,
            security_question_2=form.security_question_2.data
        )
        user_dict[f"{new_driver.get_email()}"] = new_driver
        db["Users"] = user_dict
        db.close()

        flash('Driver account created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/driver_signup.html", form=form)


@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    form = SignUp(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('customers.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening customers.db.")
        new_admin = Admin(
            email=form.email.data.lower(),
            password=form.password.data,
            name=form.name.data,
            address=form.address.data,
            security_question_1=form.security_question_1.data,
            security_question_2=form.security_question_2.data
        )
        user_dict[f"{new_admin.get_email()}"] = new_admin
        db["Users"] = user_dict
        db.close()

        flash('Admin account created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template("admin/admin_signup.html", form=form)


@app.route('/edit_user/<email>', methods=['GET', 'POST'])
def edit_user(email):
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    user_dict = {}
    db = shelve.open('customers.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
        else:
            db["Users"] = user_dict
    except:
        print("Error in opening customers.db.")
        db.close()
        return redirect(url_for('admin_dashboard'))

    user = user_dict.get(email)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        user.set_name(request.form['name'])
        user.set_email(request.form['email'])
        user.set_password(request.form['password'])
        user_dict.pop(email)
        user_dict[user.get_email()] = user
        db["Users"] = user_dict
        db.close()
        flash('User information updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    db.close()
    return render_template('admin/edit_user.html', user=user)


@app.route('/delete_user/<email>', methods=['POST'])
def delete_user(email):
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))

    user_dict = {}
    db = shelve.open('customers.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
        else:
            db["Users"] = user_dict
    except:
        print("Error in opening customers.db.")
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

@app.route('/profile')
def profile():
    if "user" not in session or session.get("role") != 'user':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))
    user_dict = {}
    db = shelve.open('customers.db', 'c')
    try:
        if "Users" in db:
            user_dict = db["Users"]
        else:
            db["Users"] = user_dict
    except:
        print("Error in opening customers.db.")
    db.close()
    user_email = session["user"]
    user = user_dict[user_email]
    return render_template('customer/profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("role", None)
    return redirect(url_for('home'))

@app.route('/security_questions', methods=['GET', 'POST'])
def security_questions():
    return render_template('security_questions.html')


@app.route('/verify_security_questions', methods=['POST'])
def verify_security_questions():
    email = request.form['email']
    user_dict = {}
    try:
        db = shelve.open('customers.db', 'c')
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
        db = shelve.open('customers.db', 'c')
        if "Users" in db:
            user_dict = db["Users"]
        db.close()
    except Exception as e:
        flash('Error accessing the database. Please try again later.', 'danger')
        return redirect(url_for('security_questions'))

    if email in user_dict:
        user = user_dict[email]
        if user.get_security_question_1() == answer1 and user.get_security_question_2() == answer2:
            session["change_password"] = True
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
    if "change_password" not in session:
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            user_dict = {}
            db = shelve.open('customers.db', 'c')
            try:
                if "Users" in db:
                    user_dict = db["Users"]
            except:
                print("Error in opening customers.db.")

            email = session.get('email')
            if email in user_dict:
                user = user_dict[email]
                user._Users__password = new_password
                db["Users"] = user_dict
                db.close()

                session.pop("change_password", None)
                flash('Password changed successfully!', 'success')
                return redirect(url_for('login'))
            else:
                flash('User not found.', 'danger')
        else:
            flash('Passwords do not match. Please try again.', 'danger')

    return render_template('change_password.html')

@app.route('/deactivate', methods=['GET', 'POST'])
def deactivate():
    if "user" in session:
        user_email = session["user"]
        user_dict = {}
        db = shelve.open('customers.db', 'c')
        try:
            if "Users" in db:
                user_dict = db["Users"]
            else:
                db["Users"] = user_dict
        except:
            print("Error in opening customers.db.")

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

    return redirect(url_for('home'))

@app.route('/manage_users')
def manage_users():
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))
    db = shelve.open('customers.db', 'r')
    user_dict = db.get('Users', {})
    db.close()
    return render_template('admin/manage_users.html', users=user_dict)

@app.route('/manage_admins')
def manage_admins():
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))
    db = shelve.open('customers.db', 'r')
    user_dict = db.get('Users', {})
    db.close()
    return render_template('admin/manage_admins.html', users=user_dict)

@app.route('/manage_drivers')
def manage_drivers():
    if "user" not in session or session.get("role") != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('home'))
    db = shelve.open('customers.db', 'r')
    user_dict = db.get('Users', {})
    db.close()
    return render_template('admin/manage_drivers.html', users=user_dict)


@app.route('/driver/availability', methods=['GET', 'POST'])
def submit_availibility():
    if 'user' not in session or session.get("role") != 'driver':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('login'))

    form = Availability(request.form)
    if request.method == 'POST' and form.validate():
        user_email = session['user']
        db = shelve.open('availability.db', 'c')
        availability_dict = db.get('Availability', {})

        availability_dict[user_email] = {
            'monday': form.monday.data,
            'tuesday': form.tuesday.data,
            'wednesday': form.wednesday.data,
            'thursday': form.thursday.data,
            'friday': form.friday.data,
            'saturday': form.saturday.data,
            'sunday': form.sunday.data
        }

        db['Availability'] = availability_dict
        db.close()

        flash('Availability updated successfully!', 'success')
        return redirect(url_for('driver_dashboard'))

    return render_template('driver/availability.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
