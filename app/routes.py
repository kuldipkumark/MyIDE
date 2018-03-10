from app import app, db
from flask import render_template, url_for, flash, redirect, request
from app.forms import SubmissionForm, LoginForm, RegistrationForm
from config import Config
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, SaveCode
import requests
import json

source=''
cust_input=''
language=''
temp_source_code=''
temp_language=''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    permitted_languages = [("C", "C (gcc 4.8.1)"), ("CPP", "C++ (g++ 4.8.1)"), ("CSHARP", "C#"), \
                ("CLOJURE", "Clojure (clojure 1.1.0)"), ("CSS", "CSS"), ("HASKELL", "Haskell (ghc 7.4.1)"), \
                ("JAVA", "Java (openjdk 1.7.0_09)"), ("JAVASCRIPT", "JavaScript"), ("OBJECTIVEC", "Objective-C (clang 3.3)"), \
                ("PERL", "Perl (perl 5.14.2)"), ("PHP", "PHP (php 5.3.10)"), ("PYTHON", "Python (python 2.7.3)"), \
                ("R", "R (RScript 2.14.1)"), ("RUBY", "Ruby (ruby 2.1.1)"), ("RUST", "Rust (rustc 1.4.0)"), ("SCALA", "Scala (scalac 2.9.1)")
    ]

    form = SubmissionForm()
    form.language.choices = permitted_languages

    if form.validate_on_submit():
        global source
        source = form.source_code.data
        global cust_input
        cust_input = form.custom_input.data
        global language
        language = form.language.data
        if form.compile_code.data:
            return redirect(url_for('compile'))
        elif form.run_code.data:
            return redirect(url_for('run'))
        elif form.save_code.data:
            if not (current_user.is_authenticated):
                global temp_source_code
                temp_source_code = source
                flash('You need to login first')
                return redirect(url_for('login'))
            else:
                user = User.query.filter_by(username=current_user.username).first()
                code = SaveCode(source_code=source, coder=user)
                flash('Saved')
                db.session.add(code)
                db.session.commit()

    if request.method == 'GET' and temp_source_code:
        form.source_code.data = temp_source_code
        if hasattr(current_user, 'username'):
            user = User.query.filter_by(username=current_user.username).first()
            code = SaveCode(source_code=temp_source_code, coder=user)
            db.session.add(code)
            db.session.commit()
            flash("Saved")
        temp_source_code = ''

    return render_template('index.html', form=form)

@app.route('/compile/')
def compile():
    data = {
    'client_secret': Config.CLIENT_SECRET_KEY,
    'async': 0,
    'source': source,
    'lang': language,
    'time_limit': 5,
    'memory_limit': 262144,
    }
    r = requests.post(Config.COMPILE_URL, data=data)
    x = json.loads(r.text)
    return render_template('compile.html', result=x)

@app.route('/run')
def run():
    data = {
    'client_secret': Config.CLIENT_SECRET_KEY,
    'async': 0,
    'source': source,
    'lang': language,
    'time_limit': 5,
    'memory_limit': 262144,
    }
    if cust_input:
        data['input'] = cust_input

    r = requests.post(Config.RUN_URL, data=data)
    x = json.loads(r.text)
    return render_template('run.html', result=x)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('logged out')
    global temp_source_code
    temp_source_code = ''
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a register user')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/saved')
def saved():
    user = User.query.filter_by(username=current_user.username).first()
    codes = user.save_codes.all()
    if len(codes) == 0:
        return render_template('previous_saved.html', content="")
    recent_saved = codes[-1]
    return render_template('previous_saved.html', content=recent_saved.source_code)