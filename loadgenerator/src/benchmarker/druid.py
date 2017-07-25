import datetime
import json
import urllib2
import StringIO
import gzip
import thread
import time
import logging

from Queue import Queue

from load_iterators import generate_random_domain_iterator
from benchmarker import Benchmarker, Benchmark

logger = logging.getLogger(__name__)

class DruidBenchmarker(Benchmarker):
    def get_domain_benchmarker(self):
        return DruidDomainBenchmark()

class DruidBaseBenchmark(Benchmark):
    def __init__(self, url):
        self.url = url

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

        request = urllib2.Request(self.url,
                                  headers={'Content-Type': 'application/json',
                                           'Content-Encoding': 'gzip'},
                                  data=data)
        opener = urllib2.build_opener()
        opener.open(request)

    def _query(self, query):
        url = 'http://localhost:8082/druid/v2/'
        request = urllib2.Request(url,
                                  headers={'Content-Type': 'application/json'},
                                  data=json.dumps(query))
        opener = urllib2.build_opener()
        return opener.open(request).read()

class DruidDomainBenchmark(DruidBaseBenchmark):
    def __init__(self):
        DruidBaseBenchmark.__init__(self, 'http://localhost:8200/v1/post/domains')

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
            "granularity": "day",
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


if __name__ == '__main__':
    it = generate_random_domain_iterator(10, 100000)
    def get_rand():
        return {
            'timestamp': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'domain': next(it)
        }

    if __name__ == '__main__':
        url = 'http://localhost:8200/v1/post/domains'
        # Advertencia: Si los tasks de un intervalo fallaron, Tranquility ignora todos los datos enviados
        while True:
            data = '\n'.join([json.dumps(get_rand()) for _ in range(1000)])
            import StringIO, gzip
            out = StringIO.StringIO()
            with gzip.GzipFile(fileobj=out, mode="w") as f:
                f.write(data)
            data = out.getvalue()

            request = urllib2.Request(url,
                                      headers={'Content-Type': 'application/json',
                                               'Content-Encoding': 'gzip'},
                                      data=data)
            opener = urllib2.build_opener()
            print(opener.open(request).read(), datetime.datetime.now().time())
            import time
            time.sleep(1)
            #break
        print('sended')
        import os
        os._exit(0)
        from pydruid.client import *
        from pydruid.utils.aggregators import doublesum
        query = PyDruid("http://localhost:8082", 'druid/v2')
        ts = query.timeseries(
            datasource='domains',
            granularity='minute',
            intervals='2017-07-24/p4w',
            aggregations={'count': doublesum('count')},
        )
        print(ts[:])
