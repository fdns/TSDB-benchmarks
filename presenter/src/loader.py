import json
import logging
logger = logging.getLogger(__name__)

def load(filename):
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
                check_data_validity(data, file)
                clear_invalid_points(data)
                return data
            except ValueError:
                logger.error('Error parsing json data from file {}'.format(file))
                return False
    except IOError:
        logger.warning('File not found  : {}'.format(filename))
        return False

def check_data_validity(data, file):
    data = data['validation']
    if data[0] != int(data[1]):
        logger.warning('The data is not validated ({} != {}, {} difference) for {}'.format(data[0], data[1], data[0] - data[1], file))

def clear_invalid_points(data):
    data['query'] = [x for x in data['query'] if x[1] >= 0]

