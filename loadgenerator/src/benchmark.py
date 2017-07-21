from cpu_stats import fetch_docker_disk_usuage,fetch_proc_stats
from multiprocessing.pool import ThreadPool
import time
import logging

logger = logging.getLogger(__name__)

class Benchmark(object):
    def print_stats_header(self):
        logger.info("iteration\tcpu_time\tmemory\tdisk")

    def print_stats(self, iteration, pid, volume):
        (cpu_time, memory) = fetch_proc_stats(pid)
        disk = fetch_docker_disk_usuage(volume)
        result = "{}\t{}\t{}\t{}".format(iteration, cpu_time, memory, disk)
        logger.info(result)
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

        return {
            'stats': [x.get() for x in stat_result] + [self.print_stats(i+1, pid, volume)],
            'query': [x.get() for x in query_result] + [benchmarker.query_data()],
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
