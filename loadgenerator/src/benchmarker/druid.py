import datetime
import json
import urllib2
import StringIO
import gzip
import thread
import time
import logging

from Queue import Queue

from benchmarker import Benchmarker, Benchmark

logger = logging.getLogger(__name__)

class DruidBenchmarker(Benchmarker):
    def get_domain_benchmarker(self):
        return DruidDomainBenchmark()

    def get_mask_benchmark(self):
        return DruidMaskBenchmark()

    def get_length_benchmark(self):
        return DruidLengthBenchmark()

class DruidBaseBenchmark(Benchmark):
    def __init__(self, dataset):
        self.dataset = dataset
        self.insert_url = 'http://localhost:8200/v1/post/{}'.format(dataset)

    def initialize(self):
        self.cache = Queue()
        thread.start_new_thread(self._process_queue, ())

    def _process_queue(self):
        while True:
            cache = []
            for _ in range(self.cache.qsize()):
                cache.append(self.cache.get_nowait())
            if len(cache) > 0:
                self._insert_data('\n'.join([json.dumps(x) for x in cache]))
            # Sleep for one second after the insert
            time.sleep(1)

    def _insert_data(self, data):
        out = StringIO.StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(data)
        data = out.getvalue()

        request = urllib2.Request(self.insert_url,
                                  headers={'Content-Type': 'application/json',
                                           'Content-Encoding': 'gzip'},
                                  data=data)
        opener = urllib2.build_opener()
        while True:
            try:
                opener.open(request)
                break
            except Exception as e:
                logger.exception(e)
                logger.error('Retrying send data')

    def _query(self, query):
        url = 'http://localhost:8082/druid/v2/'
        request = urllib2.Request(url,
                                  headers={'Content-Type': 'application/json'},
                                  data=json.dumps(query))
        opener = urllib2.build_opener()
        return opener.open(request).read()

class DruidDomainBenchmark(DruidBaseBenchmark):
    def __init__(self):
        DruidBaseBenchmark.__init__(self, 'domains')

    def insert_data(self, iterator):
        self.cache.put({
            'timestamp': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'domain': next(iterator)
        })

    def query_data(self):
        now = datetime.datetime.utcnow()
        query = {
            "queryType": "topN",
            "dataSource": "domains",
            "dimension": "domain",
            "threshold": 5,
            "metric": "count",
            "granularity": "minute",
            "aggregations": [
                {
                    "type": "longSum",
                    "name": "count",
                    "fieldName": "count"
                },
            ],
            "postAggregations": [
            ],
            "intervals":["{}/{}".format((now - datetime.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))]
        }
        before = time.time()
        self._query(query)
        return time.time() - before

    def validate_data(self, expected):
        now = datetime.datetime.utcnow()
        query = {
            "queryType": "groupBy",
            "dataSource": "domains",
            "dimension": "domain",
            "metric": "count",
            "granularity": "year",
            "aggregations": [
                {
                    "type": "longSum",
                    "name": "count",
                    "fieldName": "count"
                },
            ],
            "postAggregations": [
            ],
            "intervals":["{}/{}".format((now - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))]
        }
        now = time.time()
        value = json.loads(self._query(query))[0]['event']['count']
        if expected == value:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
        return (expected, value, time.time() - now)

class DruidMaskBenchmark(DruidBaseBenchmark):
    def __init__(self):
        DruidBaseBenchmark.__init__(self, 'masks')

    def insert_data(self, iterator):
        self.cache.put({
            'timestamp': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'mask': next(iterator)
        })

    def query_data(self):
        now = datetime.datetime.utcnow()
        query = {
            "queryType": "groupBy",
            "dataSource": self.dataset,
            "dimensions": ["mask"],
            "granularity": "minute",
            "metric": "count",
            "aggregations": [
                {
                    "type": "longSum",
                    "name": "count",
                    "fieldName": "mask"
                },
            ],
            "postAggregations": [
            ],
            "intervals":["{}/{}".format((now - datetime.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))]
        }
        before = time.time()
        self._query(query)
        return time.time() - before

    def validate_data(self, expected):
        now = datetime.datetime.utcnow()
        query = {
            "queryType": "groupBy",
            "dataSource": self.dataset,
            "metric": "count",
            "granularity": "year",
            "aggregations": [
                {
                    "type": "longSum",
                    "name": "count",
                    "fieldName": "count"
                },
            ],
            "postAggregations": [
            ],
            "intervals":["{}/{}".format((now - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))]
        }
        now = time.time()
        logger.info('validating')
        logger.info(self._query(query))
        value = json.loads(self._query(query))[0]['event']['count']
        if expected == value:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
        return (expected, value, time.time() - now)


class DruidLengthBenchmark(DruidBaseBenchmark):
    def __init__(self):
        DruidBaseBenchmark.__init__(self, 'length')
        self.count = 0

    def insert_data(self, iterator):
        bytes = next(iterator)
        self.count += bytes
        self.cache.put({
            'timestamp': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'bytes': bytes
        })

    def query_data(self):
        now = datetime.datetime.utcnow()
        query = {
            "queryType": "groupBy",
            "dataSource": self.dataset,
            "granularity": "minute",
            "metric": "bytes",
            "aggregations": [
                {
                    "type": "longSum",
                    "name": "bytes",
                    "fieldName": "bytes"
                },
            ],
            "postAggregations": [
            ],
            "intervals":["{}/{}".format((now - datetime.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))]
        }
        before = time.time()
        self._query(query)
        return time.time() - before

    def validate_data(self, _):
        now = datetime.datetime.utcnow()
        expected = self.count
        query = {
            "queryType": "groupBy",
            "dataSource": self.dataset,
            "metric": "count",
            "granularity": "year",
            "aggregations": [
                {
                    "type": "longSum",
                    "name": "bytes",
                    "fieldName": "bytes"
                },
            ],
            "postAggregations": [
            ],
            "intervals":["{}/{}".format((now - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ"), now.strftime("%Y-%m-%dT%H:%M:%SZ"))]
        }
        now = time.time()
        logger.info(self._query(query))
        value = json.loads(self._query(query))[0]['event']['bytes']
        if expected == value:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
        return (expected, value, time.time() - now)
