class Benchmarker(object):
    def get_domain_benchmarker(self, iterator):
        raise NotImplementedError()
    def get_mask_benchmark(self):
        raise NotImplementedError()
    def get_length_benchmark(self, expected):
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
