from flask import render_template, request, redirect, url_for, flash
from flask_package.form import RegistrationForm, LoginForm
from datetime import datetime
from flask_package.models import User
from flask_package import app, db, bcrypt
from flask_login import login_user, logout_user, current_user
from datetime import datetime

feedback = []
def store_feedback(url):
    feedback.append(dict(
        url=url,
        user='Loonycorn',
        date= datetime.utcnow()
    ))
    
def new_feedback(num):
    return sorted(feedback, key=lambda bm:bm['date'], reverse=True)[:num]
    

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', new_feedback = new_feedback(3))

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful')
        
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/sale")
def sale():
    return render_template('sale.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
