from flask import Flask

from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome!'
