from pricing.src.app import app
from pricing.src.common.logging_base import Logging

logger = Logging.create_rotating_log(module_name=__name__, logging_directory='/tmp')

logger.info('Launching Pricing Aplication')
app.run(debug=True, port=4990)
