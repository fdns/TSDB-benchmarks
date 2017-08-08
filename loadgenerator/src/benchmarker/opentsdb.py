from benchmarker import Benchmarker, AsyncBenchmark
from threading import Lock
import json
import urllib
import urllib2
import time
import logging

logger = logging.getLogger(__name__)


class OpenTSDBBenchmarker(Benchmarker):
    def get_domain_benchmarker(self):
        return OpenTSDBDomainBenchmark()

    def get_mask_benchmark(self):
        return OpenTSDBMaskBenchmark()

    def get_length_benchmark(self):
        return OpenTSDBLengthBenchmark()


class OpenTSDBBaseBenchmark(AsyncBenchmark):
    def __init__(self):
        super(OpenTSDBBaseBenchmark, self).__init__()
        self.lock = Lock()

    def _deduplicate(self, data):
        dedup = {}
        metric = data[0]['metric']
        tagk = data[0]['tags'].keys()[0]
        for item in data:
            tag = item['tags'].values()[0]
            if item['timestamp'] not in dedup:
                dedup[item['timestamp']] = {
                    tag: item['value']
                }
            elif tag not in dedup[item['timestamp']]:
                dedup[item['timestamp']][tag] = item['value']
            else:
                dedup[item['timestamp']][tag] += item['value']

        # Rebuild item
        result = []
        for (key, val) in dedup.iteritems():
            for (tag, count) in val.iteritems():
                result.append({
                    'metric': metric,
                    'timestamp': key,
                    'value': count,
                    'tags': {
                        tagk: tag,
                    }})
        return result

    def _insert_data(self, data):
        # Lock the insert so the validation can wait for the inserts
        with self.lock:
            # Deduplicate the data and insert after
            data = self._deduplicate(data)

            chunk = 2000
            for i in range(0,len(data), chunk):
                url = 'http://localhost:4242/api/put?details=1'
                request = urllib2.Request(url,
                                          headers={'Content-Type': 'application/json'},
                                          data=json.dumps(data[i:i+chunk]))
                opener = urllib2.build_opener()
                try:
                    r = opener.open(request).read()
                    if json.loads(r)['failed'] != 0:
                        logger.warning('Error inserting data: {}'.format(r))
                except urllib2.HTTPError as e:
                    logger.exception(e)

    def _validate_data(self, expected, metric):
        while self._data_in_queue():
            logger.info('Waiting for data to be sended')
            time.sleep(10)
        time.sleep(60)
        with self.lock:
            start = time.time()
            url = 'http://localhost:4242/api/query?start={}&m=sum:1h-sum-none:{}'.format(int(time.time())-24*60*60, metric)
            request = urllib2.Request(url)
            opener = urllib2.build_opener()
            result = opener.open(request).read()
            data = json.loads(result)[0]
            value = 0
            for v in data['dps'].itervalues():
                value += int(v)

            if expected == value:
                logger.info('The stored data is equal to the produced quantity.')
            else:
                logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
            return (expected, value, time.time() - start)

class OpenTSDBDomainBenchmark(OpenTSDBBaseBenchmark):
    def insert_data(self, iterator):
        return self.insert_async({
            'metric': 'domains',
            'timestamp': int(time.time()),
            'value': 1,
            'tags': {
                'domain': next(iterator)
            }
        })

    def query_data(self):
        # Note: Querying over 10m range with 1m querys never return the result
        url = 'http://localhost:4242/api/query/gexp?start={}&end={}&exp=highestCurrent(sum:5m-sum-none:domains{{domain=*}}, 5)'
        now = int(time.time()) - 60*10
        start = time.time()
        try:
            opener = urllib2.build_opener()
            for i in range(1):
                req = url.format(now+i*60*5,now+(i+1)*60*10)
                urllib.urlopen(req).read()
        except urllib2.HTTPError:
            logger.warning('Error reading data, this can happen the first time when no data have been inserted')
            logger.warning(req)
        except Exception as e:
            logger.error(req)
            logger.exception(e)
        return time.time() - start

    def validate_data(self, expected):
        return self._validate_data(expected, 'domains')


class OpenTSDBMaskBenchmark(OpenTSDBBaseBenchmark):
    def insert_data(self, iterator):
        return self.insert_async({
            'metric': 'masks',
            'timestamp': int(time.time()),
            'value': 1,
            'tags': {
                'mask': next(iterator)
            }
        })

    def query_data(self):
        # Note: Querying over 10m range with 1m querys never return the result
        url = 'http://localhost:4242/api/query?start={}&end={}&m=sum:1m-sum-none:masks{{mask=*}}'
        now = int(time.time())
        start = time.time()
        try:
            opener = urllib2.build_opener()
            req = url.format(now - 60*10, now)
            result = opener.open(req)
        except urllib2.HTTPError:
            logger.warning('Error reading data, this can happen the first time when no data have been inserted')
            logger.warning(req)
        except Exception as e:
            logger.error(req)
            logger.exception(e)
        return time.time() - start

    def validate_data(self, expected):
        return self._validate_data(expected, 'masks')


class OpenTSDBLengthBenchmark(OpenTSDBBaseBenchmark):
    def __init__(self):
        super(OpenTSDBLengthBenchmark, self).__init__()
        self.count = 0

    def insert_data(self, iterator):
        val = next(iterator)
        self.count += val
        return self.insert_async({
            'metric': 'length',
            'timestamp': int(time.time()),
            'value': val,
            'tags': {
                'host': 'localhost'
            }
        })

    def query_data(self):
        # Note: Querying over 10m range with 1m querys never return the result
        url = 'http://localhost:4242/api/query?start={}&end={}&m=sum:1m-sum-none:length'
        now = int(time.time())
        start = time.time()
        try:
            opener = urllib2.build_opener()
            req = url.format(now - 60*10, now)
            respose = opener.open(req)
        except urllib2.HTTPError:
            logger.warning('Error reading data, this can happen the first time when no data have been inserted')
            logger.warning(req)
        except Exception as e:
            logger.exception(e)
            logger.error(req)
        return time.time() - start

    def validate_data(self, _):
        return self._validate_data(self.count, 'length')
