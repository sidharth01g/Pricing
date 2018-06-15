from flask import Flask
from pricing.src.common.logging_base import Logging
import pricing

# Import blueprints
from pricing.src.models.users.views import user_blueprint

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])

app = Flask(__name__)
app.secret_key = 'abcd1234'

# Register blueprints
app.register_blueprint(blueprint=user_blueprint, url_prefix='/users')


@app.route('/')
def home():
    return 'Welcome!'


if __name__ == '__main__':
    port = 4776
    logger.info('Starting Pricing Application at port {}'.format(port))
    app.run(port=port)
