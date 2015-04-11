import datetime

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_user, logout_user, \
    login_required, current_user

from project import db, bcrypt, login_manager
from project.models import User
from .decorators import check_confirmed
from .email import send_email
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ResetPasswordForm
from .token import generate_confirmation_token, confirm_token


user_blueprint = Blueprint('user', __name__,)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data,
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for(
            'user.confirm_email', token=token, _external=True)
        html = render_template('user/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("user.unconfirmed"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.index'))


@user_blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_confirmation_token(user.email)
            reset_url = url_for(
                'user.confirm_password', token=token, _external=True)
            html = render_template(
                'user/password_reset_email.html', reset_url=reset_url)
            subject = "Request to change password"
            send_email(user.email, subject, html)
            flash('A password reset link has been sent via email.', 'success')
            return redirect(url_for("main.index"))
        else:
            flash('No account matches that email.', 'danger')
            return redirect(url_for("user.reset_password"))
    return render_template('user/password_reset.html', form=form)


@user_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def confirm_password(token):
    try:
        email = confirm_token(token)
    except:
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect(url_for('user.change_password'))


@user_blueprint.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.index')
    flash('Please confirm your account!', 'warning')
    return render_template('user/unconfirmed.html')


@user_blueprint.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('user/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('user.unconfirmed'))


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
@check_confirmed
def profile():
    return render_template('user/profile.html')


@user_blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
@check_confirmed
def change_password():
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password successfully changed.', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Password change was unsuccessful.', 'danger')
            return redirect(url_for('user.change_password'))
    return render_template('user/password_change.html', form=form)
