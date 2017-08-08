from influxdb import InfluxDBClient
from benchmarker import Benchmarker, AsyncBenchmark
import time
import datetime
import random
import logging
logger = logging.getLogger(__name__)

class InfluxDBBenchmarker(Benchmarker):
    def get_domain_benchmarker(self):
        return InfluxDBDomainBenchmark()

    def get_mask_benchmark(self):
        return InfluxDBMaskBenchmark()

    def get_length_benchmark(self):
        return InfluxDBLengthBenchmark()


class BaseInfluxDBBenchmark(AsyncBenchmark):
    def __init__(self):
        super(BaseInfluxDBBenchmark, self).__init__()
        self.id = 0
        self.client = InfluxDBClient('localhost', 8086, 'root', 'root', 'TestDB')
        self.retention_policy = 'TestDB'
        self.client.create_database('TestDB')
        self.client.create_retention_policy('TestDB', '1d', 1, default=True)

    def current_time(self):
        self.id = (self.id + 1) % 1000000 # Prevent value override
        now = time.mktime(datetime.datetime.now().utctimetuple())
        return int(now)*1000000000+self.id

    def _insert_data(self, data):
        self.client.write_points(data, retention_policy=self.retention_policy)



class InfluxDBDomainBenchmark(BaseInfluxDBBenchmark):
    def __init__(self):
        super(InfluxDBDomainBenchmark, self).__init__()
        logger.info('Nota: La consulta de este benchmark no puede ser utilizada en grafana (incompatible por tags).')

    def insert_data(self, iterator):
        return self.insert_async({
            'time': self.current_time(),
            'measurement': 'domains',
            'tags': {
                'domain': next(iterator)
            },
            'fields': {
                'value': 1
            }
        })

    def validate_data(self, expected):
        start = time.time()
        data = self.client.query('SELECT count(*) FROM domains')
        value = int(next(data.get_points())['count_value'])
        if expected == value:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
        return (expected, value, time.time() - start)

    def query_data(self):
        start = time.time()
        result = self.client.query('SELECT TOP(n, 2), domain FROM (SELECT sum("value") as n FROM "domains" WHERE time > now()-10m GROUP BY time(1m), domain) where time > now()-10m group by time(1m)')
        return time.time() - start


class InfluxDBMaskBenchmark(BaseInfluxDBBenchmark):
    def __init__(self):
        super(InfluxDBMaskBenchmark, self).__init__()

    def insert_data(self, iterator):
        return self.insert_async({
            'time': self.current_time(),
            'measurement': 'masks',
            'tags': {
                'mask': next(iterator)
            },
            'fields': {
                'value': 1
            }
        })

    def validate_data(self, expected):
        start = time.time()
        data = self.client.query('SELECT count(*) FROM masks')
        value = int(next(data.get_points())['count_value'])
        if expected == value:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
        return (expected, value, time.time() - start)

    def query_data(self):
        start = time.time()
        result = self.client.query('SELECT sum("value") FROM "masks" WHERE time > now()-10m GROUP BY time(1m), mask')
        logger.info(result)
        return time.time() - start


class InfluxDBLengthBenchmark(BaseInfluxDBBenchmark):
    def __init__(self):
        super(InfluxDBLengthBenchmark, self).__init__()
        self.sum = 0

    def insert_data(self, iterator):
        val = next(iterator)
        self.sum += val
        return self.insert_async({
            'time': self.current_time(),
            'measurement': 'lengths',
            'fields': {
                'length': val
            }
        })

    def validate_data(self, _):
        start = time.time()
        data = self.client.query('SELECT sum(length) FROM lengths')
        value = int(next(data.get_points())['sum'])
        if self.sum == value:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(self.sum, value))
        return (self.sum, value, time.time() - start)

    def query_data(self):
        start = time.time()
        result = self.client.query('SELECT sum("length") FROM "lengths" WHERE time > now()-10m GROUP BY time(1m)')
        return time.time() - start
