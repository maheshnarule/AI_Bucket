# # from flask import Flask, render_template

# # # Import feature modules
# # from age_gender import register_age_gender_routes
# # from emotion import register_emotion_routes
# # from species import register_species_routes
# # from hand_gesture import register_hand_routes
# # # from plant_disease import predict_disease

# # app = Flask(__name__)

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # # Register routes
# # register_age_gender_routes(app)
# # register_emotion_routes(app)
# # register_species_routes(app)
# # register_hand_routes(app)
# # # register_plant_disease_routes(app)


# # if __name__ == "__main__":
# #     app.run(debug=True)




from flask import Flask, render_template, request, redirect, url_for, flash, session
# Import feature modules
from age_gender import register_age_gender_routes
from emotion import register_emotion_routes
from species import register_species_routes
from hand_gesture import register_hand_routes
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for sessions & flash

# ---------- DB Setup ----------
def init_sqlite_db():
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_sqlite_db()

# ---------- Routes ----------
@app.route('/')
def main():
    return render_template('main.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = c.fetchone()

        if existing_user:
            flash("Email already exists. Please login instead.", "warning")
            conn.close()
            # 🔹 Show this alert on signin page
            return redirect(url_for('signin'))
        else:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                      (name, email, password))
            conn.commit()
            conn.close()
            flash("Signup successful! Please login.", "success")
            # 🔹 After signup, go to signin and show flash
            return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("user.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            flash("Login successful!", "success")
            # 🔹 After signin, redirect to dashboard → index.html
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            # 🔹 Error also shows in index.html
            return redirect(url_for('dashboard'))

    return render_template('signin.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Pass user name + show flash in index.html
        return render_template("index.html", name=session['name'])
    else:
        flash("Please login first.", "warning")
        return redirect(url_for('signin'))


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('signin'))


# ---------- Admin ----------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Hardcoded admin check
        if email == "user-admin" and password == "123456":
            session['admin'] = True
            flash("Welcome Admin!", "success")
            # 🔹 Redirect to admin dashboard with flash
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin Credentials", "danger")
            # 🔹 Error flash also shows in admin dashboard
            return redirect(url_for('admin_dashboard'))

    return render_template("admin_login.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('signin'))

    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', users=users)


# ---------- Register Feature Routes ----------
register_age_gender_routes(app)
register_emotion_routes(app)
register_species_routes(app)
register_hand_routes(app)

if __name__ == "__main__":
    import os
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    app.run(debug=True, use_reloader=False)
