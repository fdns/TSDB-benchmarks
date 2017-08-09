import json
import logging
logger = logging.getLogger(__name__)

def load(filename):
    with open(filename) as file:
        try:
            return json.load(file)
        except ValueError:
            logger.error('Error parsing json data from file {}'.format(file))
            raise ValueError('Error parsing json data from file {}'.format(filename))