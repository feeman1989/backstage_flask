from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_required,login_user,logout_user,current_user
from ..models import User
from .forms import LoginForm
from . import auth
@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated user are allowed!'
@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('main.index'))
    form = LoginForm()
    if  form.validate_on_submit():
        print form.username
        print 'test....'
        print form.username.data
        user = User.query.filter_by(username=form.username.data).first()
        print user
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')

    return render_template('auth/login.html',form=form)
@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


