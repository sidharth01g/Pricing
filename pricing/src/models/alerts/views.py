from flask import Blueprint, session, render_template
from pricing.src.models.alerts.alert import Alert

alert_blueprint = Blueprint(name='alerts', import_name=__name__)


@alert_blueprint.route('/')
def index():
    email = session['email']
    if email is not None:
        alerts = Alert.find_by_email(email=email)
        return render_template('alerts/alerts.html', alerts=alerts)

    return render_template('alerts/message.html')


@alert_blueprint.route('/new', methods=['POST'])
def create_alert():
    pass


@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id: str):
    pass


@alert_blueprint.route('/<string:alert_id>')
def get_alert_page(alert_id: str):
    alert = Alert.find_one_by_id(_id=alert_id)
    return render_template('alerts/alert.html', alert=alert)


@alert_blueprint.route('/alerts_for_user/<string:user_id>')
def get_alerts_for_user(user_id: str):
    pass
