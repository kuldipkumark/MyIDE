from app import app
from flask import render_template, url_for, flash, redirect
from app.forms import SubmissionForm

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
		flash("valid one {} \n {} with {} also {}".format(form.language.data, form.source_code.data, \
			form.custom_input.data, form.custom_input_check.data))
		if form.compile_code.data:
			return redirect(url_for('compile'))
		elif form.run_code.data:
			return redirect(url_for('run'))

	return render_template('index.html', title='USER', form=form)

@app.route('/compile')
def compile():
	return render_template('compile.html')

@app.route('/run')
def run():
	return render_template('run.html')