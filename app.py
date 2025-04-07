from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os 
from flask_bcrypt import Bcrypt  # ✅ Step 1: Import bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)  # ✅ Step 2: Initialize bcrypt

# ----------------- ROUTES ------------------

@app.route('/')
def login():
    return render_template('login.html')

@app.route("/login_validation", methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

     # Print the email and password to verify that the values are correctly passed
    print(f"Email: {email}")
    print(f"Password: {password}")

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    # Fetch the user from the database based on email
    user = cursor.execute("SELECT * FROM USERS WHERE email=?", (email,)).fetchall()
    connection.close()

    # If user exists
    if user:
        stored_hash = user[0][3]  # Assuming the password hash is in the 4th column (index 3)
        
        # Print the stored hash to the console to check if it's a bcrypt hash
        print("Stored Hash:", stored_hash)
        
        # Now check if the password matches the stored hash
        if bcrypt.check_password_hash(stored_hash, password):
            session['username'] = user[0][0]  # Storing first_name in session
            return redirect('/dashboard')
        else:
            # Password mismatch
            return redirect('/')
    else:
        # Email not found
        return redirect('/')


# @app.route("/login_validation", methods=['POST'])
# def login_validation():
#     email = request.form.get('email')  # use 'email' not 'name'
#     password = request.form.get('password')

#     connection = sqlite3.connect('LoginData.db')
#     cursor = connection.cursor()
#     cursor.execute("SELECT email, password FROM USERS")
#     users = cursor.fetchall()

#     for u in users:
#         print(u)
#      # ✅ Get the user by email only (since passwords are hashed)

#     user = cursor.execute("SELECT * FROM USERS WHERE email=?", (email,)).fetchone()
#     connection.close()

#      # ✅ Check if user exists and verify password

#     # if user and bcrypt.check_password_hash(user[3], password):
#     #     session['username'] = user[0]  # first_name
#     #     return redirect(f'/dashboard')  # ✅ Redirect to dashboard
#     # else:
#     if user:
#         stored_hash = user[3]  # index 3 = password
#         if bcrypt.check_password_hash(stored_hash, password):
#             print("Stored Hash:", stored_hash)
#             print("Password Entered:", password)

#             session['username'] = user[0]  # first_name
#             return redirect('/dashboard')
#         else:
#             return redirect('/')  # password mismatch
#     else:
#         return redirect('/')  # email not found
       

    
#     # if len(user) > 0: 
#     #     return redirect(f'/home?fname={user[0][0]}&lname={user[0][1]}&email={user[0][2]}')


#     # else:
#     #     return redirect('/')

# ----------------- REGISTER ------------------

@app.route('/register')
def register():
    return render_template('register.html')

# ----------------- HOME ------------------

@app.route('/home')
def home():
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    email = request.args.get('email')

    return render_template('home.html', fname=fname, lname=lname, email=email)


# ----------------- DASHBOARD ------------------

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return  render_template("dashboard.html", username=session['username'])
    return redirect(url_for("home"))



# add user route

@app.route('/add_user', methods=['POST'])
def add_user():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    ans = cursor.execute("SELECT * FROM USERS WHERE email=?", (email,)).fetchall()

    if len(ans) > 0:
        connection.close()
        return render_template('login.html')  # email already exists
    else:
        cursor.execute('INSERT INTO USERS(first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
                       (fname, lname, email, hashed_password))
        connection.commit()
        connection.close()
        return render_template('login.html')


# ----------------- LOGOUT ------------------

@app.route ("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# ----------------- RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)