from flask import Flask, request, redirect, url_for, render_template, session
from databases import *
import json, requests

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"


##### Code here ######

@app.route("/")
def home():
    response = requests.get('http://jservice.io/api/random')
    info = json.loads(response.content)[0]
    question = info["question"]
    category = info["category"]["title"]
    answer = info["answer"]
    session['answer'] = answer
    value = info['value']
    if 'username' in session:
        user = query_by_username(session['username'])
        return render_template('home.html', question=question, category=category, value=value, loggedin='username' in session, username=session['username'], score=user.score)
    else:
        return render_template('home.html', question=question, category=category, value=value, loggedin=False)

@app.route('/check', methods=["POST"])
def check():
    resp = request.form["input"]
    answer = session['answer']
    if resp.lower() == answer.lower() and 'username' in session:
        user = query_by_username(session['username'])
        print(user.score + int(request.form['points']))
        update_score(session['username'], user.score + int(request.form['points']))
    session.pop('answer', None)
    return redirect(url_for('home'))

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
            session["username"] = username
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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

#####################


if __name__ == '__main__':
    app.run(debug=True)
