from benchmark import DomainBenchmark, SubnetworkBenchmark, LengthBenchmark
from load_iterators import generate_random_domain_iterator, generate_random_ipv4_mask_iterator, generate_random_size_iterator
from benchmarker.prometheus import PrometheusBenchmark
from benchmarker.druid import DruidBenchmarker
from benchmarker.clickhouse import ClickHouseBenchmarker
from benchmarker.influxdata import InfluxDBBenchmarker
from benchmarker.elastic import ElasticBenchmarker
from benchmarker.opentsdb import OpenTSDBBenchmarker

import argparse
import logging
import json

logger = logging.getLogger()


def run_domain_benchmark(benchmarker, pid, volume, seconds, step):
    # Get the data iterators
    domain = generate_random_domain_iterator()
    return DomainBenchmark().run_benchmark(benchmarker, domain, pid, volume, seconds, step)

def run_mask_benchmark(benchmarker, pid, volume, seconds, step):
    mask = generate_random_ipv4_mask_iterator()
    return SubnetworkBenchmark().run_benchmark(benchmarker, mask, pid, volume, seconds, step)

def run_length_benchmark(benchmarker, pid, volume, seconds, step):
    size = generate_random_size_iterator()
    return LengthBenchmark().run_benchmark(benchmarker, size, pid, volume, seconds, step)

parser = argparse.ArgumentParser(description='Run a benchmark for the given pid and volume.')
parser.add_argument('--debug', action='store_const', help='Show debug information', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
type = parser.add_mutually_exclusive_group(required=True)
type.add_argument('--domain', action='store_const', help='Run the domain benchmark', dest='bench_type', const=run_domain_benchmark)
type.add_argument('--mask', action='store_const', help='Run the mask benchmark', dest='bench_type', const=run_mask_benchmark)
type.add_argument('--length', action='store_const', help='Run the packet length benchmark', dest='bench_type', const=run_length_benchmark)
database = parser.add_mutually_exclusive_group(required=True)
database.add_argument('--prometheus', action='store_const', help='Execute the prometheus benchmark', dest='database', const=PrometheusBenchmark())
database.add_argument('--druid', action='store_const', help='Execute the prometheus benchmark', dest='database', const=DruidBenchmarker())
database.add_argument('--clickhouse', action='store_const', help='Execute the ClickHouse benchmark', dest='database', const=ClickHouseBenchmarker())
database.add_argument('--influxdb', action='store_const', help='Execute the InfluxDB benchmark', dest='database', const=InfluxDBBenchmarker())
database.add_argument('--elasticsearch', action='store_const', help='Execute the ElasticSeach benchmark', dest='database', const=ElasticBenchmarker())
database.add_argument('--opentsdb', action='store_const', help='Execute the OpenTSDB benchmark', dest='database', const=OpenTSDBBenchmarker())
parser.add_argument('pids', type=str, help='List of new-line separated pids to monitor')
parser.add_argument('volume', type=str, help='Volume name used by the database')
parser.add_argument('seconds', nargs='?', type=int, help='Number of seconds used for the benchmark', default=1200)
parser.add_argument('step', nargs='?', type=int, help='Number of metrics generated each second', default=1000)

if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig()
    logger.setLevel(args.loglevel)
    logger.info('Total number of metrics: {}'.format(args.seconds * args.step))
    logger.info('Pids to monitor: {}'.format(args.pids))
    print(json.dumps(args.bench_type(args.database, args.pids, args.volume, args.seconds, args.step)))
