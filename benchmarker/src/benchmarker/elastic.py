from threading import Lock
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from benchmarker import Benchmarker, AsyncBenchmark

import time
import logging
logger = logging.getLogger(__name__)


class ElasticBenchmarker(Benchmarker):
    def get_domain_benchmarker(self):
        return ElasticDomainBenchmark()

    def get_mask_benchmark(self):
        return ElasticMaskBenchmark()

    def get_length_benchmark(self):
        return ElasticLengthBenchmark()

class ElasticBaseBenchmark(AsyncBenchmark):
    def __init__(self):
        super(ElasticBaseBenchmark, self).__init__()
        logging.getLogger('elasticsearch').setLevel(logging.WARNING)
        self.mutex = Lock()
        self.es = Elasticsearch()
        self.__create_indices()

    def _insert_data(self, data):
        with self.mutex:
            bulk(self.es, data)

    def _count_data(self, expected, doc_type):
        with self.mutex:
            time.sleep(60)
            now = time.time()
            value = self.es.search(
                index='test',
                doc_type=doc_type,
                body={
                    'query': {
                    },
                    'aggs': {
                        'total_count': {
                            'value_count': {
                                'field': 'type'
                            }
                        }
                    }
                })
            value = value['hits']['total']
            if expected == value:
                logger.info('The stored data is equal to the produced quantity.')
            else:
                logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
            return (expected, value, time.time() - now)

    def __create_indices(self):
        self.es.indices.create('test', body={
            'settings': {
                'index': {
                    'refresh_interval': '5s',
                },
            },
            'mappings': {
                'domain': {
                    "_all": {"enabled": False},
                    "_source": {"enabled": False},
                    'properties': {
                        '@timestamp': {
                            'type': 'date',
                        },
                        'domain': {
                            "index": "not_analyzed",
                            'type': 'keyword',
                        }
                    }
                },
                'mask': {
                    "_all": {"enabled": False},
                    "_source": {"enabled": False},
                    'properties': {
                        '@timestamp': {
                            'type': 'date',
                        },
                        'mask': {
                            "index": "not_analyzed",
                            'type': 'ip',
                        }
                    }
                },
                'length': {
                    "_all": {"enabled": False},
                    "_source": {"enabled": False},
                    'properties': {
                        '@timestamp': {
                            'type': 'date',
                        },
                        'length': {
                            "index": "not_analyzed",
                            'type': 'integer',
                        }
                    }
                },
            },
        })

class ElasticDomainBenchmark(ElasticBaseBenchmark):
    def insert_data(self, iterator):
        self.insert_async({
            "_index": "test",
            "_type": "domain",
            "_source": {
                '@timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                'domain': next(iterator)
            }
        })

    def query_data(self):
        start = time.time()
        try:
            self.es.search(
                index='test',
                doc_type='domain',
                timeout='300s',
                request_timeout=300,
                body={
                    'query': {
                    },
                    'aggs': {
                        'total': {
                            'date_histogram': {
                                'interval': '1m',
                                'field': '@timestamp'
                            },
                            'aggs': {
                                'dt': {
                                    'terms': {
                                        'field': 'domain',
                                        "size": 2,
                                        "order": {"_count": "desc"}
                                    },
                                }
                            }
                        }
                    }
                }
            )
        except Exception as e:
            logger.exception(e)
            return (start, -1)
        return (start, time.time() - start)

    def validate_data(self, expected):
        return self._count_data(expected, 'domain')

class ElasticMaskBenchmark(ElasticBaseBenchmark):
    def insert_data(self, iterator):
        self.insert_async({
            "_index": "test",
            "_type": "mask",
            "_source": {
                '@timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                'mask': next(iterator)
            }
        })

    def query_data(self):
        start = time.time()
        self.es.search(
            index='test',
            doc_type='mask',
            timeout='60s',
            body={
                'query': {
                },
                'aggs': {
                    'total': {
                        'date_histogram': {
                            'interval': '1m',
                            'field': '@timestamp'
                        },
                        'aggs': {
                            'dt': {
                                'terms': {
                                    'field': 'mask',
                                },
                            }
                        }
                    }
                }
            }
        )
        return (start, time.time() - start)

    def validate_data(self, expected):
        return self._count_data(expected, 'mask')


class ElasticLengthBenchmark(ElasticBaseBenchmark):
    def __init__(self):
        super(ElasticLengthBenchmark, self).__init__()
        self.count = 0

    def insert_data(self, iterator):
        value = next(iterator)
        self.count += value
        self.insert_async({
            "_index": "test",
            "_type": "length",
            "_source": {
                '@timestamp': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                'length': value
            }
        })

    def query_data(self):
        start = time.time()
        self.es.search(
            index='test',
            doc_type='length',
            timeout='60s',
            body={
                'query': {
                },
                'aggs': {
                    'total': {
                        'date_histogram': {
                            'interval': '1m',
                            'field': '@timestamp'
                        },
                        'aggs': {
                            'total': {
                                'sum': {
                                    'field': 'length',
                                },
                            }
                        }
                    }
                }
            }
        )
        return (start, time.time() - start)

    def validate_data(self, _):
        with self.mutex:
            time.sleep(60)
            now = time.time()
            value = self.es.search(
                index='test',
                doc_type='length',
                body={
                    'query': {
                    },
                    'aggs': {
                        'total_count': {
                            'sum': {
                                'field': 'length'
                            }
                        }
                    }
                })

            value = value['aggregations']['total_count']['value']
            if self.count == value:
                logger.info('The stored data is equal to the produced quantity.')
            else:
                logger.warning(
                    'The stored data is different to the produced quantity (expected {} != {}).'.format(self.count, value))
            return (self.count, value, time.time() - now)
