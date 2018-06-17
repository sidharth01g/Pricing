from flask import Blueprint

alert_blueprint = Blueprint(name='alerts', import_name=__name__)


@alert_blueprint.route('/')
def index():
    return "This is the alerts index page"


@alert_blueprint.route('/new', methods=['POST'])
def create_alert():
    pass


@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id: str):
    pass


@alert_blueprint.route('/alert/<string:alert_id>')
def get_alert_page(alert_id: str):
    pass


@alert_blueprint.route('/alerts_for_user/<string:user_id>')
def get_alets_for_user(user_id: str):
    pass
