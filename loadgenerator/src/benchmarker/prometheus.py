from prometheus_client import start_http_server, Counter
from benchmarker import Benchmarker, Benchmark
import time
import json
import urllib
import urllib2
import logging

logger = logging.getLogger(__name__)


domain = Counter('test_dns_query_name', 'Number of dns requests for query name', ['name'])
subnetwork = Counter('test_subnetwork_query', 'Number of dns requests by subnetwork', ['name'])
length = Counter('test_packet_size', 'Length of the responces generated')

class PrometheusBenchmark(Benchmarker):
    def get_domain_benchmarker(self):
        return PrometheusDomainBenchmark()

    def get_mask_benchmark(self):
        return PrometheusMaskBenchmark()

    def get_length_benchmark(self):
        return PrometheusLengthBenchmark()


class PrometheusBaseBenchmark(Benchmark):
    def initialize(self):
        start_http_server(8000)

    def _query_range(self, query):
        url = 'http://localhost:9090/api/v1/query_range?'
        query = {
            'query': query,
            'start': int(time.time()) - 600,
            'end': int(time.time()),
            'step': 60,
        }
        before = time.time()
        urllib2.urlopen(url + urllib.urlencode(query)).read()
        dt = time.time() - before
        return dt

    def _check_quantity(self, query, expected):
        time.sleep(20)
        url = 'http://localhost:9090/api/v1/query?'
        query = {
            'query': query,
        }
        before = time.time()

        result = urllib2.urlopen(url + urllib.urlencode(query)).read()
        dt = time.time() - before
        logger.debug(result)
        value = int(json.loads(result)['data']['result'][0]['value'][1])
        if value == expected:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected,
                                                                                                               value))
        return (expected, value, dt)


class PrometheusDomainBenchmark(PrometheusBaseBenchmark):
    def insert_data(self, iterator):
        domain.labels(name=next(iterator)).inc()

    def query_data(self):
        return self._query_range('topk(5,sum_over_time(test_dns_query_name[1m])) by (group)')

    def validate_data(self, expected):
        return self._check_quantity('sum(test_dns_query_name)', expected)


class PrometheusMaskBenchmark(PrometheusBaseBenchmark):
    def insert_data(self, iterator):
        subnetwork.labels(name=next(iterator)).inc()

    def query_data(self):
        return self._query_range('sum_over_time(test_subnetwork_query[1m])')

    def validate_data(self, expected):
        return self._check_quantity('sum(test_subnetwork_query)', expected)


class PrometheusLengthBenchmark(PrometheusBaseBenchmark):
    def __init__(self):
        self.total_sended = 0

    def insert_data(self, iterator):
        n = next(iterator)
        self.total_sended += n
        length.inc(n)

    def query_data(self):
        return self._query_range('sum_over_time(test_packet_size[1m])')

    def validate_data(self, _):
        return self._check_quantity('sum(test_packet_size)', self.total_sended)
