from functools import wraps
from flask import session, redirect, url_for, request, render_template
import pricing


def requires_login(func: 'function') -> 'function':
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'email' not in session or session['email'] is None:
            # Redirect to login page and upon login, redirect to the requested page (next=request.path)
            return redirect(location=url_for(endpoint='users.login_user', next=request.path))

        return func(*args, **kwargs)

    return wrapper


def requires_admin(func: 'function') -> 'function':
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'email' not in session or session['email'] is None:
            # Redirect to login page and upon login, redirect to the requested page (next=request.path)
            return redirect(location=url_for(endpoint='users.login_user', next=request.path))
        if session['email'] not in pricing.configuration['admins']:
            message = 'You do not have access to this resource'
            return render_template('show_message.html', message=message)

        return func(*args, **kwargs)

    return wrapper
