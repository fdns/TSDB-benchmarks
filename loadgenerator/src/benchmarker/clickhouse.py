from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.models import Model
from infi.clickhouse_orm.fields import *
from infi.clickhouse_orm.engines import MergeTree

class Domains(Model):
    query_date = DateField()
    timestamp = DateTimeField()
    domain_name = StringField()
    count = Int32Field()

    engine = MergeTree('query_date', ('timestamp', 'domain_name'))

db = Database('TestDB')
db.create_table(Domains)

from load_iterators import generate_random_domain_iterator
dns = generate_random_domain_iterator(size=100000)
while True:
    timestamp = datetime.datetime.utcnow()
    data = []
    for i in range(10000):
        data.append(Domains(query_date=timestamp.date(), timestamp=timestamp, domain_name=next(dns), count=1))
    db.insert(data)
    dt = datetime.datetime.utcnow() - timestamp
    if dt < datetime.timedelta(seconds=1):
        import time
        time.sleep(1 - dt.microseconds/1000000.)

#SELECT t, groupArray((domain_name, c)) as groupArr FROM (     SELECT (intDiv(toUInt32(toStartOfMinute(timestamp)), 10) * 10) * 1000 as t, domain_name, count(*) as c     FROM TestDB.domains     WHERE query_date >= toDate(1501272757) AND timestamp >= toDateTime(1501272757) GROUP BY t, domain_name ORDER BY t limit 5 by t ) GROUP BY t order by t
for i in db.select('SELECT t, groupArray((domain_name, c)) as groupArr FROM (     SELECT (intDiv(toUInt32(toStartOfMinute(timestamp)), 10) * 10) * 1000 as t, domain_name, count(*) as c     FROM TestDB.domains     WHERE query_date >= toDate(1501268571) AND timestamp >= toDateTime(1501268571) GROUP BY t, domain_name ORDER BY t ) GROUP BY t'):
    print i.t
print db.count(Domains)