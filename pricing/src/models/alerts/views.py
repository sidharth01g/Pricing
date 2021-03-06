import pricing
from flask import Blueprint, session, render_template, request, redirect, url_for
from pricing.src.models.alerts.alert import Alert
from pricing.src.models.items.item import Item
from pricing.src.common.logging_base import Logging
from pricing.src.models.users.decorators import requires_login

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])
alert_blueprint = Blueprint(name='alerts', import_name=__name__)


@alert_blueprint.route('/')
@requires_login
def index() -> str:
    email = session['email']
    if email is not None:
        alerts = Alert.find_by_email(email=email)
        return render_template('alerts/alerts.html', alerts=alerts)

    return render_template('alerts/message.html')


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def create_alert() -> str:
    logger.debug('Received request: {}'.format(request.method))
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price = float(request.form['price'])

        item = Item(name=name, url=url)
        item.load_price(update_in_database=True)

        alert = Alert(item_id=item._id, price_threshold=price, user_email=session['email'])
        alert.insert_into_database()
    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id: str) -> str:
    alert = Alert.find_one_by_id(_id=alert_id)
    if request.method == 'POST':

        price = float(request.form['price'])

        alert.price_threshold = price

        alert.update_in_database(upsert=False)
        return redirect(location=url_for(endpoint='.get_alert_page', alert_id=alert._id))
    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/deactivate/<string:alert_id>')
@requires_login
def deactivate_alert(alert_id: str) -> str:
    logger.debug('Deactivate alert: {}'.format(alert_id))
    alert = Alert.find_one_by_id(_id=alert_id)
    alert.deactivate()
    return redirect(location=url_for(endpoint='.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/activate/<string:alert_id>')
@requires_login
def activate_alert(alert_id: str) -> str:
    logger.debug('Activate alert: {}'.format(alert_id))
    alert = Alert.find_one_by_id(_id=alert_id)
    alert.activate()
    return redirect(location=url_for(endpoint='.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id: str) -> str:
    logger.debug('Delete alert: {}'.format(alert_id))
    Alert.remove_alert(alert_id=alert_id)
    return redirect(location=url_for(endpoint='.'))


@alert_blueprint.route('/<string:alert_id>')
@requires_login
def get_alert_page(alert_id: str) -> str:
    alert = Alert.find_one_by_id(_id=alert_id)
    return render_template('alerts/alert.html', alert=alert)


@alert_blueprint.route('/alerts_for_user/<string:user_id>')
@requires_login
def get_alerts_for_user(user_id: str) -> str:
    return 'Alerts for {}'.format(user_id)


@alert_blueprint.route('/load_item_price/<string:alert_id>')
@requires_login
def load_item_price(alert_id: str) -> str:
    alert = Alert.find_one_by_id(_id=alert_id)
    if not alert:
        logger.error('Alert ID {} not found in order to load price'.format(alert_id))
        return redirect(location=url_for(endpoint='.'))
    alert.refresh()
    return redirect(location=url_for(endpoint='.get_alert_page', alert_id=alert_id))
