import pricing
from flask import Blueprint, session, render_template, request
from pricing.src.models.alerts.alert import Alert
from pricing.src.models.items.item import Item
from pricing.src.common.logging_base import Logging
from pricing.src.models.users.decorators import requires_login

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])
alert_blueprint = Blueprint(name='alerts', import_name=__name__)


@alert_blueprint.route('/')
@requires_login
def index():
    email = session['email']
    if email is not None:
        alerts = Alert.find_by_email(email=email)
        return render_template('alerts/alerts.html', alerts=alerts)

    return render_template('alerts/message.html')


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def create_alert():
    logger.debug('Received request: {}'.format(request.method))
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price = float(request.form['price'])

        item = Item(name=name, url=url)
        item.load_price()
        item.insert_into_database()

        alert = Alert(item_id=item._id, price_threshold=price, user_email=session['email'])
        alert.insert_into_database()
    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/deactivate/<string:alert_id>')
@requires_login
def deactivate_alert(alert_id: str):
    print(alert_id)
    pass


@alert_blueprint.route('/<string:alert_id>')
def get_alert_page(alert_id: str):
    alert = Alert.find_one_by_id(_id=alert_id)
    return render_template('alerts/alert.html', alert=alert)


@alert_blueprint.route('/alerts_for_user/<string:user_id>')
def get_alerts_for_user(user_id: str):
    print(user_id)
    pass
