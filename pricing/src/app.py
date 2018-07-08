from flask import Flask, render_template
from pricing.src.common.logging_base import Logging
import pricing

# Import blueprints
from pricing.src.models.users.views import user_blueprint
from pricing.src.models.alerts.views import alert_blueprint
from pricing.src.models.stores.views import store_blueprint

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])

app = Flask(__name__)
app.secret_key = 'abcd1234'

# Register blueprints
app.register_blueprint(blueprint=user_blueprint, url_prefix='/users')
app.register_blueprint(blueprint=alert_blueprint, url_prefix='/alerts')
app.register_blueprint(blueprint=store_blueprint, url_prefix='/stores')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    port = 4776
    logger.info('Starting Pricing Application at port {}'.format(port))
    app.run(port=port, debug=True)
