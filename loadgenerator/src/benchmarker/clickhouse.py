from benchmarker import Benchmarker, AsyncBenchmark
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree

import logging
logger = logging.getLogger(__name__)

class Domains(Model):
    query_date = DateField()
    timestamp = DateTimeField()
    domain_name = StringField()

    engine = MergeTree('query_date', ('timestamp', 'domain_name'))

class Mask(Model):
    query_date = DateField()
    timestamp = DateTimeField()
    mask = StringField()

    engine = MergeTree('query_date', ('timestamp', 'mask'))

class Length(Model):
    query_date = DateField()
    timestamp = DateTimeField()
    length = UInt32Field()

    engine = MergeTree('query_date', ('timestamp',))

class ClickHouseBenchmarker(Benchmarker):
    def get_domain_benchmarker(self):
        return ClickHouseDomainBenchmark()

    def get_mask_benchmark(self):
        pass

    def get_length_benchmark(self):
        pass

class ClickHouseDomainBenchmark(AsyncBenchmark):
    def __init__(self):
        super(AsyncBenchmark, self).__init__()
        self.db = Database('TestDB')
        self.db.create_table(Domains)

    def insert_data(self, iterator):
        timestamp = datetime.datetime.utcnow()
        self.insert_async(Domains(query_date=timestamp.date(), timestamp=timestamp, domain_name=next(iterator)))

    def _insert_data(self, data):
        self.db.insert(data)

    def query_data(self):
        now = datetime.datetime.now()
        before = now - datetime.timedelta(minutes=10)
        now = time.mktime(now.utctimetuple())
        before = time.mktime(before.utctimetuple())
        self.db.raw('SELECT t, groupArray((domain_name, c)) as groupArr FROM (SELECT (intDiv(toUInt32(toStartOfMinute(timestamp)), 10) * 10) * 1000 as t, domain_name, count(*) as c FROM TestDB.domains WHERE query_date BETWEEN toDate(1501514798) AND toDate({}) AND timestamp BETWEEN toDateTime({}) AND toDateTime({}) GROUP BY t, domain_name ORDER BY t limit 5 by t ) GROUP BY t order by t'\
                    .format(now, before, now, before))

    def validate_data(self, expected):
        now = time.time()
        value = int(self.db.raw('SELECT count(*) FROM TestDB.domains'))
        if expected == value:
            logger.info('The stored data is equal to the produced quantity.')
        else:
            logger.warning('The stored data is different to the produced quantity (expected {} != {}).'.format(expected, value))
        return (expected, value, time.time() - now)
