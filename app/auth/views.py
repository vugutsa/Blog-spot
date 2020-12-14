from . import auth
from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user,logout_user,login_required
from ..models import User,Writer
from .forms import LoginForm,RegistrationForm,WriterLoginForm
from .. import db
from ..request import get_quote
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    
    quote = get_quote()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
        return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or Password')
    title = "idea Application login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/login/writer',methods=['GET','POST'])
def writer_login():
    quote = get_quote()
    login_form = WriterLoginForm()
    if login_form.validate_on_submit():
        writer = Writer.query.filter_by(writer_email = login_form.writer_email.data).first()
        if writer is not None and writer.verify_password(login_form.password.data):
            login_user(writer,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "Idea"
    return render_template('auth/writer_login.html',login_form = login_form,title=title, quote=quote)

@auth.route('/register',methods = ["GET","POST"])
def register():
    
    quote = get_quote()
    form = RegistrationForm()
    if form.validate_on_submit():
        print('password', form.password.data)
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        
        mail_message("Welcome to idea Application","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
    
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)
@auth.route('/register/writer',methods = ["GET","POST"])
def writer_register():
    quote = get_quote()
    form = WriterRegistrationForm()
    if form.validate_on_submit():
        writer = Writer(writer_email = form.writer_email.data, writer_name = form.writer_name.data,password = form.writer_password.data)
        db.session.add(writer)
        db.session.commit()

        mail_message("Welcome to Joseph Shitandi idea website as a writer","email/welcome_user",writer.writer_email,writer=writer)

        return redirect(url_for('auth.writer_login'))
        title = "New Account"
    return render_template('auth/writer_register.html',registration_form = form, quote=quote)

@auth.route('/logout')
@login_required
def logout():
    
    quote = get_quote()
    logout_user()
    
    flash('You have been successfully logged out')
    
    return redirect(url_for("main.index"))