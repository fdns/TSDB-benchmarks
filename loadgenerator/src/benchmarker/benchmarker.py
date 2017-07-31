from Queue import Queue
import thread
import time

class Benchmarker(object):
    def get_domain_benchmarker(self):
        raise NotImplementedError()
    def get_mask_benchmark(self):
        raise NotImplementedError()
    def get_length_benchmark(self):
        raise NotImplementedError()

class Benchmark(object):
    def initialize(self):
        pass
    def insert_data(self, iterator):
        raise NotImplementedError()
    def query_data(self):
        raise NotImplementedError()
    def validate_data(self, expected):
        raise NotImplementedError()

class AsyncBenchmark(Benchmark):
    def initialize(self):
        self.cache = Queue()
        thread.start_new_thread(self.__process_queue, ())

    def __process_queue(self):
        while True:
            cache = []
            for _ in range(self.cache.qsize()):
                cache.append(self.cache.get_nowait())
            if len(cache) > 0:
                self._insert_data(cache)
            # Sleep for one second after the insert
            time.sleep(1)

    def _insert_data(self, data):
        raise NotImplementedError()

    def insert_async(self, data):
        self.cache.put(data)
