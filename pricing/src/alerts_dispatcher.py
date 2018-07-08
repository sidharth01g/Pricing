from pricing.src.models.alerts.alert import Alert
from pricing.src.common.logging_base import Logging
import pricing

logger = Logging.create_rotating_log(module_name=__name__, logging_directory=pricing.configuration['logging_directory'])

alerts_to_update = Alert.get_alerts_to_update()
logger.debug('Alerts to update: {}'.format(alerts_to_update))

for alert in alerts_to_update:
    alert.send_email_if_price_reached()
