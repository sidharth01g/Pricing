from flask import Blueprint, request, session, url_for, redirect, render_template
from pricing.src.models.users.user import User
import pricing
from pricing.src.common.logging_base import Logging
import pricing.src.models.users.errors as user_errors

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])
user_blueprint = Blueprint(name='users', import_name=__name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    logger.debug('Received HTTP request to user login endpoint with method "{}"'.format(request.method))
    if request.method == 'POST':
        email = request.form['email']
        password_hashed = request.form['password_hashed']
        try:
            if User.is_login_valid(email=email, password_hashed=password_hashed, configuration=pricing.configuration):
                session['email'] = email
                return redirect(location=url_for(endpoint='.user_alerts'))
        except user_errors.UserError as e:
            # return render_template('users/login.html', message='Invalid credentials. Please try again')
            return e.message

    elif request.method == 'GET':
        return render_template('users/login.html')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    logger.debug('Received HTTP request to user registration endpoint with method "{}"'.format(request.method))
    if request.method == 'POST':
        email = request.form['email']
        password_hashed = request.form['password_hashed']
        try:
            if User.register_user(email=email, password_hashed=password_hashed) is True:
                session['email'] = email
                return redirect(location=url_for(endpoint='.user_alerts'))
            else:
                pass
        except user_errors.UserError as e:
            return e.message

    elif request.method == 'GET':
        pass


@user_blueprint.route('/alerts')
def user_alerts():
    return "This is the user alerts page"


@user_blueprint.route('/logout')
def logout_user():
    pass


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id: str):
    print(user_id)
    pass
