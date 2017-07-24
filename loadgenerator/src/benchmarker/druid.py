import datetime
import json
import urllib, urllib2

from load_iterators import generate_random_domain_iterator

it = generate_random_domain_iterator(5, 10000)
def get_rand():
    return {
        'timestamp': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        'domain': next(it)
    }

if __name__ == '__main__':
    url = 'http://localhost:8200/v1/post/domains'

    while True:
        request = urllib2.Request(url,
                                  headers={'Content-Type': 'application/json'},
                                  data='\n'.join([json.dumps(get_rand()) for _ in range(500)]))
        opener = urllib2.build_opener()
        print(opener.open(request).read())
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
