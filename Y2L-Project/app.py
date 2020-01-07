from flask import Flask, request, redirect, url_for, render_template, session
from databases import *
import json, requests

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"


##### Code here ######

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', loggedin=False)
    else:
        username = request.form['username']
        password = request.form['password']
        user = query_by_username(username)
        if password != user.password:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('home'))

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/user_creation', methods=['POST'])
def user_creation():
    user = request.form['username']
    pw = request.form['password']
    pw_confirm = request.form['confirm']
    if not pw == pw_confirm:
        return redirect(url_for('register'))
    else:
        add_user(user,pw)
        return redirect(url_for('login'))

#####################


if __name__ == '__main__':
    app.run(debug=True)
