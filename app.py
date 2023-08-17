from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from logging import DEBUG
from form import RegistrationForm, LoginForm


app = Flask(__name__)
app.secret_key = b'S\x96\xb4\x0ea\xc0\x89R'

app.logger.setLevel(DEBUG)

feedback = []

def store_feedback(url):
    feedback.append(dict(
        url=url,
        user='Loonycorn',
        date= datetime.utcnow()
    ))

@app.route('/')
@app.route('/index')
def home():
    
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        url = request.form['url']
        store_feedback(url)
        app.logger.debug('stored feedback: ' + url)
        flash("Your feedback: " + url)
        return redirect(url_for('home')) 
        
    return render_template('add.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created!')
        return redirect(url_for('login'))
    if form.errors:
        flash('Validation Errors: ' + str(form.errors))
        app.logger.error('ValidationError:\n' + str(form.errors))
        
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@loony.com' and form.password.data =='loony':
            flash('Logged in!')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful')
        
    return render_template('login.html', title='Login', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)