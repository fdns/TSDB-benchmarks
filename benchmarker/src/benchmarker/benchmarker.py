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
    def data_sended(self):
        return True

class AsyncBenchmark(Benchmark):
    MAX_QUEUE_SIZE = 500000

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

    def _data_in_queue(self):
        return not self.cache.empty()

    def _insert_data(self, data):
        raise NotImplementedError()

    def insert_async(self, data):
        # If the queue is bigger than the max, wait for it to process some data
        # Every item will wait one second until the size is less than the max
        if self.cache.qsize() > self.MAX_QUEUE_SIZE:
            time.sleep(1)
        self.cache.put(data)

    def data_sended(self):
        return not self._data_in_queue()
