from app import app
from flask import render_template, url_for, flash, redirect
from app.forms import SubmissionForm
from config import Config
import requests
import json

source=''
cust_input=''
language=''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
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

    return render_template('index.html', title='USER', form=form)

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
    print(json.dumps(x,indent=4))
    print(x['compile_status'])
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
    print(json.dumps(x,indent=4))
    return render_template('run.html', result=x)
