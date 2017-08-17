from cpu_stats import fetch_docker_disk_usuage,fetch_proc_stats
from multiprocessing.pool import ThreadPool
import time
import logging

logger = logging.getLogger(__name__)

class Benchmark(object):
    def print_stats_header(self):
        logger.info("timestamp\titeration\tcpu_time\tmemory\tdisk")

    def print_stats(self, iteration, pids, volume):
        try:
            (cpu_time, memory) = fetch_proc_stats(pids)
            disk = fetch_docker_disk_usuage(volume)
            result = {
                'timestamp': int(time.time()),
                'iteration': iteration,
                'cpu': cpu_time,
                'memory': memory,
                'disk': disk
            }
            logger.info("{timestamp}\t{iteration}\t{cpu}\t{memory}\t{disk}".format(**result))
        except Exception as e:
            logger.exception(e)
            import os
            os._exit(0)
        return result

    def _run_benchmark(self, benchmarker, data_iterator, pid, volume, seconds, step):
        """
        Run the selected benchmark
        :type benchmarker: benchmarker.benchmarker.Benchmark
        :type data_iterator: collections.Iterable
        :type pid: int
        :type volume: str
        :type seconds: int
        :type step: int
        :return: str
        """
        benchmarker.initialize()
        self.print_stats_header()
        pool = ThreadPool(processes=2)
        total = seconds * step
        start = time.time()
        stat_result = []
        query_result = []
        for i in range(total):
            if i % step == 0:
                if i % (step*10) == 0:
                    stat_result.append(pool.apply_async(self.print_stats, (i, pid, volume)))
                if i % (step*60) == 0:
                    query_result.append(pool.apply_async(benchmarker.query_data, ()))
                dt = time.time() - start
                if dt < 1:
                    time.sleep(1-dt)
                start = time.time()
            benchmarker.insert_data(data_iterator)

        # Send the last print stat and query data
        last_stats = self.print_stats(i+1, pid, volume)
        last_query = benchmarker.query_data()
        # Wait until all the data is sended
        while not benchmarker.data_sended():
            logger.warning('Waiting for benchmarker to finish sending data')
            time.sleep(5)
        # Give the databases time to catch up before validating
        time.sleep(10)
        return {
            'stats': [x.get() for x in stat_result] + [last_stats],
            'query': [x.get() for x in query_result] + [last_query],
            'validation': benchmarker.validate_data(total),
        }

    def run_benchmark(self, benchmarker, data_iterator, pid, volume, seconds, step):
        raise NotImplementedError()

class DomainBenchmark(Benchmark):
    def run_benchmark(self, benchmarker, data_iterator, pid, volume, seconds, step):
        return self._run_benchmark(benchmarker.get_domain_benchmarker(), data_iterator, pid, volume, seconds, step)

class SubnetworkBenchmark(Benchmark):
    def run_benchmark(self, benchmarker, data_iterator, pid, volume, seconds, step):
        return self._run_benchmark(benchmarker.get_mask_benchmark(), data_iterator, pid, volume, seconds, step)

class LengthBenchmark(Benchmark):
    def run_benchmark(self, benchmarker, data_iterator, pid, volume, seconds, step):
        return self._run_benchmark(benchmarker.get_length_benchmark(), data_iterator, pid, volume, seconds, step)
